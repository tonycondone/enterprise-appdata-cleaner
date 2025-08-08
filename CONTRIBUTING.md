# Contributing to Enterprise AppData Deep Clean Suite

Thank you for your interest in contributing to the Enterprise AppData Deep Clean Suite! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Windows 10/11 or Windows Server 2016+
- Administrative privileges (for testing)

### Development Setup

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/your-username/enterprise-appdata-cleaner.git
   cd enterprise-appdata-cleaner
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Unix/MacOS
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install development dependencies**
   ```bash
   pip install pytest black flake8 mypy
   ```

## 🔧 Development Guidelines

### Code Style

We follow PEP 8 style guidelines. Use the following tools:

```bash
# Format code with black
black cleaner.py

# Check code style with flake8
flake8 cleaner.py

# Type checking with mypy
mypy cleaner.py
```

### Code Standards

- **Type Hints**: All functions must have type hints
- **Docstrings**: All functions must have docstrings following Google style
- **Error Handling**: Comprehensive error handling with appropriate logging
- **Security**: Follow security best practices for enterprise software
- **Testing**: Write unit tests for new features

### Example Function Structure

```python
def example_function(param1: str, param2: int) -> Dict[str, Any]:
    """
    Brief description of what the function does.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Dictionary containing the result
        
    Raises:
        ValueError: If parameters are invalid
        OSError: If file operations fail
    """
    try:
        # Implementation here
        result = {}
        return result
    except Exception as e:
        logger.error(f"Function failed: {e}")
        raise
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=cleaner

# Run specific test file
pytest tests/test_cleaner.py
```

### Writing Tests

Create tests in the `tests/` directory. Example test structure:

```python
import pytest
from pathlib import Path
from cleaner import EnterpriseAppDataCleaner

class TestEnterpriseAppDataCleaner:
    def test_initialization(self):
        """Test cleaner initialization"""
        cleaner = EnterpriseAppDataCleaner(dry_run=True)
        assert cleaner.dry_run is True
        
    def test_configuration_loading(self):
        """Test configuration loading"""
        cleaner = EnterpriseAppDataCleaner()
        assert 'enterprise' in cleaner.config
        assert 'security' in cleaner.config
```

## 📝 Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make your changes**
   - Follow the coding standards
   - Add tests for new functionality
   - Update documentation if needed

3. **Test your changes**
   ```bash
   # Run tests
   pytest
   
   # Test the script
   python cleaner.py --dry-run --validate
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add amazing feature"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Create a Pull Request**
   - Provide a clear description of the changes
   - Include any relevant issue numbers
   - Add screenshots if UI changes are involved

### Pull Request Guidelines

- **Title**: Clear, descriptive title
- **Description**: Detailed description of changes
- **Testing**: Describe how you tested the changes
- **Breaking Changes**: Note any breaking changes
- **Documentation**: Update documentation if needed

## 🐛 Bug Reports

### Before Submitting a Bug Report

1. Check if the issue has already been reported
2. Try to reproduce the issue with the latest version
3. Check the logs for error messages

### Bug Report Template

```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run command '...'
2. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Environment:**
- OS: Windows 10/11
- Python version: 3.8+
- Cleaner version: 1.2.0

**Additional context**
Add any other context about the problem here.
```

## 💡 Feature Requests

### Before Submitting a Feature Request

1. Check if the feature has already been requested
2. Consider if the feature aligns with the project's goals
3. Think about the implementation complexity

### Feature Request Template

```markdown
**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is.

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions.

**Additional context**
Add any other context or screenshots about the feature request.
```

## 📚 Documentation

### Contributing to Documentation

- Update README.md for user-facing changes
- Add docstrings for new functions
- Update configuration examples if needed
- Create new documentation files for major features

### Documentation Standards

- Use clear, concise language
- Include code examples
- Add screenshots for UI features
- Keep documentation up to date

## 🔒 Security

### Security Guidelines

- Never commit sensitive information (passwords, API keys, etc.)
- Follow secure coding practices
- Report security vulnerabilities privately
- Test security features thoroughly

### Reporting Security Issues

If you discover a security vulnerability, please report it privately:

1. **Email**: security@company.com
2. **Subject**: "Security Vulnerability in Enterprise AppData Cleaner"
3. **Include**: Detailed description and steps to reproduce

## 🏷️ Release Process

### Version Numbers

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### Release Checklist

- [ ] Update version in setup.py
- [ ] Update CHANGELOG.md
- [ ] Run all tests
- [ ] Test on different Windows versions
- [ ] Update documentation
- [ ] Create release notes

## 🤝 Community

### Getting Help

- **Issues**: Use GitHub issues for bugs and feature requests
- **Discussions**: Use GitHub discussions for questions
- **Wiki**: Check the project wiki for additional documentation

### Code of Conduct

- Be respectful and inclusive
- Help others learn and grow
- Provide constructive feedback
- Follow the project's coding standards

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the Enterprise AppData Deep Clean Suite! 🎉 