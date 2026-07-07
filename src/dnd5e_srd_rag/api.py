"""
D&D SRD RAG 服务的 FastAPI 应用
FastAPI app for the D&D SRD RAG service.
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from dnd5e_srd_rag import config
from dnd5e_srd_rag.chat_service import answer_srd_question
from dnd5e_srd_rag.llm_answer import LLMAnswerError

# 创建 FastAPI 应用，http://127.0.0.1:8000/docs会展示以下内容
app = FastAPI(
    title="D&D SRD RAG API",
    version="0.1.0",
)

# 导入 CORS 配置，允许两个前端地址访问。
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://dnd5e-srd-rag.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 定义请求的形式， Field是校验规则，必须传，且规定格式。
# 如果不符合规则，FastAPI会自动返回422错误。比如top_k必须是1-20之间的整数，question不能为空字符串。
class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)
    top_k: int = Field(default=config.DEFAULT_TOP_K, ge=1, le=20)
    section: str | None = None # 可选section过滤，因为现在不是很准确。
    model: str | None = None # 可选model参数，默认使用后端配置的LLM模型。

# 溯源的形式
class SourceItem(BaseModel):
    label: str
    page: int | None = None
    section: str | None = None
    subsection: str | None = None

# 返回的形式
class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceItem]

# 检查接口健康
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

# chat API 接口
@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    # 调用 chat_with_srd 函数处理请求，具体 LLM provider 由后端配置决定。
    # 捕获 LLMAnswerError 异常，如果发生异常，返回503错误。
    try:
        result = answer_srd_question(
            question=request.question,
            top_k=request.top_k,
            section=request.section,
            model=request.model,
        )
    except LLMAnswerError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        ) from error

    return ChatResponse(**result)
