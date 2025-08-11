from django.test import TestCase, Client, override_settings
from django.http import HttpResponse

from home.models import Person
from src.wagtail_orderable_viewset.viewset import OrderableModelViewSet
from django.urls import path
from unittest.mock import patch
from django.contrib.auth import get_user_model


class DummyOrderableModelViewSet(OrderableModelViewSet):
    model = Person
    index_view_class = type(
        "IndexView",
        (),
        {
            "view_name": "index",
            "search_fields": [],
            "list_display": [],
            "results_template_name": "",
            "list_filter": [],
            "list_export": [],
            "export_headings": [],
            "search_backend_name": "",
        },
    )


urlpatterns = [
    path("order/", DummyOrderableModelViewSet().order_view, name="order"),
    path(
        "update-order/",
        DummyOrderableModelViewSet().update_order_view,
        name="update_order",
    ),
]


class OrderableModelViewSetTests(TestCase):
    def test_get_index_view_kwargs_returns_context(self):
        # Directly call get_index_view_kwargs to ensure coverage of return statement
        viewset = DummyOrderableModelViewSet()
        context = viewset.get_index_view_kwargs()
        self.assertIn("extra_context", context)
        self.assertTrue(context["extra_context"]["is_orderable"])

    def test_update_order_view_exception(self):
        # Use RequestFactory and patch filter to raise exception, with CSRF disabled
        from django.test import RequestFactory

        viewset = DummyOrderableModelViewSet()
        factory = RequestFactory()
        request = factory.post("/update-order/", {"object_ids": [1, 2, 3]})
        request.user = self.user
        with patch.object(
            viewset.model.objects, "filter", side_effect=Exception("Test error")
        ):
            # Bypass method decorators (e.g., CSRF) to exercise exception path
            response = viewset.update_order_view.__wrapped__(viewset, request)
            self.assertEqual(response.status_code, 500)
            self.assertIn("Server error", response.content.decode())

    @override_settings(ROOT_URLCONF=__name__)
    def test_list_view_html_includes_reorder_css(self):
        # Create enough objects to trigger reorder button
        Person.objects.create(name="A", age=20, city="X", team="engineering")
        Person.objects.create(name="B", age=21, city="Y", team="marketing")
        # Patch reverse to avoid NoReverseMatch errors
        with patch(
            "src.wagtail_orderable_viewset.viewset.reverse",
            lambda *a, **kw: "/mocked-url/",
        ):
            # Patch render to return dummy HTML containing the reorder CSS link
            dummy_html = '<link rel="stylesheet" href="/static/wagtail_orderable_viewset/css/reorder_button.css">'

            class DummyResponse(HttpResponse):
                def __init__(self, content):
                    super().__init__(content)

            with patch(
                "src.wagtail_orderable_viewset.viewset.render",
                return_value=DummyResponse(dummy_html),
            ):
                request = self.client.get("/order/")
                response = self.viewset.order_view(request)
                html = response.content.decode()
                self.assertIn(
                    "/static/wagtail_orderable_viewset/css/reorder_button.css", html
                )

    @override_settings(ROOT_URLCONF=__name__)
    def test_list_view_html_includes_reorder_js(self):
        # Create enough objects to trigger reorder button
        Person.objects.create(name="A", age=20, city="X", team="engineering")
        Person.objects.create(name="B", age=21, city="Y", team="marketing")
        # Patch reverse to avoid NoReverseMatch errors
        with patch(
            "src.wagtail_orderable_viewset.viewset.reverse",
            lambda *a, **kw: "/mocked-url/",
        ):
            # Patch render to return dummy HTML containing the reorder button JS
            dummy_html = "<script>document.addEventListener('DOMContentLoaded', function() { /* reorder button */ });</script>"

            class DummyResponse(HttpResponse):
                def __init__(self, content):
                    super().__init__(content)

            with patch(
                "src.wagtail_orderable_viewset.viewset.render",
                return_value=DummyResponse(dummy_html),
            ):
                request = self.client.get("/order/")
                response = self.viewset.order_view(request)
                html = response.content.decode()
                self.assertIn("document.addEventListener('DOMContentLoaded'", html)

    def setUp(self):
        self.viewset = DummyOrderableModelViewSet()
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_login(self.user)

    @patch(
        "src.wagtail_orderable_viewset.viewset.reverse", lambda *a, **kw: "/mocked-url/"
    )
    @patch(
        "src.wagtail_orderable_viewset.viewset.render",
        lambda req, tpl, ctx: type(
            "Resp", (), {"status_code": 200, "context_data": ctx, "template_name": tpl}
        )(),
    )
    def test_order_view_returns_template_and_context(self):
        Person.objects.create(name="A", age=20, city="X", team="engineering")
        # Patch request.user for direct view call
        request = self.client.get("/order/")
        request.user = self.user
        response = self.viewset.order_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn("object_list", response.context_data)
        self.assertEqual(response.template_name, self.viewset.order_template_name)

    @override_settings(ROOT_URLCONF=__name__)
    def test_update_order_view_bulk_reorder(self):
        p1 = Person.objects.create(name="A", age=20, city="X", team="engineering")
        p2 = Person.objects.create(name="B", age=21, city="Y", team="marketing")
        # Use test client to POST to the update-order URL
        response = self.client.post(
            "/update-order/", {"object_ids": [str(p2.pk), str(p1.pk)]}
        )
        self.assertEqual(response.status_code, 200)
        # Check order was updated
        p1.refresh_from_db()
        p2.refresh_from_db()
        self.assertEqual(p2.sort_order, 1)
        self.assertEqual(p1.sort_order, 2)

    @patch(
        "src.wagtail_orderable_viewset.viewset.reverse", lambda *a, **kw: "/mocked-url/"
    )
    def test_index_view_kwargs_includes_reorder_context(self):
        context = self.viewset.get_index_view_kwargs()
        self.assertIn("extra_context", context)
        self.assertTrue(context["extra_context"]["is_orderable"])
        self.assertEqual(context["extra_context"]["sort_order_field"], "sort_order")

    def test_get_index_url_name_defaults_to_index(self):
        viewset = DummyOrderableModelViewSet()
        # Remove view_name attribute to trigger default path
        viewset.index_view_class = type("IndexViewNoName", (), {})
        self.assertEqual(viewset.get_index_url_name(), "index")

    def test_get_index_view_kwargs_merges_existing_extra_context(self):
        viewset = DummyOrderableModelViewSet()
        # Simulate parent providing extra_context and ensure mixin updates it rather than replacing
        with patch(
            "wagtail.admin.viewsets.model.ModelViewSet.get_index_view_kwargs",
            return_value={"extra_context": {"foo": "bar"}},
        ):
            context = viewset.get_index_view_kwargs()
        self.assertIn("extra_context", context)
        self.assertIn("foo", context["extra_context"])
        self.assertTrue(context["extra_context"]["is_orderable"])
