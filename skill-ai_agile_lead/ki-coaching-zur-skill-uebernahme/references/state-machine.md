%% Mermaid State Machine: Vier-Phasen-Prozess (Agent-geführt)
stateDiagram-v2
    [*] --> Ideation
    Ideation --> Backlog: Ideation Gate (Architekt+Agent)
    Ideation --> Ideation: Iterate (Code→Test→Critique→Refactor)
    Backlog --> Execution: Backlog Gate (Handwerker+Kritiker)
    Backlog --> Ideation: Erkenntnisse / Lücken
    Execution --> Execution: Short Cycles + Execution Gate (Team+Kritiker)
    Execution --> Mastery: Reifegrad (Team autonom im Agent-Rahmen)
    Execution --> Backlog: Re-Slicing / neue Erkenntnisse
    Mastery --> [*]
