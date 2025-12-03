# Qwen Code - Skills Framework

## Project Overview

This directory contains a comprehensive collection of "Skills" - specialized AI agent behaviors designed to perform specific, well-defined tasks. Each skill is a self-contained unit of functionality that can be invoked by AI agents to perform specialized functions, from analyzing text through marker engines to creating coloring books.

### Architecture Overview

The Skills framework is organized as follows:

- **Individual Skill Directories**: Each skill is contained in its own directory with a standardized structure
- **Core Files**: Each skill typically includes a `SKILL.md` file that defines its behavior
- **Supporting Assets**: Skills may include `references/`, `assets/`, and `scripts/` directories for additional resources
- **Standardized Structure**: Skills follow a consistent format with YAML frontmatter specifying name and description

### Skill Structure

Each skill follows the pattern:

```
skill-name/
├── SKILL.md          # Primary skill definition with YAML frontmatter
├── references/       # Optional reference materials, schemas, guidelines
├── assets/           # Optional templates, examples, or static resources
├── scripts/          # Optional helper scripts
└── examples/         # Optional examples (if included)
```

The `SKILL.md` file contains:

- **YAML Frontmatter**: `name` and `description` fields
- **Usage Guidelines**: When to use the skill
- **Workflow Instructions**: Step-by-step procedures for the AI to follow
- **Output Format**: Expected response format
- **Examples**: Sample inputs and outputs

### Core Skill Types

The repository contains several categories of skills:

- **Therapeutic/Mental Health**: Skills for analysis using LeanDeep marker engines (ATO→SEM→CLU→MEMA), emotion dynamics, psychoanalytic analysis
- **Project Management**: Skills for kanban, business engineering, scrum, and general project planning
- **Content Creation**: Skills for creating coloring books, blog outlines, LinkedIn posts, and other content
- **Analysis**: Skills for root cause analysis, interview analysis, and other analytical tasks
- **Development Tools**: Skills for generating agent systems, prompt engineering, and coding tasks

### Key Concepts

**LeanDeep (LD) Marker Engine**: Many skills use a hierarchical marker system:
- **ATO (Atomic)**: Individual words, phrases, signals
- **SEM (Semantic)**: Combinations of ATOs that create deeper meaning
- **CLU (Cluster)**: Patterns within time windows or conversation segments
- **MEMA (Meta-Marker)**: Global patterns across the entire thread

**Superpowers**: Some skills support special flags like `/superpowers:brainstorm` to enable additional functionality.

## Building and Running

The Skills framework is a collection of definitions rather than a runnable application. To utilize these skills:

1. Each skill contains its own instructions in its `SKILL.md` file
2. Skills are typically invoked by AI agents that understand the skill format
3. The `skill-trainer-architect` skill can be used to create new skills by generating the proper file structure
4. Skills may reference external files and schemas located in their respective directories

To use a skill, an AI agent should:
1. Read the `SKILL.md` file for the desired skill
2. Follow the workflow instructions provided in the skill definition
3. Process according to the specified inputs and expected outputs
4. Adhere to the style rules and constraints defined in the skill

## Development Conventions

### Skill Creation Standards

- **File Naming**: Directories and skills use `hyphen-case` (e.g., `skill-emotion-dynamics`)
- **YAML Frontmatter**: All skills must include `name` and `description` fields
- **Clear Instructions**: Workflows must be detailed, step-by-step procedures
- **Output Format**: Each skill must specify its expected output format
- **Examples**: Skills should include at least two realistic examples

### Content Guidelines

- **Style**: Instructions are written in imperative and objective form (no first person or direct address to user)
- **Completeness**: No placeholders or TODOs; all sections must be fully specified
- **Clarity**: Use clear, unambiguous language with specific instructions
- **Scope**: Each skill focuses on a single, well-defined behavior

### Directory Organization

- Skills are organized in clearly named directories
- Supporting files are placed in appropriately named subdirectories (`references/`, `assets/`, etc.)
- File names should be descriptive and follow consistent naming patterns

The Skills framework represents a systematic approach to creating reusable, well-defined AI behaviors that can be invoked consistently across different contexts and applications.