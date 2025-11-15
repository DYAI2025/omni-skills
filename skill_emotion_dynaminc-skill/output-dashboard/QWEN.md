# Emotion Dynamics and Marker Annotation Dashboard

## Project Overview

This directory contains a comprehensive dashboard solution for visualizing outputs from two specialized skills:

1. **Emotion Dynamics Skill** (`emotion-dynamics-deep-insight`) - Analyzes emotional valence, arousal, and dominance in text
2. **Marker Annotation Skill** - Performs marker-based annotations using the LeanDeep architecture (ATO→SEM→CLU→MEMA)

The project also includes specifications for a psychoanalytic fusion skill that combines both approaches.

## Directory Structure

- `emotion-dynamics-dashboard.html` - Standalone dashboard for emotion dynamics visualization
- `sample-emotion-dynamics.json` - Sample data file in the expected format
- `blueprint-dashboard.md` - Original blueprint with complete HTML implementation
- `QWEN.md` - Current documentation file
- `Skill-emotion-marker-psych/` - Directory containing psychoanalytic fusion skill specifications

## Dashboard Features

### Emotion Dynamics Dashboard
The standalone HTML dashboard provides:

- **Valence/Arousal Trajectory Chart**: Line chart showing emotional valence and arousal across utterances
- **Aggregated Discrete Emotions**: Bar chart of average discrete emotion intensities across utterances
- **KPI Section**: Key metrics including:
  - Utterance count with metadata
  - Home base valence/arousal values
  - Emotional variability and intensity levels
- **UED Metrics Display**: Shows User Emotional Dynamics metrics from the skill output
- **Psychological Lenses**: Displays qualitative descriptions from the analysis
- **JSON Input**: Text areas to paste JSON outputs from skills directly

### Technical Implementation
- Single HTML file with embedded CSS and JavaScript
- Uses Chart.js for data visualization
- Responsive dark-themed UI design
- Real-time visualization of emotion dynamics data
- Error handling for invalid JSON

## Psychoanalytic Fusion Skill

The `Skill-emotion-marker-psych` directory contains specifications for a meta-level skill that:

- Combines LeanDeep markers with emotion dynamics
- Applies a psychoanalytic lens (conflicts, defense, transference)
- Optionally uses brainstorming to generate focus hypotheses
- Outputs structured JSON with evidence-based inferences
- Provides coach next actions as implementable steps

## Usage Instructions

### For Dashboard
1. Open `emotion-dynamics-dashboard.html` in a web browser
2. Paste JSON output from the emotion dynamics skill into the text area
3. Click "JSON laden & visualisieren" to load and visualize the data
4. Use "Zurücksetzen" to clear all data and start over

### For Sample Data
Use the `sample-emotion-dynamics.json` file to test the dashboard functionality.

## Integration Capabilities

The dashboard is designed to work with the expected JSON formats from the emotion dynamics and marker annotation skills. It respects the LeanDeep marker architecture and can potentially be extended to visualize the output from the psychoanalytic fusion skill as well.