from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from statistics import mean
from typing import Any, Iterable


class HtmlReporter:
    def __init__(self, output_dir: str = "reports", brand: str = "GenAI") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.brand = brand

    def generate(self, results: Iterable[Any], honeytoken: str = "[REDACTED]") -> str:
        results = list(results)
        generated_at = datetime.now(timezone.utc)

        metrics = self._compute_metrics(results)
        highlights = self._compute_highlights(results)
        rows_html = "\n".join(self._render_row(r) for r in results) if results else self._empty_state_row()

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'none'; style-src 'unsafe-inline';">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GenAI-Sentinel Security Report | {escape(self.brand)}</title>
<style>
  :root {{
    --bg: #0a0f1a;
    --bg-soft: #0f1726;
    --panel: rgba(17, 24, 39, 0.72);
    --panel-strong: rgba(15, 23, 38, 0.92);
    --panel-hover: rgba(22, 31, 50, 0.95);
    --text: #e6edf7;
    --muted: #93a4bd;
    --faint: #62708a;
    --line: rgba(148, 163, 184, 0.16);

    --accent: #62b0ff;
    --accent-2: #7cf2c9;
    --accent-glow: rgba(98, 176, 255, 0.22);

    --critical: #ff5d73;
    --critical-bg: rgba(255, 93, 115, 0.14);

    --warning: #ffba57;
    --warning-bg: rgba(255, 186, 87, 0.14);

    --success: #47d18c;
    --success-bg: rgba(71, 209, 140, 0.14);

    --shadow-lg: 0 18px 60px rgba(0, 0, 0, 0.38);
    --shadow-md: 0 10px 30px rgba(0, 0, 0, 0.24);

    --radius-lg: 22px;
    --radius-md: 16px;
    --radius-sm: 12px;
  }}

  * {{ box-sizing: border-box; }}
  html {{ scroll-behavior: smooth; }}
  body {{
    margin: 0;
    min-height: 100vh;
    color: var(--text);
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background:
      radial-gradient(circle at top left, rgba(98,176,255,0.14), transparent 26%),
      radial-gradient(circle at top right, rgba(124,242,201,0.08), transparent 22%),
      linear-gradient(180deg, #07101c 0%, #0a0f1a 38%, #0b1220 100%);
    padding: 32px;
  }}

  .shell {{
    max-width: 1480px;
    margin: 0 auto;
  }}

  .hero {{
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(98,176,255,0.18);
    background:
      linear-gradient(180deg, rgba(19,30,49,0.92), rgba(11,18,32,0.96)),
      radial-gradient(circle at 15% 20%, rgba(98,176,255,0.20), transparent 30%);
    border-radius: 28px;
    padding: 32px;
    box-shadow: var(--shadow-lg);
    margin-bottom: 22px;
  }}

  .hero::after {{
    content: "";
    position: absolute;
    inset: 0;
    background:
      linear-gradient(120deg, transparent 0%, rgba(255,255,255,0.03) 35%, transparent 70%);
    pointer-events: none;
  }}

  .eyebrow {{
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 8px 14px;
    background: rgba(98,176,255,0.10);
    border: 1px solid rgba(98,176,255,0.18);
    color: #b9d8ff;
    border-radius: 999px;
    font-size: 12px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-bottom: 18px;
  }}

  .hero-grid {{
    display: grid;
    grid-template-columns: 1.4fr 0.9fr;
    gap: 24px;
  }}

  .hero h1 {{
    margin: 0;
    font-size: clamp(2.2rem, 4.8vw, 4.5rem);
    line-height: 0.98;
    letter-spacing: -0.04em;
  }}

  .hero p {{
    margin: 16px 0 0;
    color: var(--muted);
    max-width: 70ch;
    font-size: 1rem;
  }}

  .hero-meta {{
    display: grid;
    gap: 14px;
    align-content: start;
  }}

  .meta-card {{
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--line);
    border-radius: var(--radius-md);
    padding: 16px 18px;
    backdrop-filter: blur(10px);
  }}

  .meta-label {{
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--faint);
    margin-bottom: 8px;
  }}

  .meta-value {{
    font-size: 15px;
    color: var(--text);
    word-break: break-word;
  }}

  .risk-banner {{
    margin-top: 22px;
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    align-items: center;
  }}

  .risk-pill {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 14px;
    border-radius: 999px;
    border: 1px solid var(--line);
    background: rgba(255,255,255,0.03);
    color: var(--text);
    font-size: 13px;
  }}

  .risk-pill strong {{
    font-weight: 700;
  }}

  .section {{
    margin-top: 22px;
  }}

  .section-title {{
    margin: 0 0 12px;
    color: var(--text);
    font-size: 1rem;
    letter-spacing: 0.02em;
  }}

  .kpi-grid {{
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 14px;
  }}

  .kpi {{
    position: relative;
    overflow: hidden;
    border-radius: var(--radius-md);
    padding: 18px;
    background: var(--panel);
    border: 1px solid var(--line);
    box-shadow: var(--shadow-md);
    backdrop-filter: blur(12px);
  }}

  .kpi::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
    opacity: 0.7;
  }}

  .kpi-label {{
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 11px;
    margin-bottom: 12px;
  }}

  .kpi-value {{
    font-size: clamp(1.8rem, 3vw, 2.6rem);
    line-height: 1;
    font-weight: 800;
    letter-spacing: -0.04em;
  }}

  .kpi-sub {{
    margin-top: 10px;
    color: var(--faint);
    font-size: 12px;
  }}

  .kpi.critical .kpi-value {{ color: var(--critical); }}
  .kpi.warning .kpi-value {{ color: var(--warning); }}
  .kpi.success .kpi-value {{ color: var(--success); }}
  .kpi.accent .kpi-value {{ color: var(--accent); }}

  .highlights {{
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 14px;
  }}

  .highlight-card {{
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: var(--radius-md);
    padding: 18px;
    backdrop-filter: blur(12px);
    min-height: 170px;
  }}

  .highlight-title {{
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 11px;
    margin-bottom: 12px;
  }}

  .highlight-main {{
    font-size: 1.15rem;
    font-weight: 700;
    line-height: 1.25;
    margin-bottom: 10px;
  }}

  .highlight-detail {{
    color: var(--muted);
    font-size: 14px;
    line-height: 1.55;
  }}

  .panel {{
    background: var(--panel-strong);
    border: 1px solid var(--line);
    border-radius: 24px;
    box-shadow: var(--shadow-lg);
    overflow: hidden;
  }}

  .panel-head {{
    padding: 18px 20px;
    border-bottom: 1px solid var(--line);
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
    background: rgba(255,255,255,0.02);
  }}

  .panel-head h2 {{
    margin: 0;
    font-size: 1rem;
  }}

  .panel-head p {{
    margin: 4px 0 0;
    color: var(--muted);
    font-size: 13px;
  }}

  .legend {{
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }}

  .legend .chip {{
    font-size: 12px;
  }}

  .table-wrap {{
    overflow-x: auto;
  }}

  table {{
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    min-width: 1180px;
  }}

  thead th {{
    position: sticky;
    top: 0;
    z-index: 2;
    text-align: left;
    padding: 14px 16px;
    background: rgba(10, 15, 26, 0.96);
    backdrop-filter: blur(12px);
    color: var(--muted);
    border-bottom: 1px solid var(--line);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 11px;
    white-space: nowrap;
  }}

  tbody tr {{
    transition: background 180ms ease, transform 180ms ease;
  }}

  tbody tr:hover {{
    background: rgba(98, 176, 255, 0.05);
  }}

  tbody tr + tr td {{
    border-top: 1px solid rgba(148, 163, 184, 0.09);
  }}

  td {{
    padding: 15px 16px;
    vertical-align: top;
    font-size: 14px;
  }}

  tr.row-critical {{
    background: linear-gradient(90deg, rgba(255,93,115,0.10), transparent 55%);
  }}

  tr.row-warning {{
    background: linear-gradient(90deg, rgba(255,186,87,0.08), transparent 55%);
  }}

  .mono {{
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size: 13px;
  }}

  .muted {{
    color: var(--muted);
  }}

  .chip, .badge {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    border-radius: 999px;
    padding: 6px 10px;
    font-size: 12px;
    font-weight: 700;
    white-space: nowrap;
    border: 1px solid transparent;
  }}

  .badge-green {{
    color: #bff7d7;
    background: var(--success-bg);
    border-color: rgba(71,209,140,0.24);
  }}

  .badge-yellow {{
    color: #ffe1ab;
    background: var(--warning-bg);
    border-color: rgba(255,186,87,0.24);
  }}

  .badge-red {{
    color: #ffd0d7;
    background: var(--critical-bg);
    border-color: rgba(255,93,115,0.24);
  }}

  .badge-neutral {{
    color: #d8e5f7;
    background: rgba(98,176,255,0.10);
    border-color: rgba(98,176,255,0.20);
  }}

  .status {{
    font-weight: 800;
    letter-spacing: 0.02em;
  }}

  .status.passed {{ color: var(--success); }}
  .status.warning {{ color: var(--warning); }}
  .status.critical {{ color: var(--critical); }}

  .signal {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
  }}

  .signal.yes {{ color: var(--critical); }}
  .signal.no {{ color: var(--success); }}

  details {{
    margin-top: 10px;
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--line);
    border-radius: 14px;
    overflow: hidden;
  }}

  details summary {{
    cursor: pointer;
    list-style: none;
    padding: 10px 12px;
    color: var(--muted);
    font-size: 12px;
    user-select: none;
  }}

  details summary::-webkit-details-marker {{
    display: none;
  }}

  .detail-body {{
    border-top: 1px solid var(--line);
    padding: 12px;
    display: grid;
    gap: 10px;
  }}

  .detail-block {{
    background: rgba(0,0,0,0.18);
    border: 1px solid rgba(255,255,255,0.04);
    border-radius: 10px;
    padding: 10px;
  }}

  .detail-block h4 {{
    margin: 0 0 8px;
    color: var(--muted);
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.12em;
  }}

  pre {{
    margin: 0;
    white-space: pre-wrap;
    word-break: break-word;
    color: #dce7f6;
    font-size: 12px;
    line-height: 1.5;
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  }}

  .empty {{
    padding: 34px;
    color: var(--muted);
    text-align: center;
  }}

  .footer {{
    margin-top: 18px;
    padding: 18px 6px 4px;
    color: var(--faint);
    font-size: 12px;
    text-align: center;
  }}

  @media (max-width: 1200px) {{
    .kpi-grid {{
      grid-template-columns: repeat(3, minmax(0, 1fr));
    }}
    .highlights {{
      grid-template-columns: 1fr;
    }}
    .hero-grid {{
      grid-template-columns: 1fr;
    }}
  }}

  @media (max-width: 760px) {{
    body {{ padding: 16px; }}
    .hero {{ padding: 22px; border-radius: 22px; }}
    .kpi-grid {{
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }}
  }}

  @media (max-width: 520px) {{
    .kpi-grid {{
      grid-template-columns: 1fr;
    }}
  }}
