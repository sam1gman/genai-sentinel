"""
core/model_registry.py — Provider-agnostic Model Registry for GenAI-Sentinel.
Updated: March 29, 2026.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

Provider = Literal["openai", "groq", "anthropic", "together", "mistral", "ollama", "deepseek"]

@dataclass(frozen=True)
class ModelSpec:
    model_id: str
    display_name: str
    provider: Provider
    context_window: int
    rpm_limit: int  
    supports_system: bool = True
    is_free: bool = False
    is_reasoning: bool = False  

MODEL_REGISTRY: dict[str, ModelSpec] = {
    # ── Groq (Ultra-Low Latency - 2026 Production) ──────────────────────────
    "llama-3.3-70b": ModelSpec(
        model_id="llama-3.3-70b-versatile",
        display_name="Llama 3.3 70B (Groq)",
        provider="groq",
        context_window=131_072,
        rpm_limit=30,
        is_free=True,
    ),
    "gpt-oss-120b": ModelSpec(
        model_id="openai/gpt-oss-120b",
        display_name="GPT-OSS 120B (Groq)",
        provider="groq",
        context_window=131_072,
        rpm_limit=30,
        is_free=True,
    ),
    "llama-4-scout": ModelSpec(
        model_id="meta-llama/llama-4-scout-17b-16e-instruct",
        display_name="Llama 4 Scout (Preview)",
        provider="groq",
        context_window=131_072,
        rpm_limit=15,
        is_free=True,
    ),
    "qwen3-32b": ModelSpec(
        model_id="qwen/qwen3-32b",
        display_name="Qwen 3 32B (Groq)",
        provider="groq",
        context_window=131_072,
        rpm_limit=30,
        is_free=True,
    ),

    # ── OpenAI (Flagship 2026) ────────────────────────────────────────────────
    "gpt-5.4-pro": ModelSpec(
        model_id="gpt-5.4-pro",
        display_name="GPT-5.4 Pro",
        provider="openai",
        context_window=1_000_000,
        rpm_limit=500,
    ),
    "gpt-5.4-mini": ModelSpec(
        model_id="gpt-5.4-mini",
        display_name="GPT-5.4 Mini",
        provider="openai",
        context_window=400_000,
        rpm_limit=1000,
    ),
    "o3-reasoning": ModelSpec(
        model_id="o3",
        display_name="OpenAI o3 (Reasoning)",
        provider="openai",
        context_window=200_000,
        rpm_limit=100,
        is_reasoning=True,
    ),

    # ── Anthropic (Series 4.6) ────────────────────────────────────────────────
    "claude-4-6-sonnet": ModelSpec(
        model_id="claude-4-6-sonnet-20260215",
        display_name="Claude 4.6 Sonnet",
        provider="anthropic",
        context_window=1_000_000,
        rpm_limit=100,
    ),
    "claude-4-6-opus": ModelSpec(
        model_id="claude-4-6-opus-20260205",
        display_name="Claude 4.6 Opus",
        provider="anthropic",
        context_window=1_000_000,
        rpm_limit=50,
        is_reasoning=True,
    ),
    "claude-4-5-haiku": ModelSpec(
        model_id="claude-4-5-haiku-20251015",
        display_name="Claude 4.5 Haiku",
        provider="anthropic",
        context_window=200_000,
        rpm_limit=200,
    ),

    # ── DeepSeek (Direct API) ─────────────────────────────────────────────────
    "deepseek-v3.2": ModelSpec(
        model_id="deepseek-chat",
        display_name="DeepSeek V3.2",
        provider="deepseek",
        context_window=128_000,
        rpm_limit=100,
    ),
    "deepseek-r1": ModelSpec(
        model_id="deepseek-reasoner",
        display_name="DeepSeek R1 (Reasoning)",
        provider="deepseek",
        context_window=128_000,
        rpm_limit=60,
        is_reasoning=True,
    ),

    # ── Ollama (Local & Private) ──────────────────────────────────────────────
    "llama3.2-local": ModelSpec(
        model_id="llama3.2",
        display_name="Llama 3.2 (Local)",
        provider="ollama",
        context_window=128_000,
        rpm_limit=0,
        is_free=True,
    ),
}

def get_by_provider(provider: Provider) -> list[ModelSpec]:
    return [spec for spec in MODEL_REGISTRY.values() if spec.provider == provider]

def get_free_models() -> list[ModelSpec] :
    return [spec for spec in MODEL_REGISTRY.values() if spec.is_free]

def _guess_provider(model_id: str) -> Provider:
    m = model_id.lower()
    if any(k in m for k in ["gpt", "o1", "o3", "o5"]): return "openai"
    if "claude" in m: return "anthropic"
    if "deepseek" in m: return "deepseek"
    if any(k in m for k in ["llama", "qwen", "oss", "gemma"]): return "groq"
    if "/" in model_id: return "together"
    return "openai"

def resolve(model_key: str) -> ModelSpec:
    # Registry (case-insensitive)
    for key, spec in MODEL_REGISTRY.items():
        if key.lower() == model_key.lower() or spec.model_id.lower() == model_key.lower():
            return spec

    
    provider = _guess_provider(model_key)
    return ModelSpec(
        model_id=model_key,
        display_name=f"{model_key} (Auto-resolved)",
        provider=provider,
        context_window=8192,
        rpm_limit=60,
    )