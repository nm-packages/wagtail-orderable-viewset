from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.urls import path, reverse

from wagtail.admin.viewsets.model import ModelViewSet
from wagtail.snippets.views.snippets import SnippetViewSet


class OrderableViewSetMixin:
    """
    Mixin for Wagtail viewsets to provide shared ordering functionality.

    - Adds dedicated order view and AJAX endpoint for bulk reordering.
    - Injects extra context for templates to enable reorder UI and JS hooks.
    - Works with both ModelViewSet and SnippetViewSet.
    - Default sort field name is "sort_order" (compatible with IncrementingOrderable).
    """

    # Name of the field used for ordering. Override in subclasses if needed.
    sort_order_field_name = "sort_order"

    # Template used for the dedicated order view (drag-and-drop UI)
    order_template_name = "wagtail_orderable_viewset/order.html"

    def get_index_view_kwargs(self, **kwargs):
        """
        Inject extra context for the index (listing) view.
        Enables the reorder button and JS hooks in the template.
        Merges with any existing extra_context.
        """
        context_kwargs = super().get_index_view_kwargs(**kwargs)
        extra_context = {
            "order_url_name": self.get_url_name("order"),
            "is_orderable": True,
            "sort_order_field": self.sort_order_field_name,
        }
        # Merge/override any existing extra_context
        if "extra_context" in context_kwargs and isinstance(context_kwargs["extra_context"], dict):
            context_kwargs["extra_context"].update(extra_context)
        else:
            context_kwargs["extra_context"] = extra_context
        return context_kwargs

    def get_urlpatterns(self):
        """
        Append ordering routes to the viewset's URL patterns.
        Adds:
        - /order/ for the order view (drag-and-drop UI)
        - /update-order/ for the AJAX endpoint to update order
        """
        ordering_patterns = [
            path("order/", self.order_view, name="order"),
            path("update-order/", self.update_order_view, name="update_order"),
        ]
        return ordering_patterns + super().get_urlpatterns()

    def get_index_url_name(self) -> str:
        """
        Returns the route name for the index (listing) view.
        - ModelViewSet: usually 'index'
        - SnippetViewSet: usually 'list'
        """
        view_name = getattr(self.index_view_class, "view_name", None)
        return view_name or "index"

    def get_order_queryset(self):
        """
        Returns a queryset of model instances ordered by the sort field.
        Used for displaying objects in the order view.
        """
        return self.model.objects.order_by(self.sort_order_field_name)

    def get_order_context_data(self, objects):
        """
        Returns context data for the order view template.
        Includes:
        - objects: ordered queryset
        - model metadata and verbose names
        - URLs for index and update endpoints
        """
        return {
            "objects": objects,
            "object_list": objects,
            "model_name": self.model._meta.verbose_name_plural,
            "model_verbose_name": self.model._meta.verbose_name,
            "model_verbose_name_plural": self.model._meta.verbose_name_plural,
            "model_opts": self.model._meta,
            "sort_field": self.sort_order_field_name,
            "index_url": reverse(self.get_url_name(self.get_index_url_name())),
            "update_url": reverse(self.get_url_name("update_order")),
        }

    def order_view(self, request):
        """
        Renders the order view template with the ordered objects and context.
        Used for drag-and-drop reordering in the admin UI.
        """
        objects = self.get_order_queryset()
        context = self.get_order_context_data(objects)
        return render(request, self.order_template_name, context)

    @method_decorator(csrf_protect)
    @method_decorator(require_POST)
    def update_order_view(self, request):
        """
        AJAX endpoint to update the order of objects in bulk.
        Expects a POST request with a list of object IDs in the desired order.
        Updates the sort field for each object in a transaction.
        Returns a success response or error if an exception occurs.
        """
        try:
            # Bulk reorder support: handle array of object IDs from the client
            object_ids = request.POST.getlist("object_ids[]") or request.POST.getlist("object_ids")

            if object_ids:
                # Update order based on the submitted sequence
                from django.db import transaction
                with transaction.atomic():
                    for index, pk in enumerate(object_ids, start=1):
                        self.model.objects.filter(pk=pk).update(
                            **{self.sort_order_field_name: index}
                        )
                return JsonResponse({"success": True, "updated": len(object_ids)})

        except Exception as e:
            return JsonResponse({"error": f"Server error: {e}"}, status=500)


class OrderableModelViewSet(OrderableViewSetMixin, ModelViewSet):
    """
    ModelViewSet with orderable functionality for models.

    - Adds a dedicated order view and AJAX endpoint for bulk reordering.
    - Injects order-related context into the listing view.
    - Uses a custom index template for the listing page.
    """
    index_template_name = "wagtail_orderable_viewset/list.html"


class OrderableSnippetViewSet(OrderableViewSetMixin, SnippetViewSet):
    """
    SnippetViewSet with orderable functionality for models.

    - Adds a dedicated order view and AJAX endpoint for bulk reordering.
    - Injects order-related context into the listing view.
    - Uses a custom index template for the snippets listing page.
    """
    index_template_name = "wagtail_orderable_viewset/snippets_list.html"
