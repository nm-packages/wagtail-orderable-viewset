# Example project usage

This document explains how to run the bundled example project and showcases how to use `OrderableModelViewSet` and `OrderableSnippetViewSet`, including a custom ordering field.

## Quick start

1) Install and run the example

```bash
# From the repo root
python -m venv .venv
source .venv/bin/activate
pip install -e .

cd sandbox
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

2) Seed sample data (optional but recommended)

```bash
cd sandbox
python manage.py create_sample_data --count 50
```

Available flags:
- --delete-existing: Delete all existing records first and then create new ones
- --clear-only: Delete all records and exit without creating new data
- --seed <int>: Control random seed (defaults to 1337)

3) Visit the admin

- Go to `http://localhost:8000/admin`
- You will see the following sections with ordering enabled:
  - Testimonials (model)
  - Team members (model)
  - FAQ items (model, custom ordering field)
  - Services (model, custom ordering field)
  - People (snippet)

On each listing page, a Reorder button appears when there are at least two records. Click it to open a drag‑and‑drop interface that saves order automatically.

## How it works

### For models: OrderableModelViewSet

```python
# views.py
from wagtail_orderable_viewset.viewset import OrderableModelViewSet
from .models import Testimonial

class TestimonialViewSet(OrderableModelViewSet):
    model = Testimonial
    list_display = ["name", "company", "rating", "sort_order"]
    search_fields = ["name", "company", "content"]

# Register with Wagtail admin (example using hooks)
from wagtail import hooks

testimonial_viewset = TestimonialViewSet("testimonial")

@hooks.register("register_admin_viewset")
def register_testimonial_viewset():
    return testimonial_viewset
```

Models can use the provided `IncrementingOrderable` base which manages an integer `sort_order` field and auto‑assigns it for new records:

```python
# models.py
from django.db import models
from wagtail_orderable_viewset.models import IncrementingOrderable

class Testimonial(IncrementingOrderable):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    content = models.TextField()

    class Meta:
        ordering = ["name"]  # listing order can be independent of the stored sort field
```

### Custom ordering field

If your model uses a custom ordering field, set `sort_order_field_name` on the viewset:

```python
# models.py
class FAQItem(IncrementingOrderable):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    display_order = models.IntegerField(default=0, editable=False)

    class Meta:
        ordering = ["question"]

# views.py
class FAQItemViewSet(OrderableModelViewSet):
    model = FAQItem
    sort_order_field_name = "display_order"
    list_display = ["question", "display_order"]
```

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


