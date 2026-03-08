# Contributing to SoulBot

Thank you for your interest in contributing to SoulBot! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/<your-username>/SoulBot.git`
3. Install in development mode: `pip install -e ".[dev]"`
4. Create a branch: `git checkout -b feature/your-feature`

## Development Setup

```bash
# Install all development dependencies
pip install -e ".[dev,telegram,sqlite]"

# Run tests
python -m pytest tests/ -q

# Run linter
ruff check src/
```

## How to Contribute

### Reporting Issues

- Use [GitHub Issues](https://github.com/AIXP-Foundation/SoulBot/issues) to report bugs or suggest features
- Include Python version, OS, and LLM CLI tool version
- Provide minimal reproduction steps

### Submitting Changes

1. **Create an issue** first for non-trivial changes
2. **Write tests** for new features or bug fixes
3. **Follow existing code style** — the project uses `ruff` for linting
4. **Keep commits focused** — one logical change per commit
5. **Use descriptive commit messages** following [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat: add new tool type`
   - `fix: handle empty response in ACP client`
   - `docs: update CLI usage examples`
   - `test: add session persistence tests`

### Pull Request Process

1. Update documentation if your change affects user-facing behavior
2. Ensure all tests pass: `python -m pytest tests/ -q`
3. Ensure linting passes: `ruff check src/`
4. Submit a PR to the `main` branch
5. Fill in the PR template with a clear description

## Code Guidelines

### Project Structure

- `src/soulbot/` — Framework source code
- `tests/` — Unit and integration tests
- `examples/` — Example agents
- `docs/` — Documentation

### Style

- Python 3.11+ type hints required
- Max line length: 100 characters (configured in `pyproject.toml`)
- Docstrings for public functions and classes
- No wildcard imports

### Testing

- All new features must include tests
- Use `pytest` with `pytest-asyncio` for async tests
- Place tests in `tests/` mirroring the source structure
- Mark end-to-end tests with `@pytest.mark.live`

### AISOP / AIAP Contributions

Changes to AISOP blueprints (`.aisop.json`) or AIAP packages (`*_aiap/`) should:

- Follow the [AIAP Protocol](https://github.com/AIXP-Foundation/AIAP) specification
- Maintain deterministic execution paths in mermaid graphs
- Include governance metadata in `AIAP.md` for new packages

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.
