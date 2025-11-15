---
name: marker-engine-rl
description: Vertieft den Marker-Engine-Skill um SFT/RL-Feinabstimmung mit LeanDeep 4.0; lädt Marker aus Supabase/ZIP und lernt eine Policy zur präzisen, kontextualisierten Marker-Anwendung bei strikter Bottom-up-Logik.
---

## Wann verwenden

- Wenn Agenten deterministisch-markenbasiert analysieren sollen und gleichzeitig **intuitiver** in der Auswahl, Gewichtung und Reihenfolge der Marker werden sollen (SFT→RL).
- Wenn Marker **nicht erneut abgebildet** werden müssen: die vollständigen Marker liegen bereits zentral vor (ZIP/Supabase) und werden live bezogen.
- Wenn **RF‑Kontext** und **Intuition** (provisional→confirmed→decayed) die Interpretation schärfen sollen und **MEMA/ARS** als systemische Diagnose benötigt wird.

## Workflow/Anweisungen

1. **Datenbasis übernehmen**  
   Verwende die bereitgestellten Marker‑Sätze (ZIP/Supabase) als „Single Source of Truth". Trainings‑Inputs im **SFT‑Format**: _[Instruktion/Kontext] | [Erwarteter Output]_; Beispiele enthalten ATO→SEM→CLU→MEMA inkl. RF‑Manifestation.  
   _Begründung_: SFT‑Format & Vier‑Ebenen‑Kaskade. [Quellen im Skill‑Paket]

2. **Deterministische Basis-Pipeline fixieren**  
   Erzwinge: (i) **SEM‑Komposition ≥2 unterschiedliche ATOs**, (ii) Bottom‑up‑Evaluierung (höhere Ebenen nur bei aktiver Unterebene), (iii) MEMA‑Aktivierung durch **composed*of ≥2 CLU*\***, (iv) **ARS 0–5** mit Decay. Diese Pipeline dient als Orakel und späteres Evaluations‑Backbone.

3. **SFT (Supervised Fine‑Tuning)**  
   Feine Abstimmung auf präzises Erkennen/Anwenden/Interpretieren der Marker inkl. Intuition‑Zuständen (provisional→confirmed→decayed) und temporärem Multiplier bei confirmed; RF‑Manifestation immer explizit labeln.

4. **RL‑Feintuning (Policy lernen)**  
   Definiere eine **MarkerEnv** mit Gym‑API:

   - **State**: Fenster aus Nachrichten, aktive Marker, letzte Aktionen, RF‑Level‑Schätzung.
   - **Actions**: `APPLY(marker_id) | PROMOTE(family) | SKIP | ADJUST_WINDOW(k)` (diskret).
   - **Reward** (pro Schritt): +F1‑Delta, +Gate‑Pass, +SEM‑Regel erfüllt, +ARS‑Kohärenz; −False‑Positive, −Regelverstoß, −Überdetektion.  
     Trainiere Actor‑Critic (z. B. PPO). Exportiere **policy.json** (Multiplikatoren/Fenster/Heuristik).

5. **Lehr‑Loop & Guardrails**  
   Nach jeder Epoche: **1–2 Sätze Validierung** (z. B. „SEM‑Regelverletzungen ↓22 %, ARS‑Kohärenz +0.08; nächster Schritt: LR halbieren"). Bei Misserfolg: Korrekturschleife (Reward‑Shaping anpassen, Fenster regulieren, Data‑Augment).

6. **Deployment**  
   Runtime lädt **Marker live aus Supabase** und optional `policy.json`. Policy **priorisiert und gewichtet**, die Regeln der Kaskade bleiben **unverändert** (Policy darf nicht gegen SEM‑Regel oder Bottom‑up verstoßen). Ausgabe als NDJSON‑Events inkl. ARS.

## Eingaben

- **text**: String | Liste von Nachrichten | Stream.
- **markers_source**: `supabase` (empfohlen) | `zip` | `local`; `supabase` = URL/Key in ENV.
- **runtime**: `{ sem_window, clu_window, rf_enabled, gates{min_total_markers,min_segments} }`.
- **policy_path**: optionaler Pfad zu `policy.json`.

## Ausgabeformat

JSON‑Objekt (vereinfacht):

```json
{
  "events": [
    {
      "type": "ATO_HIT",
      "id": "ATO_HESITATION",
      "messageId": "m1",
      "span": [0, 3]
    },
    {
      "type": "SEM_HIT",
      "id": "SEM_UNCERTAINTY_TONING",
      "window": ["m1"],
      "evidence": ["ATO_HESITATION", "ATO_DOUBT_PHRASE"]
    },
    {
      "type": "CLU_HIT",
      "id": "CLU_CONFLICT_ESCALATION",
      "window": ["m1", "m2"]
    },
    {
      "type": "MEMA_HIT",
      "id": "MEMA_RELATIONSHIP_STRAIN",
      "ars": 2.8,
      "decay": "0.85/24h"
    }
  ],
  "rf_context": { "level": "L1-STONE", "intensity": 0.52 },
  "telemetry": { "sem_violations": 0, "policy": "policy.json@ts=..." }
}
```

## Beispiele

**Dialog (Kurz) → bis SEM**

„Ich bin mir nicht ganz sicher… vielleicht überschätze ich die Nachfrage." / „Können wir das auf morgen schieben?" → ATOs für Unsicherheit/Hedging/Delay → SEM_UNCERTAINTY_TONING, SEM_AVOIDANT_BEHAVIOR.

**Intuition (Cluster) → confirmed**

Mehrere weiche Unsicherheits‑SEMs → CLU_INTUITION_UNCERTAINTY: provisional; „hartes" Ziel‑SEM im Fenster → confirmed, temporärer Multiplier x1.5 für Unsicherheits‑Familie.

**MEMA (Meta) → ARS**

CLU_CONFLICT_CYCLE + CLU_REPAIR → MEMA_RELATIONSHIP_STRAIN mit ARS (z. B. 2.3/5) und Decay.

## Qualitätssicherung

**CI‑Checks:** SEM‑Komposition (≥2 ATOs), Single‑Structure‑Block, Bottom‑up‑Prüfungen, Gate‑Pass.

**Eval:** ATO/SEM/CLU‑F1, ARS‑Kohärenz, Regelverletzungen/Episode, Policy‑Abstürze (0‑Toleranz).
