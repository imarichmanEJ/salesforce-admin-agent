# SF Guide Agent

> Natural language → Salesforce implementation guide, tailored to your Org.

## Overview

SF Guide Agent takes a natural language use case and generates a step-by-step Salesforce implementation guide based on the actual Org environment.

Built on a **3-LLM Pipeline** where each LLM has a single responsibility:
- **Classifier** — classifies use case type + summarizes input
- **Planner** — queries Org metadata and decides features/implementation order
- **Generator** — reads required Skill files at runtime and generates the guide

---

## Architecture

```
User Input
    ↓
Classifier LLM        → use case type (6 categories) + one-line summary
    ↓
Planner LLM + Tools   → features + step order  /  Tools: Salesforce REST API · Tavily Search
    ↓
Generator LLM + read_skill Tool  → reads only required Skill files at runtime
    ↓
Implementation Guide (markdown)
```

**Skill files** are not injected into the system prompt — Generator calls `read_skill` tool to fetch only what it needs per step.

```
skills/
├── setup / layout / prompt / flow / apex / agent
└── prompt_type/
    ├── field_generation / flex / sales_email
```

---

## Tech Stack

| | |
|--|--|
| LLM | OpenAI GPT-4o · LangGraph · LangChain |
| Backend | FastAPI · Python |
| Salesforce | REST API · CLI · OAuth 2.0 Client Credentials |
| Search | Tavily Search API |
| Frontend | HTML · CSS · marked.js |

---

## Scope & Constraints

To ensure reliable output quality, the agent covers a defined set of implementation patterns:

| Type | Supported Variants |
|------|--------------------|
| Prompt Template | Field Generation · Flex · Sales Email |
| Flow | Record-Triggered · Screen · Template-Triggered · Scheduled |
| Others | Setup · Layout · Apex · Agent |

Salesforce Org: **25 standard objects** connected via REST API + CLI metadata pipeline.

---

## Challenges & Solutions

**1. Salesforce metadata access restriction**
`GenAiPromptTemplate` is not queryable via SOQL, Tooling API, or Connect REST API. Solved by automating `Salesforce CLI` as a subprocess to pull and parse XML metadata.

**2. Dynamic Org environment**
Each Org has a unique Object/Field structure. Planner LLM queries `get_objects()` / `describe_object()` at runtime instead of relying on static rules.

**3. Task decomposition for reliable output**
A single LLM handling all steps produced inconsistent results. Separated into Classifier → Planner → Generator, each with a dedicated role and prompt.

**4. Skill file dynamic reference**
Injecting all Skill files upfront caused token waste and quality degradation. Generator retrieves only the relevant files via `read_skill` tool call at runtime.

---

## Installation

```bash
git clone https://github.com/imarichmanEJ/salesforce-admin-agent.git
cd sf-guide-agent
pip install -r requirements.txt
cp .env.example .env  # fill in your credentials
uvicorn main:app --reload
```

**.env required:**
```
OPENAI_API_KEY
TAVILY_API_KEY
SALESFORCE_DOMAIN
SALESFORCE_CLIENT_ID
SALESFORCE_CLIENT_SECRET
```