# 🧠 AI Research Assistant Agent

This is an intelligent research assistant powered by large language models and LangChain agents. It can research a topic using web and Wikipedia tools, summarize findings, and optionally save them to a file in a clean, structured format.

---

## 🚀 Features

- Uses multiple LLM providers (`OpenAI`, `Anthropic`, `Gemini`) via LangChain.
- Integrates web search (DuckDuckGo) and Wikipedia for accurate information.
- Responds with structured JSON matching a Pydantic schema.
- Automatically saves results to a `.txt` file when prompted.
- Designed for command-line interaction with verbose agent logging.

---

## 📁 Project Structure

.
├── main.py # Main script to run the agent
├── tools.py # Custom tools like search, wiki, and save_to_txt
├── requirements.txt # Python dependencies
├── .env # Environment variables (API keys, etc.)
└── README.md # This file
