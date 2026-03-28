# GitHub Copilot Instructions for Lottery System

## Project Overview

This is a **cross-platform lottery analysis and prediction system** built with Python. The system provides comprehensive lottery data analysis, prediction capabilities, and user management features.

## Architecture & Structure

### Current Architecture
- **Frontend + Backend with Authentication**: The system follows a full-stack architecture with authentication mechanisms
- **Modular Design**: Organized in a hierarchical structure:
  - `items/` - Core items and resources
  - `orders/` - Order management system
  - `bets/` - Betting functionality

### Technology Stack
- **Primary Language**: Python (for analysis and prediction)
- **Architecture Pattern**: Modular, hierarchical structure with separation of concerns
- **Authentication**: Integrated auth system for user management

## Development Guidelines

### Coding Conventions

1. **Language Standards**
   - Follow PEP 8 style guide for Python code
   - Use meaningful variable and function names in English
   - Add docstrings for all public functions and classes
   - Type hints are recommended for function signatures

2. **File Organization**
   - Keep related functionality grouped in modules
   - Maintain the hierarchical structure: items → orders → bets
   - Separate concerns: authentication, business logic, data access

3. **Documentation**
   - Document all public APIs and interfaces
   - Include usage examples in docstrings
   - Update README.md when adding major features
   - Comment complex algorithms and business logic

### Architecture Patterns

1. **Separation of Concerns**
   - Authentication logic should be isolated from business logic
   - Keep data models separate from business logic
   - Use service layers for complex operations

2. **Modularity**
   - Design components to be reusable and testable
   - Avoid tight coupling between modules
   - Use dependency injection where appropriate

3. **Error Handling**
   - Implement comprehensive error handling
   - Use specific exception types
   - Log errors appropriately for debugging
   - Provide meaningful error messages to users

## Integration Points

### Authentication System
- The system includes an authentication layer (`auth`)
- Ensure all protected endpoints verify user authentication
- Handle authentication failures gracefully

### Data Flow
- **Items** → **Orders** → **Bets**: Follow this hierarchy when implementing features
- Maintain data consistency across the hierarchy
- Use appropriate validation at each level

## Development Workflow

### Making Changes

1. **Before Starting**
   - Understand the current module structure
   - Review related code in the same module
   - Check for existing similar functionality

2. **During Development**
   - Write clean, readable code
   - Follow the existing code style
   - Add appropriate comments for complex logic
   - Consider edge cases and error scenarios

3. **Testing**
   - Test authentication flows thoroughly
   - Verify data integrity across the hierarchy
   - Test edge cases and error conditions
   - Validate input data

4. **Documentation**
   - Update relevant documentation
   - Add code comments for non-obvious logic
   - Update API documentation if applicable

### Code Quality Standards

1. **Readability**
   - Use clear, descriptive names
   - Keep functions focused and concise
   - Avoid deep nesting (max 3-4 levels)
   - Use meaningful variable names

2. **Maintainability**
   - Write self-documenting code
   - Avoid code duplication (DRY principle)
   - Keep functions under 50 lines when possible
   - Refactor complex code

3. **Security**
   - Never hardcode credentials or secrets
   - Validate and sanitize all user inputs
   - Use parameterized queries to prevent SQL injection
   - Implement proper authentication and authorization
   - Follow security best practices for sensitive data

## Project-Specific Guidelines

### Lottery System Context

1. **Data Accuracy**
   - Lottery predictions must be based on statistical analysis
   - Validate all lottery data inputs
   - Handle edge cases in lottery number ranges
   - Ensure data integrity for historical lottery results

2. **User Experience**
   - Provide clear feedback on predictions
   - Handle errors gracefully with user-friendly messages
   - Ensure responsive design for cross-platform support
   - Optimize performance for data-intensive operations

3. **Business Logic**
   - Betting rules should be clearly defined and enforced
   - Order processing must maintain transaction integrity
   - User balances and transactions must be accurate
   - Implement audit trails for financial transactions

### Common Patterns

1. **Authentication Flow**
   ```python
   # Verify user authentication before processing requests
   # Handle authentication failures with appropriate responses
   # Log authentication attempts for security
   ```

2. **Data Validation**
   ```python
   # Validate all inputs at the entry point
   # Use type hints and validation libraries
   # Return clear error messages for invalid data
   ```

3. **Error Handling**
   ```python
   # Use try-except blocks appropriately
   # Log errors with sufficient context
   # Return user-friendly error messages
   # Don't expose sensitive information in errors
   ```

## Testing Approach

### Test Coverage
- Write unit tests for business logic
- Test authentication flows
- Validate data integrity in integration tests
- Test edge cases and error conditions

### Test Organization
- Keep tests close to the code they test
- Use descriptive test names
- Follow the Arrange-Act-Assert pattern
- Mock external dependencies

## Dependencies & Tools

### Package Management
- Document all dependencies clearly
- Keep dependencies up to date
- Use virtual environments for Python projects
- Pin versions for production dependencies

### Build & Development Tools
- Use linters (pylint, flake8) for code quality
- Format code with black or autopep8
- Use pre-commit hooks for consistency

## AI Agent Guidance

When working on this codebase:

1. **Understand Context First**
   - Review the hierarchical structure: items → orders → bets
   - Check authentication requirements for the feature
   - Consider the lottery system domain context

2. **Follow Patterns**
   - Use existing patterns for similar functionality
   - Maintain consistency with the codebase style
   - Respect the modular architecture

3. **Security First**
   - Always validate and sanitize inputs
   - Never expose sensitive data
   - Follow authentication/authorization patterns
   - Be mindful of financial transaction integrity

4. **Documentation**
   - Document your changes clearly
   - Update relevant documentation files
   - Add comments for complex business logic

5. **Testing**
   - Verify your changes don't break existing functionality
   - Test authentication flows if modified
   - Validate data integrity

## Additional Resources

- **README.md**: Project overview and setup instructions
- **Authentication Module**: Located in `完整原型：前端 + 后端 — auth/`
- **Core Modules**: Items, Orders, and Bets hierarchy

## Notes for AI Assistants

- This is a lottery system with financial implications - accuracy and security are paramount
- The codebase uses Chinese folder names with English code - be mindful of this duality
- Authentication is a core component - always consider auth requirements
- Follow the hierarchical structure when adding features
- Maintain data integrity across the items → orders → bets flow