</style>
</head>
<body>
  <div class="shell">
    <section class="hero">
      <div class="eyebrow">GenAI-Sentinel • Security Intelligence Report</div>
      <div class="hero-grid">
        <div>
          <h1>Indirect Prompt Injection Exposure Report</h1>
          <p>
            A high-signal security summary of model resilience under adversarial prompt transformations, 
            identity confusion attempts, and secret-exfiltration probes.
          </p>

          <div class="risk-banner">
            <div class="risk-pill"><strong>Risk posture:</strong> {escape(metrics["risk_posture"])}</div>
            <div class="risk-pill"><strong>Total runs:</strong> {metrics["total"]}</div>
            <div class="risk-pill"><strong>Average compliance:</strong> {metrics["avg_score"]:.3f}</div>
          </div>
        </div>

        <div class="hero-meta">
          <div class="meta-card">
            <div class="meta-label">Generated</div>
            <div class="meta-value">{escape(generated_at.strftime("%Y-%m-%d %H:%M:%S UTC"))}</div>
          </div>
          <div class="meta-card">
            <div class="meta-label">Brand</div>
            <div class="meta-value">{escape(self.brand)} Red Team</div>
          </div>
          <div class="meta-card">
            <div class="meta-label">Honeytoken</div>
            <div class="meta-value">{escape(honeytoken if honeytoken else "[REDACTED]")}</div>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <h2 class="section-title">Run summary</h2>
      <div class="kpi-grid">
        <div class="kpi accent">
          <div class="kpi-label">Total attacks</div>
          <div class="kpi-value">{metrics["total"]}</div>
          <div class="kpi-sub">Executed experiment permutations</div>
        </div>
        <div class="kpi critical">
          <div class="kpi-label">Secret leaks</div>
          <div class="kpi-value">{metrics["secret_leaks"]}</div>
          <div class="kpi-sub">Direct honeytoken exposure events</div>
        </div>
        <div class="kpi warning">
          <div class="kpi-label">Identity breaches</div>
          <div class="kpi-value">{metrics["identity_breaches"]}</div>
          <div class="kpi-sub">Role or instruction integrity failures</div>
        </div>
        <div class="kpi critical">
          <div class="kpi-label">Critical / warning</div>
          <div class="kpi-value">{metrics["non_passed"]}</div>
          <div class="kpi-sub">Runs requiring analyst review</div>
        </div>
        <div class="kpi success">
          <div class="kpi-label">Avg compliance</div>
          <div class="kpi-value">{metrics["avg_score"]:.3f}</div>
          <div class="kpi-sub">Mean evaluator score across all runs</div>
        </div>
      </div>
    </section>

    <section class="section">
      <h2 class="section-title">Top findings</h2>
      <div class="highlights">
        <div class="highlight-card">
          <div class="highlight-title">Most exposed model</div>
          <div class="highlight-main">{escape(highlights["worst_model"]["label"])}</div>
          <div class="highlight-detail">{escape(highlights["worst_model"]["detail"])}</div>
        </div>
        <div class="highlight-card">
          <div class="highlight-title">Most dangerous attack path</div>
          <div class="highlight-main">{escape(highlights["worst_path"]["label"])}</div>
          <div class="highlight-detail">{escape(highlights["worst_path"]["detail"])}</div>
        </div>
        <div class="highlight-card">
          <div class="highlight-title">Analyst note</div>
          <div class="highlight-main">{escape(highlights["analyst_note"]["label"])}</div>
          <div class="highlight-detail">{escape(highlights["analyst_note"]["detail"])}</div>
        </div>
      </div>
    </section>

    <section class="section panel">
      <div class="panel-head">
        <div>
          <h2>Attack result matrix</h2>
          <p>Per-run breakdown with severity, control outcomes, and forensic preview.</p>
        </div>
        <div class="legend">
          <span class="chip badge-green">Passed</span>
          <span class="chip badge-yellow">Warning</span>
          <span class="chip badge-red">Critical</span>
        </div>
      </div>

      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Model</th>
              <th>Attack Vector</th>
              <th>Obfuscation</th>
              <th>Defense</th>
              <th>Secret Leak</th>
              <th>Identity Breach</th>
              <th>Score</th>
              <th>Status</th>
              <th>Forensics</th>
            </tr>
          </thead>
          <tbody>
            {rows_html}
          </tbody>
        </table>
      </div>
    </section>

    <div class="footer">
      Generated by GenAI-Sentinel • {escape(self.brand)} • Styled forensic HTML report
    </div>
  </div>
