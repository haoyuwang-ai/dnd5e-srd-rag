"""
LLM 回答工具。
LLM answer utilities.

当前实现使用本地 Ollama，后续可扩展为 OpenAI-compatible provider。
The current implementation uses local Ollama and can be extended to
OpenAI-compatible providers later.
"""

from __future__ import annotations

from typing import Any

import httpx

from dnd5e_srd_rag import config
from dnd5e_srd_rag.retrieval import format_source, preview_text

from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI

# 命名异常类
class LLMAnswerError(RuntimeError):
    """Raised when the configured LLM provider cannot generate an answer."""
    pass

# 把检索到的 records 组装成给 LLM 使用的上下文。
def build_context(
    records: list[dict[str, Any]],
    max_chars_per_chunk: int = 1200,
) -> str:
    context_parts = []

    for index, record in enumerate(records, start=1):
        source = format_source(record["metadata"])
        text = preview_text(record["text"], limit=max_chars_per_chunk)

        context_parts.append(
            f"[{index}] Source: {source}\n"
            f"{text}"
        )

    return "\n\n".join(context_parts)


# 构建 Ollama /api/chat 需要的 messages。
def build_messages(
    question: str,
    records: list[dict[str, Any]],
) -> list[dict[str, str]]:
    context = build_context(records)

    system_message = (
        "You are a careful Dungeons & Dragons SRD rules assistant. "
        "Answer only from the provided SRD context. "
        "Do not use outside rules, house rules, or unsupported assumptions. "
        "If the context does not contain enough information, say that the current SRD context does not answer the question. "
        "Do not write citations or a Sources section; the application will attach sources separately."
    )

    user_message = (
        "SRD context:\n"
        f"{context}\n\n"
        "Question:\n"
        f"{question}\n\n"
        "Answer with only a concise rules explanation."
    )

    return [
        {
            "role": "system",
            "content": system_message,
        },
        {
            "role": "user",
            "content": user_message,
        },
    ]


# 调用本地 Ollama /api/chat，让 LLM 基于检索上下文生成回答。
def answer_with_ollama(
    question: str,
    records: list[dict[str, Any]],
    model: str = config.DEFAULT_OLLAMA_MODEL,
    base_url: str = config.DEFAULT_OLLAMA_BASE_URL,
    timeout: float = 180,
) -> str:
    if not records:
        return "I could not find relevant SRD context for this question."

    messages = build_messages(question, records)

    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
    }

    url = f"{base_url.rstrip('/')}/api/chat"

    try:
        response = httpx.post(
            url,
            json=payload,
            timeout=timeout,
        )
        response.raise_for_status()
    except httpx.ConnectError as error:
        raise LLMAnswerError(
            f"Could not connect to Ollama at {base_url}. "
            "Make sure Ollama is installed and running. "
            "You can test it with: ollama --version"
        ) from error
    except httpx.TimeoutException as error:
        raise LLMAnswerError(
            f"Ollama request timed out after {timeout} seconds. "
            f"The model '{model}' may still be loading or may be too slow for this machine."
        ) from error
    except httpx.HTTPStatusError as error:
        response_text = error.response.text
        raise LLMAnswerError(
            f"Ollama returned HTTP {error.response.status_code} from {url}. "
            f"Model: {model}. Response: {response_text}"
        ) from error
    except httpx.HTTPError as error:
        raise LLMAnswerError(
            f"Ollama request failed: {error}"
        ) from error

    try:
        data = response.json()
    except ValueError as error:
        raise LLMAnswerError(
            f"Ollama returned a non-JSON response from {url}: {response.text}"
        ) from error

    answer = data.get("message", {}).get("content")
    if not answer:
        raise LLMAnswerError(
            f"Ollama response did not contain message.content: {data}"
        )

    return answer.strip()

# 调用 OpenAI-compatible API 让 LLM 基于检索上下文生成回答。
def answer_with_openai_compatible(
    question: str,
    records: list[dict[str, Any]],
    model: str = config.DEFAULT_OPENAI_MODEL,
    base_url: str = config.DEFAULT_OPENAI_BASE_URL,
    api_key: str | None = config.DEFAULT_OPENAI_API_KEY,
    timeout: float = 180,
) -> str:
    """Generate an answer with an OpenAI-compatible chat completions API."""
    if not records:
        return "I could not find relevant SRD context for this question."

    if not api_key:
        raise LLMAnswerError("OPENAI_API_KEY is required for openai_compatible LLM.")

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
        timeout=timeout,
    )

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=build_messages(question, records),
        )
    except APIConnectionError as error:
        raise LLMAnswerError(
            f"Could not connect to OpenAI-compatible API at {base_url}."
        ) from error
    except APITimeoutError as error:
        raise LLMAnswerError(
            f"OpenAI-compatible request timed out after {timeout} seconds. "
            f"Model: {model}."
        ) from error
    except APIStatusError as error:
        raise LLMAnswerError(
            f"OpenAI-compatible API returned HTTP {error.status_code}. "
            f"Model: {model}. Response: {error.response.text}"
        ) from error

    if not completion.choices:
        raise LLMAnswerError("no choices returned from OpenAI-compatible API.")

    answer = completion.choices[0].message.content
    if not answer:
        raise LLMAnswerError(
            f"OpenAI-compatible response did not contain choices[0].message.content: {completion}"
        )

    return answer.strip()

# answer入口
def answer_with_llm(
    question: str,
    records: list[dict[str, Any]],
    model: str | None = None,
) -> str:
    """Generate an answer with the configured LLM provider."""
    provider = config.DEFAULT_LLM_PROVIDER.lower()

    if provider == "openai_compatible":
        return answer_with_openai_compatible(
            question=question,
            records=records,
            model=model or config.DEFAULT_OPENAI_MODEL,
            base_url=config.DEFAULT_OPENAI_BASE_URL,
            api_key=config.DEFAULT_OPENAI_API_KEY,)
    elif provider == "ollama":
        return answer_with_ollama(
            question=question,
            records=records,
            model=model or config.DEFAULT_OLLAMA_MODEL,
            base_url=config.DEFAULT_OLLAMA_BASE_URL,
        )
    else:
        raise LLMAnswerError(
            f"Unsupported LLM provider: {provider}. "
            "Supported providers are: 'ollama', 'openai_compatible'."
        )