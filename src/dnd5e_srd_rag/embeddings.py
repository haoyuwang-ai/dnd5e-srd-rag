"""
文本向量化工具。
Text embedding utilities.
"""

from __future__ import annotations

from collections.abc import Sequence

# 服务器不默认走本地。
# from sentence_transformers import SentenceTransformer

from dnd5e_srd_rag import config

# 走openai
from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI


class EmbeddingError(RuntimeError):
    """Raised when embeddings cannot be generated."""

# 缓存已加载的 embedding 模型，避免重复加载。
# _MODEL: SentenceTransformer | None = None
_MODEL = None

# sentence-transformers 模型，即 Qwen/Qwen3-Embedding-0.6B，后续可根据需要调整。
def get_local_embedding_model(
    model_name: str | None = None,
):
    """加载并缓存 本地 embedding 模型。"""
    global _LOCAL_MODEL

    if _LOCAL_MODEL is None:
        from sentence_transformers import SentenceTransformer

        try:
            _LOCAL_MODEL = SentenceTransformer(model_name)
        except Exception:
            _LOCAL_MODEL = SentenceTransformer(model_name, local_files_only=True)

    return _LOCAL_MODEL


# 把文本列表转换为 embedding 向量列表，即把我的jsonl中的text字段转换为向量，后续存储到 ChromaDB 中。
def embed_texts_local(
    texts: Sequence[str],
    model_name: str | None = None,
) -> list[list[float]]:
    """生成文本 embeddings。"""
    model = get_local_embedding_model(model_name)

    embeddings = model.encode(
        list(texts),
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    return embeddings.tolist()

# openai embedding
def embed_texts_openai(
    texts: Sequence[str],
    model: str = config.DEFAULT_OPENAI_EMBEDDING_MODEL,
    api_key: str | None = config.DEFAULT_OPENAI_API_KEY,
    base_url: str = config.DEFAULT_OPENAI_BASE_URL,
    timeout: float = 180,
) -> list[list[float]]:
    """Generate embeddings with an OpenAI-compatible embeddings API."""
    if not texts:
        return []

    if not api_key:
        raise EmbeddingError("OPENAI_API_KEY is required for OpenAI embeddings.")

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
        timeout=timeout,
    )

    try:
        response = client.embeddings.create(
            model=model,
            input=list(texts),
        )
    except APIConnectionError as error:
        raise EmbeddingError(
            f"Could not connect to OpenAI-compatible embeddings API at {base_url}."
        ) from error
    except APITimeoutError as error:
        raise EmbeddingError(
            f"OpenAI-compatible embeddings request timed out after {timeout} seconds. "
            f"Model: {model}."
        ) from error
    except APIStatusError as error:
        raise EmbeddingError(
            f"OpenAI-compatible embeddings API returned HTTP {error.status_code}. "
            f"Model: {model}. Response: {error.response.text}"
        ) from error

    return [item.embedding for item in response.data]


def embed_texts(
    texts: Sequence[str],
    model_name: str | None = None,
) -> list[list[float]]:
    """Generate text embeddings with the configured embedding provider."""
    provider = config.DEFAULT_EMBEDDING_PROVIDER.lower()

    if provider == "openai":
        return embed_texts_openai(
            texts,
            model=model_name or config.DEFAULT_OPENAI_EMBEDDING_MODEL,
        )

    if provider == "local":
        return embed_texts_local(
            texts,
            model_name=model_name or config.DEFAULT_LOCAL_EMBEDDING_MODEL,
        )

    raise EmbeddingError(
        f"Unsupported EMBEDDING_PROVIDER '{provider}'. "
        "Expected 'openai' or 'local'."
    )

# 把单个查询文本转换为 embedding 向量，就是我的问题。
def embed_query(
    query: str,
    model_name: str | None = None,
) -> list[float]:
    """生成查询 embedding。"""
    return embed_texts([query], model_name=model_name)[0]
