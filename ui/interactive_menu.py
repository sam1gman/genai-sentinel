"""
ui/interactive_menu.py — 4-Step Interactive Wizard for GenAI-Sentinel.

Guides the operator through model selection, attack vector selection,
obfuscation method selection, and defense strategy selection using
Rich prompts and panels.
"""
from __future__ import annotations

import typer
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table

from attack_engine.bipia_loader import BipiaLoader
from attack_engine.obfuscator import Obfuscator
from core.model_registry import MODEL_REGISTRY, ModelSpec, get_free_models

console = Console()

def _get_dynamic_obfuscations() -> list[str]:
    
    methods = [
        m for m in dir(Obfuscator) 
        if callable(getattr(Obfuscator, m)) and not m.startswith("_")
    ]
    if "generate_chained_attack" in methods:
        methods.remove("generate_chained_attack")
        methods.insert(0, "generate_chained_attack")
    return methods

_DEFENSE_METHODS = [
    "self_reminder",
    "sandwich_defense",
    "border_strings",
    "none",
]


def _display_model_table() -> list[ModelSpec]:
    """Print a grouped model table and return the ordered list of displayed specs."""
    table = Table(title="Available Models", border_style="cyan", expand=True)
    table.add_column("#", style="dim", width=4)
    table.add_column("Display Name", style="cyan")
    table.add_column("Model ID", style="white", no_wrap=False)
    table.add_column("Provider", style="yellow")
    table.add_column("Tag", justify="center")

    ordered: list[ModelSpec] = []
    current_provider = ""
    idx = 1

    # Group by provider
    provider_order = ["groq", "openai", "anthropic", "deepseek", "together", "mistral", "ollama"]
    grouped: dict[str, list[ModelSpec]] = {p: [] for p in provider_order}
    for spec in MODEL_REGISTRY.values():
        if spec.provider in grouped:
            grouped[spec.provider].append(spec)

    for provider in provider_order:
        for spec in grouped[provider]:
            if provider != current_provider:
                table.add_section()
                current_provider = provider
            tag = "[green][FREE][/green]" if spec.is_free else ""
            table.add_row(str(idx), spec.display_name, spec.model_id, spec.provider.upper(), tag)
            ordered.append(spec)
            idx += 1

    table.add_section()
    table.add_row(str(idx), "[italic]Enter custom model ID...[/italic]", "", "", "")
    console.print(table)
    return ordered


def _step1_models() -> list[str]:
    """Interactive model selection step."""
    console.print(Panel("[bold cyan]STEP 1 — Select Target Models[/bold cyan]", border_style="cyan"))
    ordered = _display_model_table()
    custom_idx = len(ordered) + 1

    raw = Prompt.ask(
        f'Enter comma-separated indices, [cyan]"free"[/cyan] for all free models, '
        f"or [cyan]{custom_idx}[/cyan] for custom model ID"
    ).strip()

    if raw.lower() == "free":
        selected = [s.model_id for s in get_free_models()]
        console.print(f"[green]Selected {len(selected)} free models.[/green]")
        return selected

    selected_models: list[str] = []
    for token in raw.split(","):
        token = token.strip()
        if not token:
            continue
        try:
            choice = int(token)
        except ValueError:
            console.print(f"[yellow]Skipping invalid index: {token}[/yellow]")
            continue

        if choice == custom_idx:
            custom_id = Prompt.ask("Enter custom model ID").strip()
            if custom_id:
                selected_models.append(custom_id)
        elif 1 <= choice <= len(ordered):
            selected_models.append(ordered[choice - 1].model_id)
        else:
            console.print(f"[yellow]Index {choice} out of range, skipping.[/yellow]")

    if not selected_models:
        console.print("[red]No models selected. Defaulting to llama-3.3-70b-versatile.[/red]")
        return ["llama-3.3-70b-versatile"]

    return selected_models


