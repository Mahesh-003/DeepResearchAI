\# 🔬 DeepResearch AI



An AI-powered research assistant that uses Large Language Models (LLMs), multi-agent workflows, RAG, MCP tools, memory, and Flask to automate the research process.



\## ✨ Features



\- 🧠 AI-powered research planning

\- 🔎 Automated research workflow

\- 🤖 LLM-based multi-agent architecture

\- 📚 Research knowledge base

\- 🔗 Retrieval-Augmented Generation (RAG)

\- 🛠️ Model Context Protocol (MCP) integration

\- 🧮 Calculator and research tools

\- 💾 Research knowledge storage

\- 🧠 Conversation memory

\- 🌐 Flask-based web interface

\- 🎨 ChatGPT-inspired user interface

\- 🔐 Secure API-key management using environment variables



\---



\## 🏗️ System Architecture



```text

&#x20;                   ┌─────────────────────┐

&#x20;                   │        USER         │

&#x20;                   │   Research Query    │

&#x20;                   └──────────┬──────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌─────────────────────┐

&#x20;                   │     Flask Web App   │

&#x20;                   │   HTML/CSS/JS UI    │

&#x20;                   └──────────┬──────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌─────────────────────┐

&#x20;                   │   Research Planner  │

&#x20;                   │        Agent        │

&#x20;                   └──────────┬──────────┘

&#x20;                              │

&#x20;            ┌─────────────────┼─────────────────┐

&#x20;            ▼                 ▼                 ▼

&#x20;     ┌─────────────┐   ┌─────────────┐   ┌─────────────┐

&#x20;     │  Research   │   │     RAG     │   │   Memory    │

&#x20;     │    Agent    │   │    Agent    │   │    Agent    │

&#x20;     └──────┬──────┘   └──────┬──────┘   └─────────────┘

&#x20;            │                 │

&#x20;            ▼                 ▼

&#x20;     ┌─────────────┐   ┌─────────────┐

&#x20;     │ MCP Tools   │   │ Knowledge   │

&#x20;     │             │   │    Base     │

&#x20;     │ • Calculate │   │    JSON     │

&#x20;     │ • Search    │   │             │

&#x20;     └──────┬──────┘   └─────────────┘

&#x20;            │

&#x20;            └──────────────┬──────────────┘

&#x20;                           ▼

&#x20;                   ┌─────────────────────┐

&#x20;                   │    Report Agent     │

&#x20;                   └──────────┬──────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌─────────────────────┐

&#x20;                   │  Research Findings  │

&#x20;                   └─────────────────────┘

