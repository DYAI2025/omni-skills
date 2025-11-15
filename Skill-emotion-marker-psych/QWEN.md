# Psychoanalytic Dynamics Fusion Skill

## Overview

This directory contains specifications for a psychoanalytic dynamics fusion skill that combines LeanDeep markers (ATO→SEM→CLU→MEMA) with emotion dynamics and applies a psychoanalytic lens (conflicts, defense, transference). The skill optionally uses a brainstorming feature to generate hypotheses and focus lenses.

## Key Components

### Skill Definition (SKILL.md)
- Name: `psychoanalytic-dynamics-fusion`
- Description: A meta-level analysis skill that unites LeanDeep markers with emotion dynamics and applies a psychoanalytic lens

### Input Requirements
- `input`: Free text or dialogue turns (maintain chronology)
- `marker_engine`: Object/events in marker-engine format (if available)
- `emotion_dynamics`: Current state, trends, triggers, and optional timeline (if available)
- `flags`: For example, `superpowers:brainstorm` to enable brainstorming
- `context`: Optional metadata (relationship/setting/times)

### Output Goals
1. Coherent, evidence-based synthesis of marker and emotional signals
2. Psychoanalytic lens: Plausible hypotheses about conflicts, defense, and transference - carefully and traceably
3. Coach next actions as short, implementable steps
4. Structured JSON output plus a brief, user-readable summary

### Core Features

#### Brainstorming Component
- When enabled, generates 5-7 lenses (labels with 1-sentence descriptions)
- Provides questions and observable marker families for each lens
- Used only for focusing, not as evidence

#### Evidence Coherence
- Maps emotion trends to active marker windows
- Aligns temporally (window/turn IDs) and marks inflection points
- Checks complementarity (e.g., SEM_AVOIDANT_BEHAVIOR ↔ Trend withdrawal/emptiness)
- Evaluates intuition/confirmation based on marker hits

#### Psychoanalytic Lens
- Designs 1-3 core conflicts
- Names plausible defense mechanisms and transference offers (as hypotheses)
- Each hypothesis includes:
  - `derives_from`: References to specific `sems[]/clus[]/memas[]` and emotion points
  - `confidence`: 0-1 (subjective, calibrated)
  - `explanation`: 1-2 sentences, layperson comprehensible

## File Structure

The skill includes:
- `SKILL.md`: Main skill definition and documentation
- `references/output-schema.json`: JSON schema for output format
- `assets/prompt_superpowers_brainstorm.md`: Brainstorming prompt
- `assets/prompt_runtime_guidelines.md`: Runtime guidelines

## Output Schema

The JSON output includes:
- Summary text
- Brainstorm results (if enabled)
- Marker engine data
- Emotion dynamics data
- Psychoanalytic inferences (core conflicts, defenses, transference)
- Coach next actions
- Evidence-prefixed declarations
- Self-check validation