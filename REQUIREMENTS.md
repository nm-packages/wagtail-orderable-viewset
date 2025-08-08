# Wagtail Orderable Viewset - Requirements

## Package Overview
**Package Name:** wagtail-orderable-viewset  
**Description:** Add drag-and-drop ordering functionality to Wagtail's SnippetViewSet and ModelViewSet in the admin panel, similar to the functionality that wagtail-orderable provided for the deprecated wagtail-modeladmin package.

## Background
Wagtail currently doesn't offer orderable functionality for SnippetViewSets or ModelViewSets. While both ViewSet types have related functionality, neither supports ordering in the Wagtail admin interface. 

The [wagtail-orderable](https://github.com/elton2048/wagtail-orderable) package previously provided this functionality for the [wagtail-modeladmin](https://github.com/wagtail-nest/wagtail-modeladmin) package, but wagtail-modeladmin is now in maintenance mode and has been replaced by Wagtail's built-in ViewSets.

This package aims to fill that gap by providing orderable functionality for Wagtail's modern ViewSet system.

## Core Requirements

### Functional Requirements
- [ ] Provide drag-and-drop ordering for SnippetViewSet listings
- [ ] Provide drag-and-drop ordering for ModelViewSet listings
- [ ] Support custom ordering field names (default to 'sort_order')
- [ ] Maintain existing filters and search functionality when ordering
- [ ] Handle ordering updates via AJAX to avoid page reloads
- [ ] Support both ascending and descending order
- [ ] Preserve ordering when items are filtered or searched

### Technical Requirements
- [ ] Python 3.9+ compatibility
- [ ] Wagtail 7.0+ compatibility
- [ ] Django 4.2+ compatibility
- [ ] Follow Wagtail's ViewSet patterns and conventions
- [ ] Use modern JavaScript for drag-and-drop functionality
- [ ] Provide CSS styles that integrate with Wagtail admin theme

### API Requirements
- [ ] ViewSet subclass providing ordering features
- [ ] Support for custom ordering field names
- [ ] Integration with Wagtail's ViewSet system
- [ ] AJAX endpoints for updating order
- [ ] Proper CSRF protection for order updates

## Use Cases
- **Content Managers**: Need to reorder snippets (e.g., testimonials, team members, FAQ items) in the admin without manually editing sort order fields
- **Developers**: Want to add ordering to custom models registered with ViewSets without building custom admin interfaces
- **Site Administrators**: Need to maintain consistent ordering of content items across different sections of a site
- **Wagtail Plugin Developers**: Want to provide ordering functionality in their plugins using ViewSets

## Features
- [ ] OrderableModelViewSet for models/snippets
- [ ] Drag-and-drop interface in admin listings
- [ ] Automatic sort_order field management
- [ ] Custom ordering field support
- [ ] AJAX-powered order updates
- [ ] Integration with Wagtail's existing admin UI
- [ ] Support for filtered and searched results
- [ ] Visual feedback during drag operations
- [ ] Keyboard accessibility for ordering

## Dependencies
- [ ] Django 4.2+
- [ ] Wagtail 7.0+
- [ ] Python 3.9+
- [ ] Modern browser support (ES6+)
- [ ] jQuery (if required by Wagtail admin)
- [ ] CSRF token support for AJAX requests

## Testing Requirements
- [ ] Unit tests
- [ ] Integration tests
- [ ] Documentation tests

## Documentation Requirements
- [ ] README with installation and usage examples
- [ ] API documentation
- [ ] Code examples

## Performance Requirements
- [ ] AJAX order updates should complete within 500ms
- [ ] Support for ordering up to 1000 items without performance degradation
- [ ] Efficient database queries for order updates
- [ ] Minimal JavaScript bundle size (< 50KB)
- [ ] Smooth drag-and-drop animations (60fps)

## Security Requirements
- [ ] CSRF protection on all order update endpoints
- [ ] Permission checks for ordering operations
- [ ] Input validation for order values
- [ ] Rate limiting on order update endpoints
- [ ] Audit trail for order changes (optional)

## Notes
- This package should follow Wagtail's design patterns and conventions
- Should be compatible with existing Wagtail admin customizations
- Consider accessibility requirements (WCAG 2.1 AA)
- May need to handle edge cases like concurrent ordering updates
- Should provide clear documentation for migration from wagtail-orderable

---

**Last Updated:** January 2025
**Status:** Draft
