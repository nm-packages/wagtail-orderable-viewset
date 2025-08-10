
# Wagtail Orderable ViewSet

Add drag-and-drop ordering to Wagtail's SnippetViewSet and ModelViewSet in the admin panel.

## Overview

Wagtail Orderable ViewSet brings modern, AJAX-powered ordering to Wagtail's ViewSet system. It is inspired by [wagtail-orderable](https://github.com/elton2048/wagtail-orderable) and designed for Wagtail 7+ and Django 4.2+.

## Features

- Drag-and-drop ordering for SnippetViewSet and ModelViewSet
- AJAX order updates
- Custom ordering field support
- Seamless integration with Wagtail admin UI
- Visual feedback during drag operations

## Installation

```bash
pip install wagtail-orderable-viewset
```

## Quick Start

See [docs/example.md](docs/example.md) for a full example project, including model/snippet setup and data seeding.

## Usage

### For models

```python
from wagtail_orderable_viewset.viewset import OrderableModelViewSet
from .models import Testimonial

class TestimonialViewSet(OrderableModelViewSet):
	model = Testimonial
	list_display = ["name", "company", "rating", "sort_order"]
	search_fields = ["name", "company", "content"]
```

Register your viewset with Wagtail using hooks:

```python
from wagtail import hooks
testimonial_viewset = TestimonialViewSet("testimonial")

@hooks.register("register_admin_viewset")
def register_testimonial_viewset():
	return testimonial_viewset
```

### For snippets

```python
from wagtail_orderable_viewset.viewset import OrderableSnippetViewSet
from .models import Person

class PersonViewSet(OrderableSnippetViewSet):
	model = Person
	list_display = ["name", "team", "sort_order"]
```

## Requirements

- Python 3.9+
- Django 4.2+
- Wagtail 7.0+

## Development

### Setup

```bash
git clone https://github.com/nickmoreton/wagtail-orderable-viewset.git
cd wagtail-orderable-viewset
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Running Tests

```bash
python runtests.py
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

MIT License. See LICENSE for details.

## Acknowledgments

Inspired by [wagtail-orderable](https://github.com/elton2048/wagtail-orderable) and built for Wagtail's ViewSet system.
