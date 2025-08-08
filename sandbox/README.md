# Wagtail Orderable ViewSet - Sandbox Example

This sandbox demonstrates the `wagtail-orderable-viewset` package in action.

## Quick Start

1. **Install the package in development mode:**
   ```bash
   cd ..
   uv pip install -e .
   ```

2. **Run the sandbox:**
   ```bash
   cd sandbox
   source ../.venv/bin/activate
   python manage.py runserver
   ```

3. **Access the admin:**
   - Go to http://localhost:8000/admin
   - Login with: `admin` / `admin123`

## What You'll See

### Snippets with Ordering

1. **Testimonials** (`/admin/snippets/orderable_example/testimonial/`)
   - Uses default `sort_order` field
   - Drag and drop to reorder testimonials
   - Filter by rating and featured status
   - Search by name, company, or content

2. **Team Members** (`/admin/snippets/orderable_example/teammember/`)
   - Uses default `sort_order` field
   - Drag and drop to reorder team members
   - Filter by position
   - Search by name, position, or bio

### Models with Custom Ordering Fields

3. **FAQ Items** (`/admin/snippets/orderable_example/faqitem/`)
   - Uses custom `display_order` field
   - Filter by category and active status
   - Search by question or answer

4. **Services** (`/admin/snippets/orderable_example/service/`)
   - Uses custom `service_order` field
   - Filter by featured status
   - Search by title or description

## Features Demonstrated

- ✅ **Drag-and-drop ordering** for all models
- ✅ **Custom ordering fields** (FAQ uses `display_order`, Services uses `service_order`)
- ✅ **Integration with existing filters and search**
- ✅ **Visual feedback** during drag operations
- ✅ **AJAX-powered updates** (no page reloads)
- ✅ **Mobile-friendly** touch support

## How It Works

The package provides:

1. **Orderable Model Mixin** - Adds `sort_order` field to models
2. **Registration Function** - `register_orderable_snippet()` for easy setup
3. **AJAX Endpoints** - For real-time order updates
4. **JavaScript/CSS** - Drag-and-drop interface

## Code Examples

### Basic Usage
```python
from wagtail_orderable_viewset import register_orderable_snippet
from .models import Testimonial

# Register with default sort_order field
register_orderable_snippet(Testimonial)
```

### Custom Ordering Field
```python
from wagtail_orderable_viewset import register_orderable_snippet
from .models import FAQItem

# Register with custom ordering field
register_orderable_snippet(FAQItem, 'display_order')
```

## Testing the Ordering

1. Go to any of the snippet listings
2. Look for the drag handle (⋮⋮) in the first column
3. Click and drag items to reorder them
4. Notice the visual feedback and smooth animations
5. Try filtering and searching - ordering is preserved

## Development

To modify the example:

1. Edit models in `orderable_example/models.py`
2. Update registration in `orderable_example/wagtail_hooks.py`
3. Run `python manage.py makemigrations` and `python manage.py migrate`
4. Run `python manage.py create_sample_data` to refresh data

## Troubleshooting

- **No drag handles visible?** Make sure the package is installed and the app is in `INSTALLED_APPS`
- **AJAX errors?** Check the browser console for JavaScript errors
- **Order not updating?** Check the Django logs for server errors

## Next Steps

- Add more complex models with relationships
- Test with different field types
- Implement custom ordering logic
- Add bulk ordering operations
