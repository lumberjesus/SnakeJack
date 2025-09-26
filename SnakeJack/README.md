# SnakeJack

A Python implementation of BlackJack, converted from the original C# SharpJack implementation.

## Installation

```bash
pip install -e .
```

## Development Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Running Tests

```bash
pytest tests/
```