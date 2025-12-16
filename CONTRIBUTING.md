# Contributing to Lottery Analysis System

Thank you for your interest in contributing to the Lottery Analysis System! This document provides guidelines for contributing to the project.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Process](#development-process)
4. [Coding Standards](#coding-standards)
5. [Testing Guidelines](#testing-guidelines)
6. [Submitting Changes](#submitting-changes)

---

## Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in all interactions.

### Expected Behavior
- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

---

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Git for version control
- Basic understanding of lottery systems and statistics

### Setting Up Development Environment

1. **Fork the Repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/lottery-system.git
   cd lottery-system
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e .  # Install in development mode
   ```

4. **Verify Installation**
   ```bash
   python tests/test_core_modules.py
   python demo_cli.py
   ```

---

## Development Process

### Branching Strategy

- `main`: Stable release branch
- `develop`: Development branch for next release
- `feature/*`: New features
- `bugfix/*`: Bug fixes
- `hotfix/*`: Critical fixes for production

### Creating a Feature Branch

```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

### Commit Messages

Follow conventional commit format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Example:**
```
feat(prediction): add neural network prediction algorithm

Implement a new prediction algorithm using a simple neural network
that learns from historical lottery data patterns.

Closes #123
```

---

## Coding Standards

### Python Style Guide

Follow PEP 8 with these specifics:

1. **Indentation**: 4 spaces (no tabs)
2. **Line Length**: Maximum 100 characters
3. **Imports**: 
   - Standard library first
   - Third-party libraries second
   - Local imports last
   - Alphabetically within each group

4. **Naming Conventions**:
   - Classes: `PascalCase`
   - Functions/methods: `snake_case`
   - Constants: `UPPER_SNAKE_CASE`
   - Private methods: `_leading_underscore`

5. **Documentation**:
   - All modules must have docstrings
   - All public functions/classes must have docstrings
   - Use Google-style docstrings

### Example Code

```python
"""
Module for lottery number prediction.

This module provides algorithms for predicting lottery numbers
based on historical data analysis.
"""

import numpy as np
from typing import List, Dict, Optional


class PredictionEngine:
    """Generates lottery number predictions using various algorithms."""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the prediction engine.
        
        Args:
            config: Optional configuration dictionary.
        """
        self.config = config or {}
    
    def predict(self, data: np.ndarray, count: int = 6) -> List[int]:
        """
        Generate lottery number predictions.
        
        Args:
            data: Historical lottery data as numpy array.
            count: Number of predictions to generate.
            
        Returns:
            List of predicted lottery numbers.
            
        Raises:
            ValueError: If count is invalid or data is empty.
        """
        if count < 1:
            raise ValueError("Count must be positive")
        
        # Implementation here
        return []
```

### Type Hints

Use type hints for all function parameters and return values:

```python
from typing import List, Dict, Optional, Tuple

def analyze_data(data: pd.DataFrame, 
                window: int = 30) -> Dict[str, any]:
    """Analyze lottery data within a specified window."""
    pass
```

---

## Testing Guidelines

### Test Requirements

1. **Coverage**: Aim for >80% code coverage
2. **Unit Tests**: Test individual functions/methods
3. **Integration Tests**: Test module interactions
4. **Edge Cases**: Test boundary conditions and error cases

### Writing Tests

```python
def test_prediction_engine():
    """Test prediction engine functionality."""
    # Arrange
    engine = PredictionEngine()
    test_data = create_test_data()
    
    # Act
    predictions = engine.predict(test_data, count=6)
    
    # Assert
    assert len(predictions) == 6
    assert all(1 <= n <= 49 for n in predictions)
```

### Running Tests

```bash
# Run all tests
python tests/test_core_modules.py

# Run specific test
python -m pytest tests/test_core_modules.py::test_prediction_engine

# Run with coverage
python -m pytest --cov=src tests/
```

---

## Submitting Changes

### Pull Request Process

1. **Update Documentation**
   - Update README if features changed
   - Add/update docstrings
   - Update FEATURES.md if applicable

2. **Test Your Changes**
   ```bash
   python tests/test_core_modules.py
   python demo_cli.py
   ```

3. **Create Pull Request**
   - Title: Clear, descriptive summary
   - Description: 
     - What changed
     - Why it changed
     - How to test it
   - Reference related issues

4. **Code Review**
   - Address reviewer feedback
   - Keep discussion constructive
   - Make requested changes promptly

5. **Merge Requirements**
   - All tests pass
   - Code review approved
   - Documentation updated
   - No merge conflicts

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe the tests you ran

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed the code
- [ ] Commented complex code
- [ ] Updated documentation
- [ ] Added/updated tests
- [ ] All tests pass
```

---

## Areas for Contribution

### High Priority
- [ ] Mobile UI implementation (Kivy)
- [ ] Additional prediction algorithms
- [ ] Performance optimizations
- [ ] More comprehensive tests
- [ ] Multi-language support

### Medium Priority
- [ ] Database integration (SQLite)
- [ ] QR code scanning feature
- [ ] Live lottery data fetching
- [ ] Export to PDF
- [ ] Advanced visualizations

### Documentation
- [ ] Video tutorials
- [ ] API documentation
- [ ] Usage examples
- [ ] Troubleshooting guide
- [ ] Architecture diagrams

---

## Questions or Problems?

### Getting Help

- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions
- **Email**: contact@lotteryanalysis.org (if available)

### Reporting Bugs

Use the bug report template:

```markdown
**Describe the bug**
Clear description of the bug

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen

**Screenshots**
If applicable, add screenshots

**Environment:**
- OS: [e.g., Windows 10]
- Python Version: [e.g., 3.9]
- App Version: [e.g., 1.0.0]

**Additional context**
Any other relevant information
```

---

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in the application About dialog

Thank you for contributing to the Lottery Analysis System! 🎉
