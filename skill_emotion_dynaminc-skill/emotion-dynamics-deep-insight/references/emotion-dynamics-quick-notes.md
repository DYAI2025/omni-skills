# Emotion Dynamics & UED – Kurzreferenz

## Kernideen

- Emotion Dynamics (Hollenstein 2015; Kuppens & Verduyn 2017) beschreibt, wie sich emotionale Zustände über die Zeit verändern, statt sie nur als statische Momentaufnahmen zu betrachten.
- Hipson & Mohammad (2021) führen **Utterance Emotion Dynamics (UED)** ein:  
  Emotionsdynamik wird aus einer Sequenz von Äußerungen (Utterances) abgeleitet – z. B. aus Dialogen, Tagebucheinträgen, Tweets. :contentReference[oaicite:2]{index=2}
- Das verlinkte EmotionDynamics-Repository nutzt Wort-Emotion-Lexika (NRC VAD / NRC EmoLex), um aus Text kontinuierliche Emotionswerte (Valenz, Arousal, Dominanz) und daraus abgeleitete Metriken zu berechnen. :contentReference[oaicite:3]{index=3}

## Typische UED-Metriken (vereinfacht)

- **Home Base**  
  - Typischer Emotionszustand einer Person (z. B. leicht positiv, gering aktiviert).
- **Variabilität**  
  - Wie stark schwanken die Emotionen um die Home Base?
- **Instabilität / Sprunghaftigkeit**  
  - Wie häufig und wie abrupt wechseln Emotionen zwischen weit entfernten Zuständen?
- **Inertia (Trägheit)**  
  - Wie schnell kehren Emotionen nach einem Ausschlag zur Home Base zurück?
- **Rise Rate**  
  - Wie schnell steigen Emotionen nach einem auslösenden Ereignis an?
- **Recovery Rate**  
  - Wie schnell beruhigen sie sich wieder?
- **Density**  
  - Wie stark ist der Text insgesamt emotional gesättigt?

## Adaption in diesem Skill

- Statt numerischer Berechnung aus Lexika arbeitet der Skill mit qualitativen, konsistent skalierten Schätzungen für:
  - Valenz, Arousal, Dominanz (`[-1,1]` bzw. `[0,1]`).
  - Diskrete Emotionen (anger, fear, joy, sadness, usw.) im Bereich `[0,1]`.
- Die oben genannten UED-Metriken werden:
  - grob aggregiert (Mittelwerte, Muster über den Verlauf),
  - qualitativ beschrieben,
  - mit psychologischen Interpretations-Hypothesen verknüpft – ohne diagnostischen Anspruch.