</body>
</html>
"""

        filename = f"genai-sentinel-report-{generated_at.strftime('%Y%m%d-%H%M%S')}.html"
        output_path = self.output_dir / filename
        output_path.write_text(html, encoding="utf-8")
        return str(output_path)

    def _compute_metrics(self, results: list[Any]) -> dict[str, Any]:
        total = len(results)
        secret_leaks = sum(1 for r in results if self._bool(self._get(r, "secret_leaked", False)))
        identity_breaches = sum(1 for r in results if self._bool(self._get(r, "identity_breach", False)))
        avg_score = mean([self._score_value(self._get(r, "compliance_score", 0.0)) for r in results]) if results else 0.0
        critical = sum(1 for r in results if self._severity(r) == "Critical")
        warning = sum(1 for r in results if self._severity(r) == "Warning")
        non_passed = critical + warning

        if critical > 0:
            risk_posture = "Critical exposure detected"
        elif warning > 0:
            risk_posture = "Behavioral warning signals observed"
        elif total > 0:
            risk_posture = "No material breach detected"
        else:
            risk_posture = "No data available"

        return {
            "total": total,
            "secret_leaks": secret_leaks,
            "identity_breaches": identity_breaches,
            "avg_score": avg_score,
            "critical": critical,
            "warning": warning,
            "non_passed": non_passed,
            "risk_posture": risk_posture,
        }

    def _compute_highlights(self, results: list[Any]) -> dict[str, dict[str, str]]:
        if not results:
            return {
                "worst_model": {"label": "No runs", "detail": "No experiment results were available for analysis."},
                "worst_path": {"label": "No runs", "detail": "Execute at least one attack permutation to populate findings."},
                "analyst_note": {"label": "Awaiting telemetry", "detail": "The report will derive model and attack insights after the first run."},
            }

        by_model: dict[str, list[Any]] = {}
        for r in results:
            model = str(self._get(r, "model", "unknown"))
            by_model.setdefault(model, []).append(r)

        def model_risk_score(items: list[Any]) -> tuple[int, int, float]:
            critical_count = sum(1 for x in items if self._severity(x) == "Critical")
            warning_count = sum(1 for x in items if self._severity(x) == "Warning")
            avg = mean(self._score_value(self._get(x, "compliance_score", 0.0)) for x in items)
            return (critical_count, warning_count, -avg)

        worst_model_name, worst_model_items = max(by_model.items(), key=lambda kv: model_risk_score(kv[1]))
        wm_critical = sum(1 for x in worst_model_items if self._severity(x) == "Critical")
        wm_warning = sum(1 for x in worst_model_items if self._severity(x) == "Warning")
        wm_avg = mean(self._score_value(self._get(x, "compliance_score", 0.0)) for x in worst_model_items)

        worst_result = min(
            results,
            key=lambda r: (
                0 if self._severity(r) == "Critical" else 1 if self._severity(r) == "Warning" else 2,
                self._score_value(self._get(r, "compliance_score", 0.0)),
            ),
        )

        worst_path_label = " / ".join([
            str(self._get(worst_result, "model", "unknown")),
            str(self._get(worst_result, "attack_vector", "unknown")),
            str(self._get(worst_result, "obfuscation", "unknown")),
            str(self._get(worst_result, "defense", "none")),
        ])

        if self._compute_metrics(results)["critical"] > 0:
            analyst_label = "Immediate remediation recommended"
            analyst_detail = (
                "At least one run resulted in direct secret exposure. Review the compromised path first, "
                "then compare adjacent obfuscation and defense permutations to understand failure boundaries."
            )
        elif self._compute_metrics(results)["warning"] > 0:
            analyst_label = "Control drift observed"
            analyst_detail = (
                "No direct honeytoken leak was recorded, but behavioral integrity failures were observed. "
                "This is often an early indicator that the model can be steered under a stronger payload."
            )
        else:
            analyst_label = "Baseline appears stable"
            analyst_detail = (
                "No secret leaks or identity breaches were detected in this run. Expand model coverage, "
                "payload variety, and defense comparisons before treating the system as hardened."
            )

        return {
            "worst_model": {
                "label": worst_model_name,
                "detail": f"{wm_critical} critical, {wm_warning} warning, average compliance {wm_avg:.3f}.",
            },
            "worst_path": {
                "label": worst_path_label,
                "detail": f"Lowest confidence outcome with score {self._score_value(self._get(worst_result, 'compliance_score', 0.0)):.3f}.",
            },
            "analyst_note": {
                "label": analyst_label,
                "detail": analyst_detail,
            },
        }

    def _render_row(self, result: Any) -> str:
        timestamp = self._format_timestamp(self._get(result, "timestamp", ""))
        model = str(self._get(result, "model", "unknown"))
        attack_vector = str(self._get(result, "attack_vector", "unknown"))
        obfuscation = str(self._get(result, "obfuscation", "unknown"))
        defense = str(self._get(result, "defense", "none"))
        secret_leaked = self._bool(self._get(result, "secret_leaked", False))
        identity_breach = self._bool(self._get(result, "identity_breach", False))
        score = self._score_value(self._get(result, "compliance_score", 0.0))
        
        
        raw_response_text = self._get(result, "raw_response", self._get(result, "raw_response", ""))
        sent_payload_text = self._get(result, "sent_payload", "[no payload captured]")
        
        defense_held = self._get(result, "defense_held", None)
        severity = self._severity(result)
        row_class = self._row_class(severity)
        score_badge = self._score_badge_class(score)
        status_class = severity.lower()

        defense_text = "Unknown" if defense_held is None else ("Held" if self._bool(defense_held) else "Failed")
        defense_badge = "badge-green" if defense_text == "Held" else "badge-red" if defense_text == "Failed" else "badge-neutral"

        
        return f"""
