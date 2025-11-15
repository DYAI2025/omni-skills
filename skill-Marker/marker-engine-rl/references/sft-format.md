# SFT-Format & Datenaufbereitung

**Format**: `[Instruktion/Kontext] | [Erwarteter Output/Analyse-Label]`

Liefert vollständige Labels entlang ATO→SEM→CLU→MEMA, inkl. RF-Manifestation und Intuition-Zuständen.

## Kernregeln in den Labels

### SEM-Komposition

**Regel**: ≥2 unterschiedliche ATOs (Qualitätsmechanismus)

**Begründung**: Verhindert Überinterpretation einzelner Signale; ein SEM muss durch mindestens zwei unabhängige atomare Marker gestützt werden.

**Beispiel**:

```json
{
  "id": "SEM_UNCERTAINTY_TONING",
  "composed_of": ["ATO_HESITATION", "ATO_DOUBT_PHRASE"],
  "valid": true
}
```

**Ungültig**:

```json
{
  "id": "SEM_UNCERTAINTY_TONING",
  "composed_of": ["ATO_HESITATION"],
  "valid": false,
  "reason": "Nur 1 ATO, benötigt ≥2"
}
```

### MEMA-Aktivierung

**Regel**: composed*of ≥2 CLU*\*; **ARS** (0–5) + Decay angeben

**Begründung**: Meta-Analyse erfordert systemische Evidenz aus mindestens zwei Cluster-Mustern.

**Beispiel**:

```json
{
  "id": "MEMA_RELATIONSHIP_STRAIN",
  "composed_of": ["CLU_CONFLICT_CYCLE", "CLU_REPAIR_ATTEMPT"],
  "ars": 2.3,
  "decay": "0.85/24h",
  "valid": true
}
```

## SFT-Datensatz-Format

### JSONL-Struktur

Jede Zeile ist ein JSON-Objekt:

```json
{
  "instruction": "Analysiere folgenden Dialog bis zur SEM-Ebene: Alex: 'Ich bin mir nicht ganz sicher... vielleicht überschätze ich die Nachfrage.' Ben: 'Können wir das auf morgen schieben?'",
  "output": "ATO: [ATO_UNCERTAINTY_PHRASE @'nicht ganz sicher', ATO_HEDGING_VOCAB @'vielleicht', ATO_DELAY_PHRASE @'auf morgen schieben']\nSEM: [SEM_UNCERTAINTY_TONING = {ATO_UNCERTAINTY_PHRASE, ATO_HEDGING_VOCAB}, SEM_AVOIDANT_BEHAVIOR = {ATO_DELAY_PHRASE, ATO_AVOIDANCE_PHRASE}]\nRF-Manifestation: L1-STONE × SEM_UNCERTAINTY_TONING → Schonungsvolle Grenzsetzung, Intensität: 0.52",
  "meta": {
    "rule_sem_ge_2_atos": true,
    "rf_level": "L1-STONE",
    "families": ["UNCERTAINTY", "AVOIDANCE"]
  }
}
```

### Komponenten

1. **instruction**: Klare Aufgabenstellung + Kontext (Text/Dialog)
2. **output**: Strukturierte Marker-Analyse mit:
   - Erkannte ATOs mit Spans/Zitaten
   - SEMs mit Kompositionsnachweis
   - Optional: CLUs und MEMAs
   - RF-Manifestation explizit
   - Intuition-Zustände wenn relevant
3. **meta**: Validierungs-Flags, Familien, RF-Level

## Trainings-Beispiel-Kategorien

### Kategorie 1: ATO-Erkennung

```json
{
  "instruction": "Erkenne atomare Marker: 'Hmm, ich weiß nicht so recht...'",
  "output": "ATO_HESITATION @'Hmm', ATO_UNCERTAINTY_PHRASE @'ich weiß nicht so recht'",
  "meta": { "level": "ATO", "count": 2 }
}
```

### Kategorie 2: SEM-Komposition

