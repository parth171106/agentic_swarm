# STUB-FILL — Implemented by: workstream/2b-llm-adapter-tools
import asyncio
import threading
from typing import Any, List, Optional, Dict
from pydantic import PrivateAttr
from openai import AsyncOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.outputs import ChatResult, ChatGeneration
from langchain_core.callbacks import (
    CallbackManagerForLLMRun,
    AsyncCallbackManagerForLLMRun,
)
from backend.app.core.config import settings
from backend.app.core.logging import get_logger
from backend.app.core.circuit_breaker import (
    check_breaker,
    record_failure,
    record_success,
    CircuitBreakerOpen,
)
from backend.app.memory.repository import SupabaseRepository

logger = get_logger("llm_adapter")


def _run_async(coro):
    result = []
    exception = []

    def target():
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            res = loop.run_until_complete(coro)
            result.append(res)
        except Exception as e:
            exception.append(e)
        finally:
            loop.close()

    thread = threading.Thread(target=target)
    thread.start()
    thread.join()

    if exception:
        raise exception[0]
    return result[0]


class LLMAdapter(BaseChatModel):
    model: str
    temperature: float = 0.0
    max_tokens: int = 512

    _clients: dict = PrivateAttr()

    def __init__(
        self, model: str, temperature: float = 0.0, max_tokens: int = 512, **kwargs
    ):
        super().__init__(
            model=model, temperature=temperature, max_tokens=max_tokens, **kwargs
        )

        # Instantiate fallback client layers
        self._clients = {
            "gemini": AsyncOpenAI(
                api_key=settings.GEMINI_API_KEY,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            ),
            "groq": AsyncOpenAI(
                api_key=settings.GROQ_API_KEY, base_url="https://api.groq.com/openai/v1"
            ),
            "openrouter": AsyncOpenAI(
                api_key=settings.OPENROUTER_API_KEY,
                base_url="https://openrouter.ai/api/v1",
            ),
        }

    async def complete(
        self, messages: list, trace_id: str, redis_client=None, supabase_client=None
    ) -> str:
        """Runs prompt completion through Gemini -> Groq -> OpenRouter with circuit breaker failovers."""
        chain = [
            ("gemini", "gemini-1.5-flash"),
            ("groq", "llama-3.1-70b-versatile"),
            ("openrouter", "mistralai/mistral-7b-instruct:free"),
        ]

        last_error = None
        for provider, provider_model in chain:
            # 1. Circuit Breaker check
            if redis_client:
                try:
                    await check_breaker(redis_client, provider)
                except CircuitBreakerOpen:
                    logger.warning(
                        f"Circuit breaker is OPEN for {provider}. Skipping to fallback."
                    )
                    continue

            # 2. Attempt API Call
            client = self._clients[provider]
            try:
                # 25 seconds timeout limit
                response = await asyncio.wait_for(
                    client.chat.completions.create(
                        model=provider_model,
                        messages=messages,
                        temperature=self.temperature,
                        max_tokens=self.max_tokens,
                    ),
                    timeout=25.0,
                )

                # Success - Record circuit reset
                if redis_client:
                    await record_success(redis_client, provider)

                # Log metrics to Supabase
                prompt_tokens = response.usage.prompt_tokens if response.usage else 0
                completion_tokens = (
                    response.usage.completion_tokens if response.usage else 0
                )

                if supabase_client:
                    repo = SupabaseRepository()
                    await repo.insert_audit_log(
                        supabase_client,
                        {
                            "approval_request_id": "00000000-0000-0000-0000-000000000000",
                            "tool_name": f"LLM_{provider}",
                            "input_payload": {
                                "model": provider_model,
                                "messages_count": len(messages),
                            },
                            "output_payload": {
                                "prompt_tokens": prompt_tokens,
                                "completion_tokens": completion_tokens,
                            },
                        },
                    )

                return response.choices[0].message.content

            except Exception as e:
                last_error = e
                logger.error(f"Provider {provider} failed with error: {str(e)}")
                if redis_client:
                    await record_failure(redis_client, provider)
                # Apply 1s backoff retry delay before shifting
                await asyncio.sleep(1.0)

        raise CircuitBreakerOpen(
            f"All LLM providers in chain failed. Last error: {str(last_error)}"
        )

    @property
    def _llm_type(self) -> str:
        return "custom_llm_adapter"

    def _format_messages(self, messages: List[BaseMessage]) -> List[Dict[str, str]]:
        formatted = []
        for msg in messages:
            role = "user"
            if msg.type == "system":
                role = "system"
            elif msg.type == "ai":
                role = "assistant"
            elif msg.type == "human":
                role = "user"
            formatted.append({"role": role, "content": msg.content})
        return formatted

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        formatted = self._format_messages(messages)
        coro = self.complete(formatted, trace_id="sync_run")
        response_text = _run_async(coro)

        message = AIMessage(content=response_text)
        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])

    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        formatted = self._format_messages(messages)
        response_text = await self.complete(formatted, trace_id="async_run")

        message = AIMessage(content=response_text)
        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])
