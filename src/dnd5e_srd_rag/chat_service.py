"""
供 API 和未来 UI 使用的 RAG 问答服务
RAG chat service used by API and future UI
"""

from __future__ import annotations

from typing import Any

from dnd5e_srd_rag import config
from dnd5e_srd_rag.llm_answer import answer_with_llm
from dnd5e_srd_rag.retrieval import retrieve_chunks, format_source

# 引用溯源，并且格式化，有利于后续前端输出。
def build_source_items(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build structured source items from retrieved records."""
    source_items = []
    seen = set()

    for record in records:
        metadata = record["metadata"]

        label = format_source(metadata)
        page = metadata.get("page")
        section = metadata.get("section")
        subsection = metadata.get("subsection")

        source_key = (
            page,
            section,
            subsection,
            label,
        )

        if source_key in seen:
            continue

        seen.add(source_key)

        source_items.append(
            {
                "label": label,
                "page": page,
                "section": section,
                "subsection": subsection,
            }
        )

    return source_items

# 回答问题，检索 SRD chunks，调用 LLM 生成回答，并返回回答和溯源。
def answer_srd_question(
    question: str,
    top_k: int = config.DEFAULT_TOP_K,
    section: str | None = None,
    model: str | None = None,
) -> dict[str, Any]:
    """Retrieve SRD chunks, ask the configured LLM provider, and return answer plus deterministic sources."""
    records = retrieve_chunks(
        question,
        top_k=top_k,
        section=section,
    )

    answer = answer_with_llm(
        question=question,
        records=records,
        model=model,
    )

    return {
        "answer": answer,
        "sources": build_source_items(records),
    }