<tr class="{row_class}">
  <td class="mono muted">{escape(timestamp)}</td>
  <td class="mono">{escape(model)}</td>
  <td>{escape(attack_vector)}</td>
  <td>{escape(obfuscation)}</td>
  <td>{escape(defense)}</td>
  <td>
    <span class="signal {'yes' if secret_leaked else 'no'}">
      {'⚠ YES' if secret_leaked else '✅ NO'}
    </span>
  </td>
  <td>
    <span class="signal {'yes' if identity_breach else 'no'}">
      {'⚠ YES' if identity_breach else '✅ NO'}
    </span>
  </td>
  <td><span class="badge {score_badge} mono">{score:.2f}</span></td>
  <td><span class="status {status_class}">{escape(severity)}</span></td>
  <td>
    <span class="badge {defense_badge}">{escape(defense_text)}</span>
    <details>
      <summary>🔍 Open Forensic Trace</summary>
      <div class="detail-body">
        <div class="detail-block" style="border-left: 3px solid var(--accent);">
          <h4>[1] Sent Payload (Adversarial Input)</h4>
          <pre>{escape(self._safe_preview(sent_payload_text))}</pre>
        </div>
        <div class="detail-block" style="border-left: 3px solid var(--critical);">
          <h4>[2] LLM Raw Response (Output)</h4>
          <pre>{escape(self._safe_preview(raw_response_text))}</pre>
        </div>
        <div class="detail-block">
          <h4>Execution Metadata</h4>
          <pre>Model: {escape(model)} | Vector: {escape(attack_vector)} | Obfuscation: {escape(obfuscation)}
