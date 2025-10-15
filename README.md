# embedsmith

###  EmbedSmith is a simple CLI tool written in python for generating boiler plates for embedded projects with varius MCU's supported. 


[![Cirrus CI - Default Branch Build Status](https://img.shields.io/cirrus/github/:clementcole/:embedsmith)](https://github.com/clementcole/embedsmith/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/embedsmith.svg)](https://pypi.org/project/embedsmith/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/embedded-project-creator.svg)](https://pypi.org/project/embedded-project-creator/)

A Python package for creating standardized embedded project layouts with proper structure, build systems, and development tools.

## Features

- 🏗️ Standardized project structure for embedded development
- 🔧 Configurable MCU settings and toolchains
- 📁 Template-based file generation
- 🛠️ Pre-configured Makefile build system
- 📚 Organized directories for source, headers, tests, and docs
- 🎯 Command-line interface and Python API
- 🔄 GitHub Actions for CI/CD
- 
---

## Installation

```bash
pip install embedsmith
```
---

## Quick Start
```bash
# Create a default project
embedsmith my-project

# Create with custom configuration
embedsmith --mcu cortex-m7 --flash-size 1M --ram-size 512K

# Create in current directory (overwrite if exists
embedsmith . --overwrite
```
---

## Python API
```python
from embedsmith import embedsmith, ProjectConfig

# Create with default configuration
embedsmith("my-project")

# Create with custom configuration
config = ProjectConfig(
    project_name="stm32-firmware",
    mcu="cortex-m7",
    compiler="arm-none-eabi-gcc",
    flash_size="1M",
    ram_size="512K",
    author="Your Name",
    version="1.0.0"
)
embedsmith("custom-project", config=config)
```
---
## Output Folder For Sample Embedded System Project

```text
embedded-system-project-folder/
├── firmware/
│   ├── src/           # Source files
│   ├── include/       # Header files
│   ├── linker_scripts/# Memory configuration
│   ├── build/         # Build artifacts
│   └── Makefile       # Build system
├── tools/
│   ├── scripts/       # Utility scripts
│   └── configs/       # Tool configurations
├── tests/             # Test files
├── docs/              # Documentation
├── hardware/          # Hardware designs
└── project_config.json # Project configuration
```

---
# Development

## Setup Development Env.
```bash
git clone https://github.com/clementcole/embedsmith.git
cd embedsmith
pip install -r requirements-dev.txt
pip install -e .
```


## Running Tests
```bash
pytest tests/ -v
```

## Sanity Checks 
```bash
black embedded_project_creator tests
isort embedded_project_creator tests
flake8 embedded_project_creator tests
mypy embedded_project_creator
```

## GitHub Actions
- CI: Automated testing on multiple Python versions
- Linting: Code style and quality checks
- Release: Automated PyPI publishing on tag creation

## Welcoming All Contributions:
1. Fork the repository.
2. Create a feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'Add amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request