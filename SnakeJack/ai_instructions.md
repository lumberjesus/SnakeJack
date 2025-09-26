# AI Instructions

This file contains instructions and context for AI assistants working with this codebase.

## Project Context

SnakeJack is a Python implementation of a Blackjack game, converted from the original C# implementation (SharpJack). The project aims to maintain clean, well-documented, and thoroughly tested Python code while following modern Python best practices.

## Code Style Guidelines

- Use type hints for all function parameters and return values
- Document all classes and functions with proper docstrings
- Follow PEP 8 style guidelines
- Use dataclasses where appropriate
- Prefer composition over inheritance
- Keep functions and methods focused and single-purpose
- Use descriptive variable names

## Testing Requirements

- Maintain test coverage above 90%
- Include both unit tests and integration tests
- Test edge cases and error conditions
- Mock external dependencies when necessary
- Use pytest fixtures for test setup
- Include docstrings in test functions explaining test purpose

## Project Structure

```
src/snakejack/
├── models/          # Core game entities
│   ├── card.py     # Card class
│   ├── deck.py     # Deck class
│   └── player.py   # Player class
├── game/           # Game logic
│   └── blackjack.py # Main game implementation
└── __main__.py     # CLI entry point
```

## Dependencies

- Python 3.7+
- pytest for testing
- black for code formatting
- isort for import sorting
- pylint for code quality checks

## Development Process

1. Write tests first (TDD approach)
2. Update documentation with code changes
3. Ensure type hints are complete
4. Run full test suite before committing
5. Keep commits focused and atomic

## Important Considerations

- The game should handle edge cases gracefully
- User input should be validated
- Error messages should be clear and helpful
- Performance is secondary to code clarity
<!-- - Maintain backward compatibility when possible -->

## Future Plans

 - Add GUI interface
- Implement multiplayer support
- Add game statistics tracking
- Support different rule variations

## Security Considerations

- Validate all user input
- Don't expose internal state unnecessarily
- Handle errors gracefully without exposing implementation details

## Documentation Requirements

- Keep README.md updated with new features
- Document all public APIs
- Include examples in docstrings
- Update this file with new guidelines as needed

This file should be updated whenever there are changes to project requirements, coding standards, or general guidelines that AI assistants should follow.