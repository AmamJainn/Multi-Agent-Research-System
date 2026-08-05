# 🧠 Multi-Agent Research System

A fully autonomous, multi-agent AI research assistant built with **LangChain** and **Groq (Llama 3.3 70B)**. Give it a topic — a coordinated team of AI agents will **search the live web, scrape sources, write a structured report, and critique its own output** — all without a single line of manual research.

🔗 **Live Demo:** [multi-agent-research-system.streamlit.app](https://multi-agent-research-system-ea7hnsn9pb5fe93rtar8na.streamlit.app/)
📦 **Repo:** [github.com/AmamJainn/Multi-Agent-Research-System](https://github.com/AmamJainn/Multi-Agent-Research-System)

---

## 🚀 What Is This?

Instead of a single LLM answering from memory, this project deploys **four specialized agents** that collaborate through a shared pipeline — the same architecture pattern used in production-grade agentic AI systems:

| Agent | Role |
|---|---|
| 🔍 **Search Agent** | Uses the Tavily API to find recent, reliable sources on the web |
| 📖 **Reader Agent** | Scrapes and extracts clean text from the most relevant source |
| ✍️ **Writer Chain** | Synthesizes everything gathered into a structured, professional report |
| 🧐 **Critic Chain** | Reviews the report like a senior researcher — scores it and gives feedback |

Each agent shares information through a common `state` dictionary, forming a clean, linear multi-agent pipeline from raw topic → reviewed final report.

---

## 🏗️ Architecture

```
        You give a research topic
                  │
                  ▼
        ┌───────────────────┐        Tavily API
        │   Search Agent     │ ─────► (live web search)
        │ (AgentExecutor +   │ ◄─────
        │  web_search tool)  │
        └─────────┬──────────┘
                  │  state["search_results"]
                  ▼
        ┌───────────────────┐      BeautifulSoup
        │   Reader Agent     │ ─────► (scrapes page)
        │ (AgentExecutor +   │ ◄─────
        │  scrape_url tool)  │
        └─────────┬──────────┘
                  │  state["scraped_content"]
                  ▼
        ┌────────────────┬────────────────┐
        │  Writer Chain   │  Critic Chain  │
        └────────┬────────┴────────┬───────┘
                  │                 │
                  ▼                 ▼
              state["report"]  state["feedback"]
                  │                 │
                  └────────┬────────┘
                           ▼
                      Final Output
                 (shown in Streamlit UI)
```

---

## ✨ Features

- **Live web search** via the Tavily API — not stale training data
- **Real page scraping** with BeautifulSoup for deeper, factual context
- **LCEL pipelines** (`prompt | llm | StrOutputParser()`) for the Writer and Critic chains
- **Self-review loop** — the Critic Chain scores the report out of 10 with strengths and areas to improve
- **Streamlit UI** with tabs for the report, critic feedback, raw search results, and scraped content
- **Downloadable report** (Markdown) straight from the UI
- **Fast + free inference** powered by Groq's Llama 3.3 70B

---

## 🛠️ Tech Stack

- **LLM:** Llama 3.3 70B via [Groq](https://console.groq.com)
- **Orchestration:** LangChain (Agents + LCEL)
- **Web Search:** [Tavily API](https://tavily.com)
- **Scraping:** Requests + BeautifulSoup
- **UI:** Streamlit
- **Env Management:** python-dotenv

---

## 📂 Project Structure

```
Multi-Agent-Research-System/
├── app.py              # Streamlit UI — entry point for the web app
├── pipeline.py          # Orchestrator — runs all 4 agents in sequence
├── agents.py             # Defines the Search Agent, Reader Agent, Writer & Critic chains
├── tools_file.py          # Custom tools: web_searching_tool, url_scraping_tool
└── requirements.txt        # Python dependencies
```

---

## ⚙️ Setup & Installation

### 1. Clone the repo
```bash
git clone https://github.com/AmamJainn/Multi-Agent-Research-System.git
cd Multi-Agent-Research-System
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API keys
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

- Get a free Groq API key at [console.groq.com](https://console.groq.com)
- Get a free Tavily API key at [tavily.com](https://tavily.com)

---

## ▶️ Usage

### Run via terminal
```bash
python pipeline.py
```
Enter a topic when prompted, and watch all 4 agents work one by one — search, read, write, review — printed live in the terminal.

### Run the Streamlit UI
```bash
streamlit run app.py
```
Open the local URL Streamlit gives you, enter a research topic, and click **Run**.

---

## 📸 Example Output

Given a topic like *"Impact of quantum computing on cryptography"*, the pipeline produces:
- A list of live, cited sources
- Deep scraped content from the most relevant page
- A structured report (Introduction → Key Findings → Conclusion → Sources)
- A critic score out of 10 with strengths and areas to improve

---

## 🗺️ Roadmap / Ideas for Extension

- [ ] Support scraping multiple URLs instead of just the top one
- [ ] Add a vector store (FAISS) for long-context research memory
- [ ] Swap in `langgraph` for a more robust stateful pipeline
- [ ] Add PDF export for the final report
- [ ] Support multiple LLM providers (Gemini, Mistral) as fallback

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙌 Acknowledgements

Built using [LangChain](https://www.langchain.com/), [Groq](https://groq.com/), [Tavily](https://tavily.com/), and [Streamlit](https://streamlit.io/).
