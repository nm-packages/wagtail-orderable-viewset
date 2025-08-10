from django.test import TestCase, Client, override_settings
from src.wagtail_orderable_viewset.viewset import OrderableSnippetViewSet
from home.models import Person  # Use Person as a dummy snippet model for testing
from django.urls import path
from unittest.mock import patch

class DummyOrderableSnippetViewSet(OrderableSnippetViewSet):
    model = Person
    class IndexView:
        view_name = 'list'
        results_template_name = ''
        list_filter = []
        list_export = []
        export_headings = []
        search_backend_name = ''
        @staticmethod
        def as_view(**kwargs):
            def view(request, *args, **kw):
                return None
            return view
    index_view_class = IndexView
    def get_url_name(self, name):
        return f"person_snippet_{name}"

urlpatterns = [
    path('order/', DummyOrderableSnippetViewSet().order_view, name='order'),
    path('update-order/', DummyOrderableSnippetViewSet().update_order_view, name='update_order'),
]

class OrderableSnippetViewSetTests(TestCase):
    def setUp(self):
        self.viewset = DummyOrderableSnippetViewSet()
        self.client = Client()

    @override_settings(ROOT_URLCONF=__name__)
    @patch('django.shortcuts.render')
    def test_order_view_returns_template_and_context(self, mock_render):
        from unittest.mock import patch
        from django.http import HttpRequest
        from django.contrib.auth.models import AnonymousUser
        request = HttpRequest()
        request.user = AnonymousUser()
        with patch("src.wagtail_orderable_viewset.viewset.render") as mock_render:
            with patch("src.wagtail_orderable_viewset.viewset.reverse", return_value="/order/"):
                self.viewset.order_view(request)
                self.assertTrue(mock_render.called)
                args, kwargs = mock_render.call_args
                self.assertEqual(args[1], self.viewset.order_template_name)
                context = args[2]
                self.assertIn("objects", context)

    @override_settings(ROOT_URLCONF=__name__)
    def test_update_order_view_bulk_reorder(self):
        # Create dummy objects
        objs = [Person.objects.create(name=f"Person {i}", age=1) for i in range(1, 4)]
        ids = [str(obj.pk) for obj in objs]
        data = {'object_ids[]': ids}
        response = self.client.post('/update-order/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        # Check order updated
        for idx, obj in enumerate(Person.objects.order_by('sort_order'), start=1):
            self.assertEqual(obj.sort_order, idx)

    def test_get_order_queryset_returns_sorted(self):
        [Person.objects.create(name=f"Person {i}", sort_order=3-i, age=1) for i in range(3)]
        queryset = self.viewset.get_order_queryset()
        orders = list(queryset.values_list('sort_order', flat=True))
        self.assertEqual(orders, sorted(orders))

    def test_get_order_context_data_keys(self):
        from unittest.mock import patch
        objs = [Person.objects.create(name=f"Person {i}", age=1) for i in range(2)]
        with patch('src.wagtail_orderable_viewset.viewset.reverse', return_value='/index/'):
            context = self.viewset.get_order_context_data(objs)
            self.assertIn('objects', context)
            self.assertIn('object_list', context)
            self.assertIn('model_name', context)
            self.assertIn('sort_field', context)
            self.assertEqual(context['sort_field'], self.viewset.sort_order_field_name)

    def test_get_index_view_kwargs_includes_reorder_context(self):
        context = self.viewset.get_index_view_kwargs()
        self.assertIn('extra_context', context)
        self.assertTrue(context['extra_context']['is_orderable'])
        self.assertEqual(context['extra_context']['sort_order_field'], self.viewset.sort_order_field_name)

    def test_get_urlpatterns_includes_order_routes(self):
        patterns = self.viewset.get_urlpatterns()
        route_names = [p.name for p in patterns]
        self.assertIn('order', route_names)
        self.assertIn('update_order', route_names)
