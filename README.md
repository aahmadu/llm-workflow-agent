# LLM Workflow Agent

This project implements a lightweight automation agent that uses GPT‑4 to process text inputs and return structured outputs.  
It is built with FastAPI and the OpenAI API.

Example use-case: triage inbound emails, summarize documents, classify messages, generate follow-up responses — all via a simple API.

---

## Features

✅ FastAPI server with `/run-agent` route  
✅ Calls GPT‑4 to process input text  
✅ Returns structured JSON output  
✅ Easily extensible to integrate with email, Airtable, Slack, and other APIs

---

## Installation

Clone the repo:

```bash
git clone https://github.com/your-username/llm-workflow-agent.git
cd llm-workflow-agent
```

Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Setup

1. Copy the `.env.example` file:
    

```bash
cp .env.example .env
```

2. Add your OpenAI API key to `.env`:
    

```
OPENAI_API_KEY=sk-xxxxxx
```
