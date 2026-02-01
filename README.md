# VKR_program

GOST Document Validator - A Python application for validating Russian technical documents according to GOST standards.

## Project Structure

```
gost_validator/
├── config/          # Configuration settings
├── models/          # Data models
├── services/        # Business logic services
├── utils/           # Utility functions
├── validators/      # Validation rules
└── main.py          # Entry point
```

## Installation

1. Create virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

```bash
python gost_validator/main.py
```

## Requirements

- Python 3.8+
- python-docx>=0.8.11

## Author

DABychkov
