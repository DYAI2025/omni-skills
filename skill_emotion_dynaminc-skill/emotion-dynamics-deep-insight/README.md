# emotion-dynamics-deep-insight

Kurzer Überblick über Struktur, Installation und Validierung des Skills.

## Struktur
- `SKILL.md` – Spezifikation, Workflow und Ausgabeformat.
- `references/emotion-dynamics-quick-notes.md` – Kurzreferenz zu Emotion Dynamics & UED.

## Installation (Generator)
Falls du den Ordner neu generieren möchtest, nutze das Install-Skript im Repo-Wurzelverzeichnis:

```bash
bash ./install_emotion_dynamics_deep_insight.sh
```

## Schnelle Validierung
Prüft, ob Kern-Dateien vorhanden sind und Basis-Marker in `SKILL.md` existieren:

```bash
python3 ./quick_validate.py emotion-dynamics-deep-insight
```

## Hinweise
- Inhalte sind heuristisch/qualitativ; kein diagnostischer Anspruch.
- Beiträge sollten die in `SKILL.md` beschriebenen Konventionen respektieren.

