# dnd5e-srd-rag

## 中文

`dnd5e-srd-rag` 是一个基于 D&D Beyond 发布的 SRD v5.2.1 PDF 构建的本地 RAG 项目。它把 SRD PDF 处理成带版本、页码、章节和来源信息的检索索引，并提供 CLI、FastAPI 和 Next.js 聊天界面。

```text
PDF -> 文本抽取 -> 章节标注 -> chunk -> embedding -> Chroma 检索 -> LLM 回答 + sources
```

### 当前能力

- 抽取 SRD PDF 的文本和页码。
- 为 chunks 保留 SRD 版本、页码、section、subsection 和授权信息。
- 使用 `Qwen/Qwen3-Embedding-0.6B` 生成本地 embeddings。
- 使用 ChromaDB 建立本地向量索引。
- 使用 Ollama 本地 LLM 生成规则回答。
- 使用 FastAPI 暴露 `/api/chat`。
- 使用 Next.js 提供简易聊天界面。

### 快速入口

详细命令见 [TIPS.md](TIPS.md)。

常用入口：

- FastAPI: `http://127.0.0.1:8000`
- FastAPI docs: `http://127.0.0.1:8000/docs`
- Next.js UI: `http://localhost:3000`

### 项目结构

```text
dnd5e-srd-rag/
  data/                  # 本地 PDF、抽取文本、chunks、向量库，不提交生成内容
  scripts/               # 命令行工具：ingest、chunk、index、search、ask
  src/dnd5e_srd_rag/     # 后端核心包：RAG、retrieval、Ollama、FastAPI
  tests/                 # Python 测试
  web/                   # Next.js 前端
```

### 数据源与授权

- Source page: https://www.dndbeyond.com/srd
- Source PDF: https://media.dndbeyond.com/compendium-images/srd/5.2.1/SRD_CC_v5.2.1.pdf
- SRD version: 5.2.1
- Published date: 2025-05-01
- SRD content license: CC-BY-4.0

本仓库的 MIT License 仅覆盖本项目原创代码和文档，不重新授权 SRD 内容、PDF、抽取文本、chunks、embeddings 或向量库。更多归属和授权说明见 [NOTICE.md](NOTICE.md)。

### 当前限制

- 线上部署时不能直接假设存在本地 Ollama 和本地 Chroma 数据。
- FastAPI API 目前不是 streaming；`/api/chat` 会等待完整回答后返回 JSON。
- `subsection` 目前主要基于页级目录 map；同一页多个小标题时还不够精细。
- SRD PDF、抽取文本、chunks 和向量库不应提交到 Git。

---

## English

`dnd5e-srd-rag` is a local RAG project built from the D&D Beyond SRD v5.2.1 PDF. It turns the SRD PDF into a retrieval index with versioned, page-backed, section-aware sources, and exposes CLI tools, a FastAPI API, and a small Next.js chat UI.

```text
PDF -> text extraction -> section annotation -> chunking -> embeddings -> Chroma retrieval -> LLM answer + sources
```

### Current Features

- Extract SRD PDF text with page numbers.
- Preserve SRD version, page, section, subsection, and license metadata.
- Generate local embeddings with `Qwen/Qwen3-Embedding-0.6B`.
- Build a local ChromaDB vector index.
- Generate rules answers with a local Ollama LLM.
- Expose `/api/chat` with FastAPI.
- Provide a simple Next.js chat UI.

### Quick Links

Detailed commands are in [TIPS.md](TIPS.md).

Common local URLs:

- FastAPI: `http://127.0.0.1:8000`
- FastAPI docs: `http://127.0.0.1:8000/docs`
- Next.js UI: `http://localhost:3000`

### Project Structure

```text
dnd5e-srd-rag/
  data/                  # Local PDF, extracted text, chunks, vector stores; generated content is not committed
  scripts/               # CLI tools: ingest, chunk, index, search, ask
  src/dnd5e_srd_rag/     # Backend package: RAG, retrieval, Ollama, FastAPI
  tests/                 # Python tests
  web/                   # Next.js frontend
```

### Data Source and License

- Source page: https://www.dndbeyond.com/srd
- Source PDF: https://media.dndbeyond.com/compendium-images/srd/5.2.1/SRD_CC_v5.2.1.pdf
- SRD version: 5.2.1
- Published date: 2025-05-01
- SRD content license: CC-BY-4.0

The MIT License in this repository applies only to this project's original code and documentation. It does not relicense SRD content, PDFs, extracted text, chunks, embeddings, or vector indexes. See [NOTICE.md](NOTICE.md) for attribution and licensing notes.

### Current Limitations

- Online deployment cannot assume local Ollama or local Chroma data is available.
- The FastAPI API is not streaming yet; `/api/chat` waits for a full answer and returns JSON.
- `subsection` is still mostly based on a page-level table-of-contents map and is not fully item-level.
- SRD PDFs, extracted text, chunks, and vector stores should not be committed.