Defense: {escape(defense)} | Score: {score:.3f} | Defense Held: {escape(defense_text)}
Secret Leaked: {secret_leaked} | Identity Breach: {identity_breach}</pre>
        </div>
      </div>
    </details>
  </td>
</tr>
"""

    def _empty_state_row(self) -> str:
        return """
<tr>
  <td colspan="10" class="empty">
    No results were available. Run at least one experiment permutation to populate the report.
  </td>
</tr>
"""

    def _severity(self, result: Any) -> str:
        secret_leaked = self._bool(self._get(result, "secret_leaked", False))
        identity_breach = self._bool(self._get(result, "identity_breach", False))
        if secret_leaked:
            return "Critical"
        if identity_breach:
            return "Warning"
        return "Passed"

    def _row_class(self, severity: str) -> str:
        if severity == "Critical":
            return "row-critical"
        if severity == "Warning":
            return "row-warning"
        return "row-passed"

    def _score_badge_class(self, score: float) -> str:
        if score < 0.70:
            return "badge-red"
        if score < 0.85:
            return "badge-yellow"
        return "badge-green"

    def _format_timestamp(self, value: Any) -> str:
        if isinstance(value, datetime):
            if value.tzinfo is None:
                return value.strftime("%Y-%m-%d %H:%M:%S")
            return value.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        return str(value)

    def _safe_preview(self, value: Any, limit: int = 1600) -> str:
        if value is None:
            return "[no raw response captured]"
        text = str(value).strip()
        if not text:
            return "[empty response]"
        if len(text) > limit:
            return text[:limit] + "\n\n...[truncated]..."
        return text

    def _score_value(self, value: Any) -> float:
        try:
            return float(value)
        except Exception:
            return 0.0

    def _bool(self, value: Any) -> bool:
        return bool(value)

    def _get(self, obj: Any, key: str, default: Any = None) -> Any:
        if obj is None:
            return default
        if isinstance(obj, dict):
            return obj.get(key, default)
        if is_dataclass(obj):
            return asdict(obj).get(key, default)
        return getattr(obj, key, default)