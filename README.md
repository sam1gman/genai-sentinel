# 🛡️ GenAI-Sentinel
### **Advanced LLM Red-Teaming & Automated Threat Modeling Framework**

**GenAI-Sentinel** is a high-performance, provider-agnostic framework designed to evaluate the resilience of Large Language Models (LLMs) against **Indirect Prompt Injection (IPI)** and adversarial manipulation. 

Based on the **BIPIA v4.1** methodology, it automates the full Red-Teaming lifecycle: from payload obfuscation to multi-vector attacks and forensic reporting.

---

## 🚀 Key Features

* **🌐 Multi-Provider Registry**: Native support for **OpenAI (GPT-5.4/o3)**, **Groq (Llama 3.3)**, **Anthropic (Claude 4.6)**, **DeepSeek**, and **Ollama**.
* **🎭 Adversarial Obfuscation**: Implemented **Chained Attacks**, **Semantic Compression**, and **Encoded Smuggling**.
* **🛡️ Defense Matrix**: Benchmarks performance against **Sandwich Defenses**, **XML Tagging**, and **System-Level Self-Reminders**.
* **🐛 Caterpillar Evaluation**: A specialized scoring module that detects identity breaches and secret exfiltration in real-time.
* **📊 Forensic Auditing**: Generates enterprise-grade HTML reports with full execution traces.

---

## 🧠 Project Architecture Overview

The framework is built with a decoupled, modular architecture to ensure scalability and ease of integration:

| Component | Directory | Description |
| :--- | :--- | :--- |
| **Orchestrator** | `main.py` | The main entry point. Coordinates the UI, Attack Engine, and Evaluator. |
| **Attack Engine** | `attack_engine/` | Logic for generating BIPIA-based scenarios and weaponized payloads. |
| **Defense Matrix** | `defenses/` | Implementation of security guardrails (Sandwich, XML, Border Strings). |
| **Model Registry** | `core/` | Centralized management of LLM providers, API keys, and model specs. |
| **Evaluator** | `evaluator/` | The "Caterpillar" engine that scores model compliance and detects leaks. |
| **Reporter** | `reporter/` | Logic for generating the stylized forensic HTML security reports. |
| **UI/UX** | `ui/` | Interactive CLI components and terminal formatting (Rich-based). |

---

## ⚔️ Attack & Obfuscation Techniques

### 1. Indirect Prompt Injection (BIPIA 4.1)
The engine simulates attacks where malicious instructions are hidden in external data sources (e.g., a customer email or a search snippet).
* **Identity Confusion**: Forcing the model to abandon its role (e.g., "You are now a Linux Terminal").
* **Data Exfiltration**: Attempting to trick the model into revealing its internal `honeytoken`.

### 2. Obfuscation Suite
To bypass keyword-based filters and simple guardrails:
* **Base64/ROT13 Smuggling**: Encoding the attack string to hide malicious intent from static scanners.
* **Chained JSON Wrapping**: Nesting the attack within complex data structures to confuse the model's instruction priority.
* **Semantic Compression**: Shortening the attack to its core logical components to maximize impact within the context window.

---

## 🛡️ Defense Mechanisms

GenAI-Sentinel tests the effectiveness of current LLM hardening patterns:

* **Sandwich Defense**: Positioning the user input between two layers of high-priority system instructions.
* **XML Border Tags**: Wrapping untrusted input in strict XML tags (e.g., `<user_input>...</user_input>`) to prevent the model from treating it as an instruction.
* **Instructional Reinforcement**: Periodically re-injecting core safety constraints into the prompt to prevent "drift" during long responses.

---

## 🛠️ Installation & Setup

### 1. Clone & Install
```bash
git clone https://github.com/your-username/genai-sentinel.git
cd genai-sentinel
pip install -r requirements.txt
```

### 2. Environment Configuration
Create a .env file in the root directory to manage your API credentials:
```bash
# .env example
# ── OpenAI ───────────────────────────────────────────────────────────
OPENAI_API_KEY=your_openai_key_here
# ── Groq (free inference) ────────────────────────────────────────────
GROQ_API_KEY=your_groq_key_here
# ── Anthropic ────────────────────────────────────────────────────────
ANTHROPIC_API_KEY=your_anthropic_key_here
# ── Ollama (local inference) ────────────────────────────────────────
OLLAMA_BASE_URL=http://localhost:11434/v1
# ── Alice Honeytoken ──────────────────────────────────────────────
ALICE_HONEYTOKEN=REPLACE_WITH_YOUR_SECRET_TOKEN
```
### Or

Copy the example environment file and fill in your API credentials:
```bash
cp env.example .env
```


### 3. Launching the Wizard
Run the main script to start the interactive Red-Teaming session:

```bash
python main.py --interactive 
```

---

## ⚠️ Ethical Disclosure
For authorized security testing and research only. The developer assumes no liability for misuse of this tool. Use responsibly and only within the boundaries of the target provider's Terms of Service and legal frameworks.

---

## 📜 License
Licensed under the MIT License.
