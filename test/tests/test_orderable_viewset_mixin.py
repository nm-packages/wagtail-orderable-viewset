from django.test import TestCase, RequestFactory
from django.urls import reverse, ResolverMatch
from home.models import Person
from src.wagtail_orderable_viewset.viewset import OrderableViewSetMixin
from wagtail.admin.viewsets.model import ModelViewSet
from unittest.mock import patch

class DummyViewSet(OrderableViewSetMixin, ModelViewSet):
    model = Person
    index_view_class = type('IndexView', (), {'view_name': 'index'})
    sort_order_field_name = 'sort_order'
    order_template_name = 'wagtail_orderable_viewset/order.html'
    def get_url_name(self, name):
        return f"person_{name}"
    def __init__(self):
        self.request_factory = RequestFactory()

class OrderableViewSetMixinTests(TestCase):
    def setUp(self):
        self.viewset = DummyViewSet()

    def test_get_order_queryset_returns_sorted(self):
        p1 = Person.objects.create(name="A", age=20, city="X", team="engineering")
        p2 = Person.objects.create(name="B", age=21, city="Y", team="marketing")
        p2.sort_order = 1
        p2.save()
        p1.sort_order = 2
        p1.save()
        qs = self.viewset.get_order_queryset()
        self.assertEqual(list(qs), [p2, p1])

    @patch('src.wagtail_orderable_viewset.viewset.reverse', lambda *a, **kw: '/mocked-url/')
    def test_get_order_context_data_keys(self):
        Person.objects.create(name="A", age=20, city="X", team="engineering")
        objects = self.viewset.get_order_queryset()
        context = self.viewset.get_order_context_data(objects)
        expected_keys = {
            'objects', 'object_list', 'model_name', 'model_verbose_name',
            'model_verbose_name_plural', 'model_opts', 'sort_field', 'index_url', 'update_url'
        }
        self.assertTrue(expected_keys.issubset(context.keys()))
        self.assertEqual(context['sort_field'], 'sort_order')

    def test_get_urlpatterns_includes_order_routes(self):
        # Patch the super call to return [] using patch.object on the parent class
        with patch.object(ModelViewSet, 'get_urlpatterns', return_value=[]):
            patterns = self.viewset.get_urlpatterns()
            names = [p.name for p in patterns]
            self.assertIn('order', names)
            self.assertIn('update_order', names)
