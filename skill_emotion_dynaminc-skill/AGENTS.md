# Repository Guidelines

## Project Structure & Module Organization
- Current files: `Blueprint.md` documents the scope and behavior.
- Proposed layout once code lands:
  - `src/` – production code (organize by feature/module).
  - `tests/` – mirrors `src/` structure; one test file per module.
  - `assets/` – data, prompts, and example inputs.
  - `scripts/` – one-off utilities (setup, lint, release).

## Build, Test, and Development Commands
- Until tooling is added, prefer Make targets or package scripts. Examples:
  - `make setup` – install deps and pre-commit hooks.
  - `make test` – run unit tests locally.
  - `make lint` – run formatters/linters.
- If no Makefile:
  - Python: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && pytest`.
  - Node: `npm ci && npm test`.

## Coding Style & Naming Conventions
- Indentation: 4 spaces; line length target 100.
- Naming: `snake_case` for files/functions, `PascalCase` for classes, `kebab-case` for CLI/task names.
- Prefer docstrings/comments that explain “why,” not “what.”
- If using Python, adopt Black + Ruff; if JS/TS, Prettier + ESLint. Add configs to `scripts/` or root.

## Testing Guidelines
- Place tests in `tests/` with `test_*.py` (Python) or `*.spec.ts` (TS) naming.
- Aim for ≥80% coverage on core modules.
- Write focused, deterministic unit tests; add integration tests for cross-module flows.
- Example: `pytest -q` or `npm test --silent`.

## Commit & Pull Request Guidelines
- Use Conventional Commits (e.g., `feat: add emotion normalizer`).
- Keep commits small and logically scoped; reference issues (`#123`).
- PRs should include: purpose, approach, before/after notes, and links to relevant `Blueprint.md` sections. Add screenshots or logs if behavior-facing.

## Security & Configuration Tips
- Do not commit secrets. Use `.env` with a checked-in `.env.example` and document keys.
- Prefer explicit version pins for reproducibility.

## Agent-Specific Instructions
- Respect this guide repo-wide. Defer to a deeper AGENTS.md in subfolders if present.
- Keep changes minimal, documented, and aligned with `Blueprint.md` intent.
