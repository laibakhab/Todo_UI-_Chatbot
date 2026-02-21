# ADR: Storage and Architecture for Todo Console App

## Status

Proposed

## Context

The Hackathon requires a simple in-memory console application to implement basic todo features using spec-driven development. The application needs to store tasks in memory during the session with auto-incrementing IDs and follow a modular structure with clean code principles. The decision needs to balance simplicity, compliance with the constitution (no external dependencies), and future evolution to Phase II.

## Decision

We will implement the following architectural decisions as a cohesive approach:

- **Storage Strategy**: Use a global dictionary for task storage with auto-incrementing integer IDs for efficient lookups
- **Project Structure**: Implement a modular design with separate files (models.py for data, services.py for business logic, cli.py for user interface)
- **Environment Management**: Use UV for Python environment and dependency management as specified in the requirements
- **Testing Strategy**: Optional pytest integration for TDD practices (as needed)

## Alternatives Considered

1. **List vs Dictionary for Storage**:
   - Alternative: Use a Python list to store tasks
   - Tradeoff: Lists would require iteration for ID lookups, making operations O(n) vs O(1) for dictionary access
   - Chosen: Dictionary for better performance when accessing tasks by ID

2. **No Environment Manager vs UV**:
   - Alternative: Skip environment management tools and use standard venv
   - Tradeoff: UV provides more modern Python project management but the PDF specifically mentions its use
   - Chosen: UV as specified in requirements

3. **Monolithic vs Modular Structure**:
   - Alternative: Single file implementation for maximum simplicity
   - Tradeoff: Single file would violate clean code principles and proper Python project structure requirements
   - Chosen: Modular approach for better maintainability and compliance with constitution

## Consequences

**Positive**:
- Simple implementation that aligns with "Simplicity" principle in constitution
- No external dependencies beyond Python standard library (except UV for management)
- Efficient O(1) task lookup by ID using dictionary
- Clear separation of concerns supporting clean code principles
- Easy evolution to Phase II with potential persistence layer
- Follows proper Python project structure requirements

**Negative**:
- No data persistence between sessions (ephemeral storage by design)
- Global state creates potential challenges for testing
- Single-user session only (by design for this phase)

## References

- specs/phase1-console/spec.md
- specs/phase1-console/plan.md
- .specify/memory/constitution.md (Simplicity and Clean Code principles)
- CLAUDE.md (for Claude Code instructions)