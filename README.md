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

## 🧠 Core Methodology & Architecture
The framework operates on a **Modular Red-Team Pipeline**:

| Stage | Component | Description |
| :--- | :--- | :--- |
| **1. Selection** | `Interactive CLI` | Define Target Model, Attack Vector, and Defense Layer. |
| **2. Execution** | `Attack Engine` | Generates weaponized payloads using BIPIA scenarios. |
| **3. Interception** | `Defense Layer` | Wraps input with canonical security guardrails. |
| **4. Evaluation** | `Caterpillar` | Detects honeytoken (canary) leaks or prompt overrides. |
| **5. Telemetry** | `Supabase` | Real-time logging for long-term trend analysis. |

---

## 🔍 Technical Deep-Dive

### ⚔️ The Attack Engine (BIPIA v4.1)
Unlike simple prompt overrides, GenAI-Sentinel simulates **Indirect Prompt Injection**. It masks malicious instructions within "untrusted data" (e.g., a simulated email or search result). The engine supports:
* **Recursive Obfuscation**: Wrapping payloads in multiple layers (Base64 -> JSON -> Markdown).
* **Multilingual Shifts**: Leveraging low-resource languages to bypass English-centric safety filters.

### 🛡️ Defense Verification
The framework evaluates three primary defensive architectural patterns:
1. **Sandwich Defense**: Encapsulating user input between high-priority system instructions.
2. **XML/Delimiter Tagging**: Explicitly marking data boundaries to prevent instruction leakage.
3. **Instructional Self-Reminders**: Dynamic reinforcement of the model's core identity during the inference pass.

### 📈 Forensic Reporting & Telemetry
Every execution is recorded with full **Forensic Traceability**. The generated HTML reports include:
* **Sent Payload vs. Raw Response**: Side-by-side comparison for manual audit.
* **Compliance Scoring**: Automated 0.0-1.0 score based on the model's ability to maintain its original System Prompt.

---

## 🛠️ Installation & Quick Start

### 1. Clone & Install
```bash
git clone [https://github.com/your-username/genai-sentinel.git](https://github.com/your-username/genai-sentinel.git)
cd genai-sentinel
pip install -r requirements.txt
