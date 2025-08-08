# Wagtail Orderable ViewSet

Add drag-and-drop ordering functionality to Wagtail's SnippetViewSet and ModelViewSet in the admin panel.

## Overview

This package provides ordering functionality for Wagtail's ViewSet system, similar to what [wagtail-orderable](https://github.com/elton2048/wagtail-orderable) provided for the deprecated wagtail-modeladmin package.

## Features

- Drag-and-drop ordering for SnippetViewSet and ModelViewSet
- AJAX-powered order updates
- Custom ordering field support
- Integration with Wagtail's existing admin UI
- Mobile-friendly touch support
- Visual feedback during drag operations

## Installation

```bash
pip install wagtail-orderable-viewset
```

## Quick Start

For end-to-end setup, models/snippets examples, and seeding data, see the example guide:

[docs/example.md](docs/example.md)

## Advanced Usage

See `docs/example.md` for custom ordering fields and additional patterns.

## Requirements

- Python 3.9+
- Django 4.2+
- Wagtail 7.0+

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/nickmoreton/wagtail-orderable-viewset.git
cd wagtail-orderable-viewset

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
```

### Running Tests

```bash
python -m pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

This package is inspired by the [wagtail-orderable](https://github.com/elton2048/wagtail-orderable) package and aims to provide similar functionality for Wagtail's modern ViewSet system.
