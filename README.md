# 🛡️ GenAI-Sentinel
### **Advanced LLM Red-Teaming & Automated Threat Modeling Framework**

**GenAI-Sentinel** is a high-performance, provider-agnostic framework designed to evaluate the resilience of Large Language Models (LLMs) against **Indirect Prompt Injection (IPI)** and adversarial manipulation. 

Based on the **BIPIA v4.1** methodology, it automates the full Red-Teaming lifecycle: from payload obfuscation to multi-vector attacks and forensic reporting.

---

## 🚀 Key Features

* **🌐 Multi-Provider Registry**: Native support for **OpenAI (GPT-5.4/o3)**, **Groq (Llama 3.3)**, **Anthropic (Claude 4.6)**, **DeepSeek**, and **Ollama**.
* **🎭 Adversarial Obfuscation**: Implements **Chained Attacks**, **Semantic Compression**, and **Encoded Smuggling** (Base64/ROT13) to bypass guardrails.
* **🛡️ Defense Matrix**: Benchmarks performance against **Sandwich Defenses**, **XML Tagging**, and **System-Level Self-Reminders**.
* **🐛 Caterpillar Evaluation**: A specialized scoring module that detects identity breaches and secret exfiltration in real-time.
* **📊 Forensic Auditing**: Generates enterprise-grade HTML reports with full execution traces and risk posture analysis.

---

## 🧠 Core Methodology
The framework operates on a **Modular Red-Team Pipeline**:

| Stage | Component | Description |
| :--- | :--- | :--- |
| **1. Selection** | `Interactive CLI` | Define Target Model, Attack Vector, and Defense Layer. |
| **2. Execution** | `Attack Engine` | Generates weaponized payloads using BIPIA scenarios. |
| **3. Interception** | `Defense Layer` | Wraps input with canonical security guardrails. |
| **4. Evaluation** | `Caterpillar` | Detects honeytoken (canary) leaks or prompt overrides. |
| **5. Telemetry** | `Supabase` | Real-time logging for long-term trend analysis. |

---

## 🛠️ Installation & Quick Start

### 1. Clone & Install
```bash
git clone [https://github.com/your-username/genai-sentinel.git](https://github.com/your-username/genai-sentinel.git)
cd genai-sentinel
pip install -r requirements.txt
