# Agent Guidelines

## After Every Code Change

Run ruff formatting and auto-fix after every file modification:

```bash
uv run ruff format .
uv run ruff check --fix .
```

## Refactoring

- When refactoring, always update the corresponding tests in `tests/` to match the new structure/signatures.
- Do not leave tests that reference old APIs or removed code.
- Backward compatibility is generally not required — rename, restructure, and break interfaces freely when it improves the codebase.
