"""
logger/supabase_telemetry.py — Async Telemetry Logger with Graceful Degradation.

Attempts to persist attack results to a Supabase table (sentinel_logs).
Falls back silently to a local JSON file when Supabase is unavailable.
All file writes are protected with asyncio.Lock() to prevent corruption
under concurrent execution.
"""
from __future__ import annotations

import asyncio
import json
import os
import warnings
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import AttackResult


class SupabaseTelemetry:
    """Async telemetry logger with Supabase primary and JSON fallback.

    Initialises the Supabase client if ``SUPABASE_URL`` and ``SUPABASE_KEY``
    are both present in the environment; otherwise falls back to local JSON.

    Args:
        telemetry_file: Path to the local JSON telemetry fallback file.
    """

    def __init__(self, telemetry_file: str = "./data/telemetry.json") -> None:
        self._telemetry_file = telemetry_file
        self._lock = asyncio.Lock()
        self._use_supabase = False
        self._supabase_client: object | None = None
        self._init_supabase()

    def _init_supabase(self) -> None:
        """Attempt to initialise the Supabase client from environment variables.

        Sets ``self._use_supabase = True`` only when both URL and key are
        non-empty and the client initialises without error.
        """
        url = os.environ.get("SUPABASE_URL", "").strip()
        key = os.environ.get("SUPABASE_KEY", "").strip()

        if not url or not key:
            warnings.warn(
                "Supabase not configured, falling back to local JSON",
                stacklevel=2,
            )
            return

        try:
            from supabase import create_client  
            self._supabase_client = create_client(url, key)
            self._use_supabase = True
        except Exception as exc:
            warnings.warn(
                f"Supabase client init failed ({exc}), falling back to local JSON",
                stacklevel=2,
            )

    async def log(self, result: "AttackResult") -> None:
        """Persist a single attack result to Supabase or JSON fallback.

        Attempts Supabase insertion first. On any exception — or if Supabase
        is not configured — falls through to the JSON file fallback.

        Args:
            result: The ``AttackResult`` dataclass to persist.
        """
        if self._use_supabase and self._supabase_client is not None:
            try:
                await self._supabase_insert(result)
                return
            except Exception:
                # Silent fall-through to JSON fallback
                pass

        await self._json_fallback(result)

    async def _supabase_insert(self, result: "AttackResult") -> None:
        """Insert a result row into the Supabase sentinel_logs table.

        Args:
            result: The ``AttackResult`` to insert.
        """
        row = {
            "timestamp": result.timestamp,
            "model": result.model,
            "attack_vector": result.attack_vector,
            "obfuscation": result.obfuscation,
            "defense": result.defense,
            "sent_payload": result.sent_payload,
            "llm_raw_response": result.raw_response,
            "identity_breach": result.identity_breach,
            "secret_leaked": result.secret_leaked,
            "compliance_score": result.compliance_score,
            "defense_held": result.defense_held,
        }
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: (
                self._supabase_client  
                .table("sentinel_logs")
                .insert(row)
                .execute()
            ),
        )

    async def _json_fallback(self, result: "AttackResult") -> None:
        """Append a result to the local JSON telemetry file.

        Uses ``asyncio.Lock`` to ensure safe concurrent writes.
        Creates parent directories if they do not exist.
        Appends a ``/telemetry.json`` suffix if the path resolves to a directory.

        Args:
            result: The ``AttackResult`` to append.
        """
        async with self._lock:
            file_path = self._telemetry_file

            # Resolve directory paths
            if os.path.isdir(file_path):
                file_path = os.path.join(file_path, "telemetry.json")

            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)

            # Load existing records
            existing: list[dict] = []
            if path.exists():
                try:
                    existing = json.loads(path.read_text(encoding="utf-8"))
                    if not isinstance(existing, list):
                        existing = []
                except (json.JSONDecodeError, ValueError):
                    existing = []

            # Append new record
            existing.append({
                "timestamp": result.timestamp,
                "model": result.model,
                "attack_vector": result.attack_vector,
                "obfuscation": result.obfuscation,
                "defense": result.defense,
                "sent_payload": result.sent_payload,
                "raw_response": result.raw_response,
                "identity_breach": result.identity_breach,
                "secret_leaked": result.secret_leaked,
                "compliance_score": result.compliance_score,
                "defense_held": result.defense_held,
            })

            path.write_text(json.dumps(existing, indent=2), encoding="utf-8")

    async def log_batch(self, results: list["AttackResult"]) -> None:
        """Persist a batch of attack results concurrently.

        Args:
            results: List of ``AttackResult`` instances to log.
        """
        await asyncio.gather(*[self.log(r) for r in results])