# Tips and Commands

## 中文

### 1. Python 环境

在项目根目录执行：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
```

如果 PowerShell 阻止激活脚本：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

复制后端环境变量模板：

```powershell
Copy-Item .env.example .env
```

### 2. 准备 PDF

把 SRD PDF 放到：

```text
data/raw/SRD_CC_v5.2.1.pdf
```

PDF 文件不提交到 Git。

### 3. 构建 RAG 数据

按顺序运行：

```powershell
.\.venv\Scripts\python.exe scripts\ingest_pdf.py
.\.venv\Scripts\python.exe scripts\annotate_sections.py
.\.venv\Scripts\python.exe scripts\chunk_pages.py
.\.venv\Scripts\python.exe scripts\inspect_chunks.py
.\.venv\Scripts\python.exe scripts\index_chunks.py --reset
```

脚本作用：

1. `ingest_pdf.py`：从 PDF 抽取每页文本和页码。
2. `annotate_sections.py`：根据 `section_map.py` 标注章节。
3. `chunk_pages.py`：把页面文本切成检索 chunks。
4. `inspect_chunks.py`：检查 chunk 长度、章节分布和异常内容。
5. `index_chunks.py --reset`：重新建立 Chroma 向量索引。

### 4. CLI 检索和问答

语义检索：

```powershell
.\.venv\Scripts\python.exe scripts\search.py "What does Fire Bolt do?" --top-k 3
```

按 section 过滤：

```powershell
.\.venv\Scripts\python.exe scripts\search.py "What does Fire Bolt do?" --section Spells --top-k 3
```

输出引用式上下文：

```powershell
.\.venv\Scripts\python.exe scripts\search_context.py "How does Cleric spellcasting work?" --top-k 3
```

本地 Ollama 问答：

```powershell
.\.venv\Scripts\python.exe scripts\chat_cli.py "What does Fire Bolt do?" --top-k 3
```

显示传给 LLM 的上下文：

```powershell
.\.venv\Scripts\python.exe scripts\chat_cli.py "What does Fire Bolt do?" --top-k 3 --show-context
```

Ollama 模型准备：

```powershell
ollama pull llama3.1:8b
ollama run llama3.1:8b
```

### 5. FastAPI 后端

启动 API：

```powershell
.\.venv\Scripts\python.exe -m uvicorn dnd5e_srd_rag.api:app --reload
```

常用地址：

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
POST http://127.0.0.1:8000/api/chat
```

请求示例：

```json
{
  "question": "What does Fire Bolt do?",
  "top_k": 5,
  "model": "llama3.1:8b"
}
```

如果 Ollama 没有运行，`/api/chat` 会返回 `503 Service Unavailable`，错误信息在 `detail` 字段中。

### 6. Next.js 前端

前端位于 `web/`。

第一次安装依赖：

```powershell
cd web
npm install
```

复制前端环境变量模板：

```powershell
Copy-Item .env.example .env.local
```

本地默认配置：

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

启动前端：

```powershell
npm run dev
```

浏览器打开：

```text
http://localhost:3000
```

本地开发需要同时运行：

```text
FastAPI: http://127.0.0.1:8000
Next.js: http://localhost:3000
```

### 7. 测试和检查

Python 测试：

```powershell
.\.venv\Scripts\python.exe -m pytest
```

前端 lint：

```powershell
cd web
npm run lint
```

### 8. 不要提交的内容

不要提交：

```text
data/raw/*.pdf
data/extracted/*
data/chunks/*
data/vectorstores/*
data/indexes/*
.env
.venv/
web/node_modules/
web/.next/
web/.env.local
```

可以提交：

```text
.env.example
web/.env.example
README.md
NOTICE.md
TIPS.md
src/
scripts/
tests/
web/app/
web/lib/
web/package.json
web/package-lock.json
```

---

## English

### 1. Python Environment

Run from the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
```

If PowerShell blocks activation scripts:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

Copy backend environment defaults:

```powershell
Copy-Item .env.example .env
```

### 2. Prepare the PDF

Place the SRD PDF at:

```text
data/raw/SRD_CC_v5.2.1.pdf
```

Do not commit the PDF.

### 3. Build RAG Data

Run in order:

```powershell
.\.venv\Scripts\python.exe scripts\ingest_pdf.py
.\.venv\Scripts\python.exe scripts\annotate_sections.py
.\.venv\Scripts\python.exe scripts\chunk_pages.py
.\.venv\Scripts\python.exe scripts\inspect_chunks.py
.\.venv\Scripts\python.exe scripts\index_chunks.py --reset
```

### 4. CLI Search and Ask

Semantic search:

```powershell
.\.venv\Scripts\python.exe scripts\search.py "What does Fire Bolt do?" --top-k 3
```

Citation-style context:

```powershell
.\.venv\Scripts\python.exe scripts\search_context.py "How does Cleric spellcasting work?" --top-k 3
```

Local Ollama answer:

```powershell
.\.venv\Scripts\python.exe scripts\chat_cli.py "What does Fire Bolt do?" --top-k 3
```

Prepare the Ollama model:

```powershell
ollama pull llama3.1:8b
ollama run llama3.1:8b
```

### 5. FastAPI Backend

Start the API:

```powershell
.\.venv\Scripts\python.exe -m uvicorn dnd5e_srd_rag.api:app --reload
```

Useful URLs:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
POST http://127.0.0.1:8000/api/chat
```

Example request:

```json
{
  "question": "What does Fire Bolt do?",
  "top_k": 5,
  "model": "llama3.1:8b"
}
```

If Ollama is not running, `/api/chat` returns `503 Service Unavailable` with a readable message in `detail`.

### 6. Next.js Frontend

The frontend lives in `web/`.

Install dependencies:

```powershell
cd web
npm install
```

Copy frontend environment defaults:

```powershell
Copy-Item .env.example .env.local
```

Start the frontend:

```powershell
npm run dev
```

Open:

```text
http://localhost:3000
```

Local development needs both services running:

```text
FastAPI: http://127.0.0.1:8000
Next.js: http://localhost:3000
```

### 7. Tests and Checks

Python tests:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Frontend lint:

```powershell
cd web
npm run lint
```

### 8. Do Not Commit

Do not commit generated data or local environments:

```text
data/raw/*.pdf
data/extracted/*
data/chunks/*
data/vectorstores/*
data/indexes/*
.env
.venv/
web/node_modules/
web/.next/
web/.env.local
```
