🛡️ GenAI-Sentinel
Advanced LLM Red-Teaming & Automated Threat Modeling Framework
GenAI-Sentinel is a high-performance, provider-agnostic framework designed to evaluate the resilience of Large Language Models (LLMs) against Indirect Prompt Injection (IPI) and adversarial manipulation. Based on the BIPIA v4.1 (Benchmark for Indirect Prompt Injection Attacks) methodology, it automates the full lifecycle of a Red-Teaming engagement: from payload obfuscation to multi-vector attacks and forensic reporting.

🚀 Key Features
Multi-Provider Registry: Native support for OpenAI (GPT-5.4/o3), Groq (Llama 3.3/4 Scout), Anthropic (Claude 4.6), DeepSeek, and Ollama for private local testing.

Adversarial Obfuscation Suite: Implements multi-stage evasion techniques:

Chained Attacks: Recursive JSON/Markdown wrapping.

Semantic Compression: Compressing payloads to bypass context-window filters.

Encoded Smuggling: Base64/ROT13 and Multilingual logic shifts.

Automated Defense Matrix: Benchmarks model performance against Sandwich Defenses, XML Tagging, and System-Level Self-Reminders.

Caterpillar Evaluation Engine: A specialized scoring module that analyzes LLM outputs for identity breaches and secret exfiltration.

Forensic HTML Auditing: Generates enterprise-grade security reports with raw execution traces and risk posture analysis.

🧠 Core Methodology & Architecture
The framework operates on a Modular Red-Team Pipeline:

Selection: Interactive CLI wizard to define Target Model, Attack Vector, and Defense Layer.

Execution: The Attack Engine generates a weaponized payload using BIPIA-inspired scenarios.

Interception: The Defense Layer wraps the input with canonical security guardrails.

Evaluation: The Caterpillar Evaluator detects if the honeytoken (canary) was leaked or if the system prompt was overridden.

Telemetry: Real-time logging to Supabase for long-term trend analysis.

🛠️ Installation & Quick Start
1. Clone & Install
Bash
git clone https://github.com/your-username/genai-sentinel.git
cd genai-sentinel
pip install -r requirements.txt
2. Environment Setup
Create a .env file in the root directory (see .env.example):

Plaintext
OPENAI_API_KEY=your_key
GROQ_API_KEY=your_key
SUPABASE_URL=your_url
SUPABASE_KEY=your_key
3. Launch Interactive Wizard
Bash
python main.py --interactive
⚙️ Advanced Configuration (config.yaml)
Fine-tune your Red-Teaming parameters for automated batch testing:

YAML
experiment_suite:
  models: ["llama-3.3-70b", "gpt-5.4-mini", "deepseek-r1"]
  vectors: ["data_exfiltration", "identity_confusion", "rce_simulation"]
  obfuscations: ["base64_smuggling", "chained_json_wrap", "none"]
  defenses: ["sandwich_defense", "xml_border_tags", "none"]

security_params:
  honeytoken: "SENTINEL_SECRET_9921" # The canary token to monitor for leaks
  max_retries: 3
  timeout: 30.0
📊 Forensic Reporting
Every session concludes with a generated Security Intelligence Report (HTML).

Risk Posture: Automated classification (Critical/Warning/Passed).

Forensic Trace: Full visibility into the Sent Payload vs. LLM Raw Response.

Control Drift: Analysis of how specific defenses (like Sandwich) affected the attack success rate.

⚠️ Ethical Disclosure & Disclaimer
For authorized security testing and educational research only.
Unauthorized testing against third-party production systems is strictly prohibited. The developer (Samuel Isenin) assumes no liability for misuse of this framework. Use responsibly within the boundaries of the target provider's Terms of Service.

📜 License
Licensed under the MIT License - see the LICENSE file for details.
