# TODOS

## 目标：优先部署上线，确保公网可访问并能跑通问答

## 1. 部署方案决策

- [ ] 确定后端部署平台：Render / Railway / Fly.io 任选其一，优先选最容易跑通的。
- [ ] 确定线上 LLM 方案：本地继续 Ollama，线上改用 OpenAI-compatible API 或其他 hosted LLM。
- [ ] 确定线上向量库方案：短期启动时重建索引，或使用持久化 Chroma / Qdrant / Pinecone / Supabase pgvector。
- [ ] 明确线上不会提交 SRD PDF、抽取文本、chunks、向量库等生成数据。

## 2. 后端生产化

- [ ] 抽象 LLM 调用层，让 FastAPI 可通过环境变量切换 `ollama` / `openai_compatible`。
- [ ] 增加线上 LLM 环境变量：`LLM_PROVIDER`、`OPENAI_BASE_URL`、`OPENAI_API_KEY`、`OPENAI_MODEL`。
- [ ] 为 FastAPI 增加生产启动说明：`uvicorn dnd5e_srd_rag.api:app --host 0.0.0.0 --port $PORT`。
- [ ] 配置 FastAPI CORS，允许本地前端和未来 Vercel 域名访问。
- [ ] 确认 `/health` 不依赖 Chroma、embedding 或 LLM，可用于部署健康检查。
- [ ] 确认 `/api/chat` 在后端依赖缺失时返回清晰错误，而不是 traceback。

## 3. 后端部署

- [ ] 准备 Render/Railway 后端部署配置和环境变量清单。
- [ ] 部署 FastAPI 后端。
- [ ] 验证线上 `/health` 可访问。
- [ ] 验证线上 `/api/chat` 可返回 answer + sources。
- [ ] 记录后端公网 URL，用于前端环境变量。

## 4. 前端部署

- [ ] 确认 Next.js 前端本地 `npm run lint` 和 `npm run build` 通过。
- [ ] 在 Vercel 创建前端项目，根目录指向 `web/`。
- [ ] 在 Vercel 设置 `NEXT_PUBLIC_API_BASE_URL` 为线上后端 URL。
- [ ] 部署 Next.js 前端。
- [ ] 验证公网前端能调用公网后端并展示 answer + sources。

## 5. 部署文档

- [ ] 在 `TIPS.md` 中补充后端部署命令和环境变量说明。
- [ ] 在 `TIPS.md` 中补充 Vercel 前端部署步骤。
- [ ] 在 `README.md` 中加入线上 demo 地址。

## 6. 上线后再做

- [ ] 美化 Next.js 聊天页面，优化 loading、error 和 sources 展示。
- [ ] 优化自动检索策略，避免用户手动选择 section。
- [ ] 增加流式响应，让体验更接近 ChatGPT。
- [ ] 增加本地开发脚本，简化常用命令。

## 7. RAG 质量优化

- [ ] 优化 chunk 边界，优先处理 Spells 和 Monsters。
- [ ] 增加条目级 subsection，例如 `Fire Bolt`、`Cleric`、`Grappled` 和怪物名称。
- [ ] 建立小型检索评估集，记录预期命中的页码和章节。
- [ ] 探索混合检索：BM25 关键词检索 + embedding 向量检索。
