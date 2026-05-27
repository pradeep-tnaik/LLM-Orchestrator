
# 🤖 Multi-LLM AI Moderator Orchestrator

A lightweight, asynchronous Python dashboard designed for rapid product R&D and strategic analysis. This tool allows users to query multiple foundational LLMs (ChatGPT and Claude) simultaneously and synthesize their unique perspective strengths into a single, cohesive Master Blueprint document.

---

## 💡 Key Architectural Features

- **Parallel Execution Pipeline:** Powered by `trio` to handle asynchronous HTTP requests concurrently, reducing API response times by up to 50%.
- **Universal Abstraction Layer:** Implements `litellm` to easily swap out or append foundational models using an intuitive, standardized prompt routing payload.
- **Granular Perspective Control:** Dynamically toggle specific models on or off via interactive UI checkboxes depending on your current analytical scope.
- **Synthesis Engine Selection:** Choose which core engine handles the final blending process—leveraging ChatGPT's high-empathy customer framing or Claude's rigorous technical system analysis.
- **Secure Runtime Credential Handling:** API keys are injected on-the-fly directly inside the browser session UI, preventing accidental token leakage or environmental exposure.

---

## 🏗️ The Orchestration Workflow

```text
                  ┌────────────────────────┐
                  │   User Product Input   │
                  └───────────┬────────────┘
                              ▼
                 ┌──────────────────────────┐
                 │  Asynchronous Nursery    │
                 └──────┬────────────┬──────┘
                        │            │
      ┌─────────────────┘            └─────────────────┐
      ▼                                                ▼
┌───────────┐                                    ┌───────────┐
│  ChatGPT  │                                    │  Claude   │
│ (gpt-4o)  │                                    │ (sonnet)  │
└─────┬─────┘                                    └─────┬─────┘
      │                                                │
      └─────────────────┐            ┌─────────────────┘
                        ▼            ▼
                 ┌──────────────────────────┐
                 │ Dynamic Synthesis Engine │
                 └───────────┬──────────────┘
                             ▼
                 🏆 Unified Master Blueprint
```

---

## 🛠️ Local Installation & Setup

### 1. Prerequisites
Ensure you have Git and Python 3.10+ installed on your system machine.

### 2. Clone the Workspace Repository
```bash
git clone https://github.com
cd LLM-Orchestrator
```

### 3. Install Dependencies
Force package registrations into your operational runner binary directly:
```bash
python -m pip install streamlit litellm trio
```

### 4. Execute the Application Terminal Dashboard
```bash
python -m streamlit run "import streamlit as st.py"
```

---

## 🔑 Secure Credential Requirements

> [!CAUTION]
> **Security Notice:** Do not hardcode your private developer platform API keys anywhere inside the code. This app uses dynamic runtime form-mask inputs in the sidebar layout to protect your API parameters securely.

To power the background requests, make sure you have loaded minimal developer credits into your respective consoles:
- **OpenAI Platform Keys:** Available at [://openai.com](https://://openai.com)
- **Anthropic Console Keys:** Available at [://anthropic.com](https://://anthropic.com)

---

## 📄 License
This architecture is distributed for independent research, educational tracking, and rapid platform optimization. Open-source under the MIT License framework.
