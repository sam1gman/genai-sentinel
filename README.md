# genai-sentinel
Automated LLM Threat Modeling &amp; Red-Teaming Framework based on BIPIA v4.1. Evaluates prompt injection resilience with advanced obfuscation and defense matrix scoring.
**LLM Security Evaluation Framework** — POC for automated prompt injection testing & guardrail evaluation.

## ⚠️ Ethical Use Only

- For **authorized internal testing** and **educational/research** purposes only
- Do not use against production systems without explicit written permission
- User is responsible for compliance with target provider ToS

## Features
- Multi-provider support (Groq, OpenAI, Anthropic, Ollama)
- Interactive CLI with model/attack selection
- BIPIA-inspired scenarios + obfuscation techniques
- Real-time scoring & telemetry
- Professional HTML audit reports

## 🧠 Core Methodology

### ⚔️ Attack Vectors (BIPIA v4.1)
- **Indirect Prompt Injection:** Scenarios where malicious instructions are hidden in external data.
- **Obfuscation Suite:** - `Base64/ROT13 Smuggling`: Encoding payloads to bypass static keyword filters.
    - `Multilingual Shift`: Wrapping attacks in low-resource languages.
    - `Chained Attack`: Recursive JSON wrapping + Semantic compression for maximum evasion.

### 🛡 Defense Matrix
Evaluates model resilience against:
- **Self-Reminder:** Internal instructions to maintain role.
- **Border Strings:** Explicit delimiters for untrusted content.
- **Sandwich Defense:** Dual-layer framing for high-priority instruction hierarchy.

## Quick Start
```bash
pip install -r requirements.txt
python main.py --interactive
```

## License
MIT — Educational/Research use only

## ⚙️ Configuration (`config.yaml`)
```yaml
models:
  - "openai/gpt-4o"
  - "groq/llama-3.3-70b-versatile"
attack_vectors: ["social_engineering", "data_exfiltration"]
obfuscations: ["generate_chained_attack", "base64_logic"]
defenses: ["sandwich_defense", "none"]
max_concurrent: 5
honeytoken: "REPLACE_WITH_YOUR_CANARY_TOKEN"
