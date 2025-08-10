# Example Project Usage

This guide shows how to run the example project and use `OrderableModelViewSet` and `OrderableSnippetViewSet`, including custom ordering fields.

## Quick Start

### 1. Install and Run the Example

```bash
# From the repo root
python -m venv .venv
source .venv/bin/activate
pip install -e .

cd test
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 2. Seed Sample Data (Optional)

```bash
cd test
python manage.py create_sample_data --count 50
```

Flags:
- `--delete-existing`: Delete all existing records before creating new ones
- `--clear-only`: Delete all records and exit
- `--seed <int>`: Set random seed (default: 1337)

### 3. Visit the Admin

Go to `http://localhost:8000/admin` and log in. You will see sections with ordering enabled:
- Testimonials (model)
- Team members (model)
- FAQ items (model, custom ordering field)
- Services (model, custom ordering field)
- People (snippet)

On each listing page, a Reorder button appears when there are at least two records. Click it to open a drag-and-drop interface that saves order automatically.

## How It Works

### For Models: OrderableModelViewSet

```python
# views.py
from wagtail_orderable_viewset.viewset import OrderableModelViewSet
from .models import Testimonial

class TestimonialViewSet(OrderableModelViewSet):
  model = Testimonial
  list_display = ["name", "company", "rating", "sort_order"]
  search_fields = ["name", "company", "content"]

# Register with Wagtail admin (using hooks)
from wagtail import hooks
testimonial_viewset = TestimonialViewSet("testimonial")

@hooks.register("register_admin_viewset")
def register_testimonial_viewset():
  return testimonial_viewset
```

Models can use the provided `IncrementingOrderable` base, which manages an integer `sort_order` field and auto-assigns it for new records:

```python
# models.py
from django.db import models
from wagtail_orderable_viewset.models import IncrementingOrderable

class Testimonial(IncrementingOrderable):
  name = models.CharField(max_length=100)
  company = models.CharField(max_length=100)
  content = models.TextField()
```

### For Snippets: OrderableSnippetViewSet

```python
# views.py
from wagtail_orderable_viewset.viewset import OrderableSnippetViewSet
from .models import Person

class PersonViewSet(OrderableSnippetViewSet):
  model = Person
  list_display = ["name", "team", "sort_order"]
```

Register with Wagtail admin as above.

## Custom Ordering Fields

You can use a custom integer field for ordering by overriding `sort_order_field_name` in your viewset:

```python
class ServiceViewSet(OrderableModelViewSet):
  model = Service
  sort_order_field_name = "display_order"
  list_display = ["name", "display_order"]
```

## Patterns

See the source code in the `test` directory for usage examples.

### For snippets: OrderableSnippetViewSet

```python
# models.py
class Person(IncrementingOrderable):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    city = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]
        verbose_name = "Person"
        verbose_name_plural = "People"

# views.py
from wagtail_orderable_viewset.viewset import OrderableSnippetViewSet

class PersonViewSet(OrderableSnippetViewSet):
    model = Person
    list_display = ["name", "age", "city", "sort_order"]
    search_fields = ["name", "city"]

# register_snippet
from wagtail.snippets.models import register_snippet

register_snippet(PersonViewSet)
```

`OrderableSnippetViewSet` provides the same ordering UI and endpoints for snippets. The index template is tailored to the snippets listings and includes a Reorder button when applicable.

## What the viewsets add

Both `OrderableModelViewSet` and `OrderableSnippetViewSet`:
- Inject a Reorder button into the listing page
- Provide an Order page with drag‑and‑drop (SortableJS)
- Expose a POST endpoint for updating order (bulk list or single‑item move)
- Respect a configurable `sort_order_field_name` (default: `sort_order`)

The implementation uses a shared `OrderableViewSetMixin` so you can extend or override behavior in one place if needed.

## Files of interest

- Templates
  - `wagtail_orderable_viewset/list.html` (models index)
  - `wagtail_orderable_viewset/snippets_list.html` (snippets index)
  - `wagtail_orderable_viewset/order.html` (drag‑and‑drop order page)
- Static
  - `wagtail_orderable_viewset/js/orderable.js`
  - `wagtail_orderable_viewset/css/orderable.css`
- Python
  - `wagtail_orderable_viewset/viewset.py` (viewsets + mixin)
  - `wagtail_orderable_viewset/models.py` (`IncrementingOrderable`)

## Troubleshooting

- Reorder button not visible: it only appears when the listing has 2+ items.
- NoReverseMatch on snippet order page: ensure you are using `OrderableSnippetViewSet` for snippets; it wires the correct `list` route internally.
- CSRF issues on reorder: make sure you are logged in via the admin and the browser is sending cookies; the JS includes the CSRF token automatically.


