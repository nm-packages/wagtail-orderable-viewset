
# Wagtail Orderable ViewSet

Add drag-and-drop ordering to Wagtail's SnippetViewSet and ModelViewSet in the admin panel.

Note: the feature is planned for a [future release](https://github.com/wagtail/wagtail/pull/12857) of Wagtail core.

## Overview

Wagtail Orderable ViewSet brings, AJAX-powered ordering to Wagtail's ViewSet system. It is inspired by [wagtail-orderable](https://github.com/elton2048/wagtail-orderable) and designed for Wagtail 7+ and Django 4.2+.

Wagtail core may eventually include this functionality: https://github.com/wagtail/wagtail/pull/12857

## Features

- Drag-and-drop ordering for SnippetViewSet and ModelViewSet
- An IncrementingOrderable model mixin

## Installation

```bash
pip install wagtail-orderable-viewset
```

## Quick Start

See [docs/example.md](docs/example.md) for a full example project, including model/snippet setup and data seeding.

## Requirements

- Python 3.9+
- Django 4.2+
- Wagtail 7.0+

## Development

Clone the repository:

```bash
git clone https://github.com/nickmoreton/wagtail-orderable-viewset.git
```

and change to the directory: `cd wagtail-orderable-viewset`

### Setup

Using UV <https://docs.astral.sh/uv/>

```bash
uv sync
```

### Running Tests

```bash
uv run python runtests.py
```

## Contributing

Contributions are welcome! Please open an [issue](https://github.com/nm-packages/wagtail-orderable-viewset/issues) or submit a [pull request](https://github.com/nm-packages/wagtail-orderable-viewset/pulls).

## License

MIT License. See LICENSE for details.

## Acknowledgments

Inspired by [wagtail-orderable](https://github.com/elton2048/wagtail-orderable) and built for Wagtail's ViewSet system.