def _step2_attack_vectors(custom_payload_holder: list[str | None]) -> list[str]:
    """Interactive attack vector selection step."""
    console.print(Panel("[bold cyan]STEP 2 — Select Attack Vectors[/bold cyan]", border_style="cyan"))
    loader = BipiaLoader()
    vectors = loader.available_vectors()

    for i, v in enumerate(vectors, start=1):
        console.print(f"  [cyan]{i}[/cyan]. {v}")
    console.print("  [cyan]A[/cyan]. All vectors")
    console.print("  [cyan]C[/cyan]. Custom payload")

    raw = Prompt.ask("Enter comma-separated indices, A for all, C for custom").strip()

    if raw.upper() == "A":
        return list(vectors)

    selected: list[str] = []
    for token in raw.split(","):
        token = token.strip()
        if token.upper() == "C":
            cp = Prompt.ask("Enter your custom injection payload").strip()
            if cp:
                custom_payload_holder[0] = cp
                selected.append("custom")
        elif token.upper() == "A":
            return list(vectors)
        else:
            try:
                idx = int(token)
                if 1 <= idx <= len(vectors):
                    selected.append(vectors[idx - 1])
                else:
                    console.print(f"[yellow]Index {idx} out of range.[/yellow]")
            except ValueError:
                console.print(f"[yellow]Skipping invalid input: {token}[/yellow]")

    if not selected:
        console.print("[red]No vectors selected. Defaulting to data_exfiltration.[/red]")
        return ["data_exfiltration"]

    return selected


def _step3_obfuscations() -> list[str]:
    """Interactive obfuscation method selection step — Now Dynamic!"""
    console.print(Panel("[bold cyan]STEP 3 — Select Obfuscation Methods[/bold cyan]", border_style="cyan"))
    
    
    available_methods = _get_dynamic_obfuscations()
    
    for i, m in enumerate(available_methods, start=1):
        
        style = "bold magenta" if m == "generate_chained_attack" else "cyan"
        console.print(f"  [{style}]{i}[/{style}]. {m}")
        
    console.print("  [cyan]A[/cyan]. All methods")
    console.print("  [cyan]0[/cyan]. None (raw payload, no obfuscation)")

    raw = Prompt.ask("Enter comma-separated indices, A for all, 0 for none").strip()

    if raw == "0":
        return ["none"]
    if raw.upper() == "A":
        return list(available_methods)

    selected: list[str] = []
    for token in raw.split(","):
        token = token.strip()
        if token.upper() == "A":
            return list(available_methods)
        if token == "0":
            selected.append("none")
        else:
            try:
                idx = int(token)
                if 1 <= idx <= len(available_methods):
                    selected.append(available_methods[idx - 1])
                else:
                    console.print(f"[yellow]Index {idx} out of range.[/yellow]")
            except ValueError:
                console.print(f"[yellow]Skipping invalid input: {token}[/yellow]")

    if not selected:
        
        return ["generate_chained_attack"]

    return selected


def _step4_defenses() -> list[str]:
    """Interactive defense strategy selection step."""
    console.print(Panel("[bold cyan]STEP 4 — Select Defense Strategies[/bold cyan]", border_style="cyan"))
    for i, d in enumerate(_DEFENSE_METHODS, start=1):
        console.print(f"  [cyan]{i}[/cyan]. {d}")

    raw = Prompt.ask("Enter comma-separated indices (or all of the above)").strip()

    selected: list[str] = []
    for token in raw.split(","):
        token = token.strip()
        try:
            idx = int(token)
            if 1 <= idx <= len(_DEFENSE_METHODS):
                selected.append(_DEFENSE_METHODS[idx - 1])
            else:
                console.print(f"[yellow]Index {idx} out of range.[/yellow]")
        except ValueError:
            console.print(f"[yellow]Skipping invalid input: {token}[/yellow]")

    if not selected:
        console.print("[red]No defenses selected. Defaulting to none.[/red]")
        return ["none"]

    return selected


