# Example Project Usage

This guide shows how to run the example project and use `OrderableModelViewSet` and `OrderableSnippetViewSet`.

## Quick Start

### 1. Install and Run the Example

```bash
# From the repo root
cd test
uv run manage.py migrate
uv run manage.py createsuperuser
uv run manage.py runserver
```

### 2. Seed Sample Data (Optional)

```bash
# From the repo root
cd test
uv run manage.py fixtures
```

Flags:

- `--count <int>`: Number of records to create (default: 50)
- `--delete-existing`: Delete all existing records before creating new ones
- `--clear-only`: Delete all records and exit
- `--seed <int>`: Set random seed (default: 1337)

### 3. Visit the Admin

Go to `http://localhost:8000/admin` and log in. You will see menu items with ordering enabled:

- Testimonials (model)
- Team members (model)
- People (snippet)

On each listing page, a Reorder button appears when there are at least two records. Click it to open a drag-and-drop interface that saves order automatically.

## How It Works

### OrderableModelViewSet

Define a model that uses the `IncrementingOrderable` base class:

```python
# models.py
from wagtail_orderable_viewset.models import IncrementingOrderable

class Testimonial(IncrementingOrderable):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.company}"
```

Define a viewset:

```python
# admin_views.py
from wagtail_orderable_viewset.viewsets import OrderableModelViewSet

class TestimonialViewSet(OrderableModelViewSet):
    model = Testimonial

    list_display = ['name', 'company', 'rating', 'is_featured']
    list_filter = ['is_featured']
    list_export = ['name', 'company', 'rating', 'is_featured']
    
    form_fields = ['name', 'company', 'content', 'rating', 'is_featured']

    search_fields = ['name', 'company', 'content']
    order_by = ['name']

    menu_label = 'Testimonials'
    icon = 'folder-open-1'
    menu_order = 100
    add_to_admin_menu = True

testimonial_viewset = TestimonialViewSet('testimonial')
```

Register the viewset with Wagtail admin (using hooks):

```python
# wagtail_hooks.py
from wagtail import hooks

from .admin_views import testimonial_viewset

@hooks.register("register_admin_viewset")
def register_testimonial_viewset():
    return testimonial_viewset
```

### OrderableSnippetViewSet

```python
# models.py
from wagtail_orderable_viewset.models import IncrementingOrderable

class Person(IncrementingOrderable):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    city = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    team = models.CharField(max_length=50, choices=[
        ('engineering', 'Engineering'),
        ('marketing', 'Marketing'),
        ('sales', 'Sales'),
        ('support', 'Support'),
        ('hr', 'HR'),
    ])

    class Meta:
        ordering = ['name']
        verbose_name = 'Person'
        verbose_name_plural = 'People'

    def __str__(self):
        return self.name
```

Define a viewset:

```python
# admin_views.py
from wagtail_orderable_viewset.viewsets import OrderableSnippetViewSet

from .models import Person

class PersonViewSet(OrderableSnippetViewSet):
    model = Person

    list_display = ['name', 'age', 'city', 'team', 'is_active']
    list_export = ['name', 'age', 'city', 'team', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'city', 'team']
    
    order_by = ['name']

    icon = 'user'

person_viewset = PersonViewSet()
```

Register the viewset with Wagtail admin (using hooks):

```python
# wagtail_hooks.py
from wagtail.snippets.models import register_snippet

from .admin_views import person_viewset

register_snippet(person_viewset)
```

## Usage Patterns

See the source code in the `test` directory for usage examples.

## What the viewsets add

Both `OrderableModelViewSet` and `OrderableSnippetViewSet`:

- Inject a Reorder button into the listing page
- Provide an Order page with drag‑and‑drop (SortableJS)
- Expose a POST endpoint for updating order (bulk list or single‑item move)

The implementation uses a shared `OrderableViewSetMixin` so you can extend or override behavior in one place if needed.

## Troubleshooting

- Reorder button not visible: it only appears when the listing has 2+ items.
- NoReverseMatch on snippet order page: ensure you are using `OrderableSnippetViewSet` for snippets; it wires the correct `list` route internally.
- CSRF issues on reorder: make sure you are logged in via the admin and the browser is sending cookies; the JS includes the CSRF token automatically.