```json
{
  "instruction": "Bilde semantische Marker aus: ATO_HESITATION, ATO_DOUBT_PHRASE, ATO_DELAY_REQUEST",
  "output": "SEM_UNCERTAINTY_TONING = {ATO_HESITATION, ATO_DOUBT_PHRASE} (≥2 ATOs ✓)\nSEM_AVOIDANT_BEHAVIOR = {ATO_DELAY_REQUEST, ATO_TOPIC_SHIFT} (≥2 ATOs ✓)",
  "meta": { "rule_sem_ge_2_atos": true }
}
```

### Kategorie 3: CLU + Intuition

```json
{
  "instruction": "Erkenne Cluster-Muster: Fenster mit SEM_UNCERTAINTY_TONING (3×), SEM_CONFLICT_MARKER (1×)",
  "output": "CLU_INTUITION_UNCERTAINTY: provisional (mehrere weiche Signale)\n→ SEM_CONFLICT_MARKER erscheint → CLU_INTUITION_UNCERTAINTY: confirmed, Multiplier ×1.5 für UNCERTAINTY-Familie",
  "meta": { "intuition_transition": "provisional→confirmed", "multiplier": 1.5 }
}
```

### Kategorie 4: MEMA + ARS

```json
{
  "instruction": "Bilde Meta-Analyse aus: CLU_CONFLICT_CYCLE, CLU_REPAIR_ATTEMPT, CLU_PATTERN_REPEAT",
  "output": "MEMA_RELATIONSHIP_STRAIN = {CLU_CONFLICT_CYCLE, CLU_REPAIR_ATTEMPT, CLU_PATTERN_REPEAT} (≥2 CLUs ✓)\nARS: 2.8/5 (mittlere systemische Belastung)\nDecay: 0.85/24h",
  "meta": { "mema_from_clus_ge_2": true, "ars": 2.8, "decay": 0.85 }
}
```

## Qualitätskriterien

### Validierungs-Checks

1. **SEM-Komposition**: Jedes SEM muss ≥2 unterschiedliche ATOs haben
2. **MEMA-Komposition**: Jedes MEMA muss ≥2 CLUs haben
3. **RF-Konsistenz**: RF-Manifestation muss zur Marker-Familie passen
4. **Bottom-up**: Höhere Ebenen nur wenn Unterebene aktiv
5. **ARS-Plausibilität**: 0≤ARS≤5, Decay 0<d<1

### Datenbalance

- **ATO**: 40% der Beispiele (Basis-Skills)
- **SEM**: 30% (Kompositions-Logik)
- **CLU**: 20% (Pattern-Erkennung + Intuition)
- **MEMA**: 10% (Systemische Synthese)

## Datenaugmentation

### Techniken

1. **Paraphrasierung**: Gleiche Marker-Struktur, anderer Wortlaut
2. **Negativ-Beispiele**: Regelbrüche als Kontrast (z.B. SEM mit nur 1 ATO)
3. **RF-Variation**: Gleicher Dialog, unterschiedliche RF-Stufen
4. **Fenster-Shifts**: Gleiche Events, unterschiedliche Zeitfenster

### Negativ-Beispiel

```json
{
  "instruction": "Erkläre warum diese SEM-Komposition ungültig ist: SEM_UNCERTAINTY = {ATO_HESITATION}",
  "output": "FEHLER: SEM_UNCERTAINTY hat nur 1 ATO (ATO_HESITATION). Regel verletzt: SEM benötigt ≥2 unterschiedliche ATOs. Diese Komposition ist ungültig.",
  "meta": { "rule_violation": true, "type": "sem_composition" }
}
```

## Export-Format für Training

### HuggingFace Datasets

```python
from datasets import Dataset

data = {
    "instruction": [...],
    "output": [...],
    "meta": [...]
}

dataset = Dataset.from_dict(data)
dataset.save_to_disk("./marker_sft_dataset")
```

### PyTorch DataLoader

```python
class MarkerSFTDataset(Dataset):
    def __init__(self, jsonl_path):
        with open(jsonl_path) as f:
            self.data = [json.loads(line) for line in f]

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        return {
            "input_text": item["instruction"],
            "target_text": item["output"],
            "metadata": item["meta"]
        }
```