def print_summary(cfg: "SessionConfig") -> None:  # type: ignore[name-defined]
    """Display a 4-column Rich summary panel for the configured session."""
    from itertools import product

    vectors = cfg.attack_vectors + (["custom"] if cfg.custom_payload else [])
    total_calls = len(list(product(cfg.models, vectors, cfg.obfuscations, cfg.defenses)))

    panels = [
        Panel("\n".join(f"• {m}" for m in cfg.models), title="[bold cyan]Models[/bold cyan]", border_style="cyan"),
        Panel("\n".join(f"• {v}" for v in vectors), title="[bold yellow]Attack Vectors[/bold yellow]", border_style="yellow"),
        Panel("\n".join(f"• {o}" for o in cfg.obfuscations), title="[bold magenta]Obfuscations[/bold magenta]", border_style="magenta"),
        Panel("\n".join(f"• {d}" for d in cfg.defenses), title="[bold green]Defenses[/bold green]", border_style="green"),
    ]

    console.print(Columns(panels))
    console.print(
        Panel(
            f"[bold]Total estimated API calls:[/bold] [cyan]{total_calls}[/cyan]\n"
            f"[bold]Max concurrent:[/bold] {cfg.max_concurrent}\n"
            f"[bold]Rate Limit (RPM):[/bold] "
            f"{cfg.requests_per_minute if cfg.requests_per_minute > 0 else 'Unlimited'}\n"
            f"[bold]Severity:[/bold] {cfg.severity}",
            border_style="yellow",
        )
    )


def run_interactive_menu() -> "SessionConfig":  # type: ignore[name-defined]
    """Run the 4-step interactive configuration wizard."""
    from main import SessionConfig

    console.print(
        Panel(
            "[bold yellow]Welcome to the GenAI-Sentinel Interactive Wizard[/bold yellow]\n"
            "Configure your red-team session in 4 steps.",
            border_style="yellow",
        )
    )

    # Step 1-4
    models = _step1_models()
    custom_payload_holder: list[str | None] = [None]
    attack_vectors = _step2_attack_vectors(custom_payload_holder)
    custom_payload = custom_payload_holder[0]
    obfuscations = _step3_obfuscations()
    defenses = _step4_defenses()

    # Advanced settings initialization
    max_concurrent = 1
    requests_per_minute = 20
    honeytoken = "AKIAIOSFODNN7EXAMPLE"
    severity = 4

    if Confirm.ask("Configure advanced settings?", default=False):
        max_concurrent = IntPrompt.ask("Max concurrent LLM calls", default=1)
        requests_per_minute = IntPrompt.ask("Requests Per Minute (RPM) limit", default=20)
        severity = IntPrompt.ask("Severity level [4/5] (5=hardest)", default=4)

        while severity not in (4, 5):
            console.print("[yellow]Severity must be 4 or 5.[/yellow]")
            severity = IntPrompt.ask("Severity level [4/5] (5=hardest)", default=4)

        masked = honeytoken[:4] + "***"
        new_token = Prompt.ask(f"Honeytoken value [{masked}]", default=honeytoken)
        if new_token and new_token != honeytoken:
            honeytoken = new_token

    # Build the config
    cfg = SessionConfig(
        models=models,
        attack_vectors=[v for v in attack_vectors if v != "custom"],
        obfuscations=obfuscations,  # Keep "none" if selected, handled in main.py
        defenses=defenses,
        custom_payload=custom_payload,
        max_concurrent=max_concurrent,
        requests_per_minute=requests_per_minute,
        honeytoken=honeytoken,
        severity=severity,
    )

    # Logic fix: Ensure the Cartesian product doesn't break if only "none" was selected
    # This aligns with how main.py treats obfuscation strings
    if not cfg.obfuscations:
        cfg = cfg.model_copy(update={"obfuscations": ["none"]})

    print_summary(cfg)

    if not Confirm.ask("▶ Start execution?", default=True):
        console.print("[yellow]Execution cancelled.[/yellow]")
        raise typer.Exit()

    return cfg