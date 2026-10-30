```markdown
# 产品智能助手

基于通义千问 + LangChain 的多工具 AI 应用：支持产品 PDF 知识库问答（RAG）、天气查询、多轮对话，以及上传 PDF 动态扩展知识库。提供 Streamlit 可视化界面，可本地一键演示。

## 功能特点

- **产品知识库问答**：PDF 解析 → 文本切分 → Chroma 向量检索（MMR）→ 大模型生成
- **天气查询工具**：根据城市查询当日天气
- **多轮对话**：保留上下文，支持连续追问
- **动态扩展知识库**：上传 PDF 即时入库，无需重启
- **防重复入库**：同一文件不会重复添加
- **Streamlit 界面**：侧边栏说明 + 对话区 + 历史记录 + 清空对话

## 技术栈

| 类别 | 技术 |
|------|------|
| 大模型 | 通义千问（OpenAI 兼容接口） |
| 框架 | LangChain（create_agent） |
| 向量库 | Chroma |
| 检索 | MMR（k=3, fetch_k=10） |
| 文档解析 | PyPDFium2 |
| 切分 | RecursiveCharacterTextSplitter（chunk_size=300, overlap=50） |
| 界面 | Streamlit |
| 其他 | python-dotenv, requests |

## 项目结构

```text
.
├── app.py                 # Streamlit 主程序（含 Agent 类）
├── produce.pdf            # 默认产品知识库文档
├── requirements.txt
├── .env.example
├── README.md
├── chroma_db/             # 向量库持久化目录
└── upload/                # 用户上传 PDF 存放目录
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`，填入你的 API Key：

```bash
QWEN_KEY=你的通义千问API密钥
```

### 3. 准备默认知识库

将产品说明 PDF 命名为 `produce.pdf` 放在项目根目录（或修改代码中的路径）。

### 4. 启动

```bash
streamlit run app.py
```

浏览器访问终端提示的本地地址即可。

## 使用说明

1. **产品咨询**：直接提问，例如「主摄像头是什么？像素和视频规格怎么样？」
2. **天气查询**：带上城市，例如「黄石今天天气怎么样？」
3. **扩展知识库**：在页面上传 PDF，提示「添加成功」后即可提问新文档内容
4. **清空对话**：点击「清空记录」同时清空界面历史与 Agent 记忆

## 实现要点

### 1. Agent 与工具路由
使用 LangChain `create_agent` 实现工具调用。模型根据用户问题自动选择：
- `search_product_knowledge`：产品相关
- `get_weather`：天气相关

### 2. RAG 流程
PDF 加载 → 切分（300/50）→ Embedding → Chroma 持久化 → MMR 检索 → 作为工具结果返回给模型生成回答。

### 3. 检索优化
- 切分从 chunk_size=500 调整为 300 后，块数量增加，MMR 召回更准
- 固定题评测中，优化后核心问题全部命中，且单块更短，有利于控制 token

### 4. 多轮对话
通过维护完整的 `messages` 列表（含 HumanMessage / AIMessage / ToolMessage），每次将完整历史传入 Agent，实现上下文记忆。

### 5. 与手写实现的对比
此前完成过手写版本（Function Calling + 自建 RAG + Streamlit），本项目用 LangChain 复现核心能力，便于理解「原理实现」与「框架复用」的差异。

## 简单评测结论

使用固定题目进行验证（产品参数、功能、天气、知识库外问题等）：

- 工具选择基本正确
- 知识库内问题在切分优化后命中率明显提升
- 知识库外问题能按提示拒绝编造
- 主要瓶颈仍是默认知识库规模；上传 PDF 可扩展覆盖范围

## 不足与后续计划

- 默认知识库较小，复杂问题仍受文档覆盖限制
- 界面以功能为主，美观度一般
- 尚未做云端部署与用户鉴权
- 后续可考虑：更规范的工程化结构、checkpointer 持久会话、简单部署上线

## 简历项目描述（可直接使用）

基于通义千问与 LangChain 的多工具智能助手：支持 PDF 知识库 RAG 问答、天气查询、多轮对话及上传 PDF 动态扩展知识库；完成检索参数与切分优化，并通过固定题评测验证效果；使用 Streamlit 提供可演示界面，覆盖大模型调用、工具编排、向量检索与基础工程化。

---

**作者**：转行学习中，目标 AI 应用工程师（黄石 / 鄂州周边）  
**关联作品**：手写版 Agent 见 [agent_app](https://github.com/hctc365853671/agent_app)
```