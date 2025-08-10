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
    Mixin that provides shared ordering functionality for Wagtail viewsets.
    Works with both ModelViewSet and SnippetViewSet.
    """

    # Default sort field name; subclasses can override
    sort_order_field_name = "sort_order"

    # Template used for the dedicated order view
    order_template_name = "wagtail_orderable_viewset/order.html"

    def get_index_view_kwargs(self, **kwargs):
        """Inject extra context to enable the "Reorder" button and JS hooks."""
        context_kwargs = super().get_index_view_kwargs(**kwargs)
        extra_context = {
            "order_url_name": self.get_url_name("order"),
            "is_orderable": True,
            "sort_order_field": self.sort_order_field_name,
        }
        # Merge/override any existing extra_context
        if "extra_context" in context_kwargs and isinstance(
            context_kwargs["extra_context"], dict
        ):
            context_kwargs["extra_context"].update(extra_context)
        else:
            context_kwargs["extra_context"] = extra_context
        return context_kwargs

    def get_urlpatterns(self):
        """Append ordering routes to the viewset's URL patterns."""
        patterns = super().get_urlpatterns()
        patterns += [
            path("order/", self.order_view, name="order"),
            path("update-order/", self.update_order_view, name="update_order"),
        ]
        return patterns

    def get_index_url_name(self) -> str:
        """
        Determine the index route name for the viewset.
        - ModelViewSet index view typically uses view_name = 'index'
        - SnippetViewSet index view uses view_name = 'list'
        """
        view_name = getattr(self.index_view_class, "view_name", None)
        return view_name or "index"

    def get_order_queryset(self):
        return self.model.objects.order_by(self.sort_order_field_name)

    def get_order_context_data(self, objects):
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
        objects = self.get_order_queryset()
        context = self.get_order_context_data(objects)
        return render(request, self.order_template_name, context)

    @method_decorator(csrf_protect)
    @method_decorator(require_POST)
    def update_order_view(self, request):
        try:
            # Bulk reorder support: handle array of object IDs from the client
            object_ids = request.POST.getlist("object_ids[]") or request.POST.getlist(
                "object_ids"
            )

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
    Custom ModelViewSet that adds a dedicated order view and AJAX endpoint
    and injects order-related context into the listing.
    """

    # Use our custom index (listing) template
    index_template_name = "wagtail_orderable_viewset/list.html"
    # Inherits ordering behaviour from mixin


class OrderableSnippetViewSet(OrderableViewSetMixin, SnippetViewSet):
    """
    Custom SnippetViewSet that adds a dedicated order view and AJAX endpoint
    and injects order-related context into the listing.
    """

    # Use a dedicated snippets index template
    index_template_name = "wagtail_orderable_viewset/snippets_list.html"
    # Inherits ordering behaviour from mixin
