# TODO

## 下一步

- [ ] 优化自动检索策略，避免用户手动选择 section。
- [ ] 美化 Next.js 聊天页面，优化 loading、error 和 sources 展示。
- [ ] 设计线上 LLM 方案：本地继续 Ollama，线上改用 OpenAI-compatible API 或其他 hosted LLM。
- [ ] 抽象 LLM 调用层，让 FastAPI 可通过环境变量切换 `ollama` / `openai_compatible`。
- [ ] 设计线上向量库方案：启动时重建索引、持久化 Chroma，或迁移到 Qdrant/Pinecone/Supabase pgvector。

## RAG 质量

- [ ] 优化 chunk 边界，优先处理 Spells 和 Monsters。
- [ ] 增加条目级 subsection，例如 `Fire Bolt`、`Cleric`、`Grappled` 和怪物名称。
- [ ] 建立小型检索评估集，记录预期命中的页码和章节。
- [ ] 探索混合检索：BM25 关键词检索 + embedding 向量检索。

## 部署

- [ ] 为 FastAPI 增加生产启动说明：`uvicorn dnd5e_srd_rag.api:app --host 0.0.0.0 --port $PORT`。
- [ ] 配置 FastAPI CORS，允许本地前端和未来 Vercel 域名访问。
- [ ] 准备 Render/Railway 后端部署配置和环境变量清单。
- [ ] 准备 Vercel 前端部署配置，设置 `NEXT_PUBLIC_API_BASE_URL`。
- [ ] 部署后验证 `/health` 和 `/api/chat`。

## 后续

- [ ] 增加流式响应，让体验更接近 ChatGPT。
- [ ] 增加本地开发脚本，简化常用命令。
