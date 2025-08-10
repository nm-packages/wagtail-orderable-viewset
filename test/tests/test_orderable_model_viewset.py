from django.test import TestCase, Client, override_settings

from home.models import Person
from src.wagtail_orderable_viewset.viewset import OrderableModelViewSet
from django.urls import path
from unittest.mock import patch
from django.contrib.auth import get_user_model

class DummyOrderableModelViewSet(OrderableModelViewSet):
    model = Person
    index_view_class = type('IndexView', (), {
        'view_name': 'index',
        'results_template_name': '',
        'list_filter': [],
        'list_export': [],
        'export_headings': [],
        'search_backend_name': ''
    })


urlpatterns = [
    path('order/', DummyOrderableModelViewSet().order_view, name='order'),
    path('update-order/', DummyOrderableModelViewSet().update_order_view, name='update_order'),
]

class OrderableModelViewSetTests(TestCase):
    def setUp(self):
        self.viewset = DummyOrderableModelViewSet()
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_login(self.user)

    @patch('src.wagtail_orderable_viewset.viewset.reverse', lambda *a, **kw: '/mocked-url/')
    @patch('src.wagtail_orderable_viewset.viewset.render', lambda req, tpl, ctx: type('Resp', (), {'status_code': 200, 'context_data': ctx, 'template_name': tpl})())
    def test_order_view_returns_template_and_context(self):
        Person.objects.create(name="A", age=20, city="X", team="engineering")
        # Patch request.user for direct view call
        request = self.client.get('/order/')
        request.user = self.user
        response = self.viewset.order_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('object_list', response.context_data)
        self.assertEqual(response.template_name, self.viewset.order_template_name)

    @override_settings(ROOT_URLCONF=__name__)
    def test_update_order_view_bulk_reorder(self):
        p1 = Person.objects.create(name="A", age=20, city="X", team="engineering")
        p2 = Person.objects.create(name="B", age=21, city="Y", team="marketing")
        # Use test client to POST to the update-order URL
        response = self.client.post('/update-order/', {'object_ids': [str(p2.pk), str(p1.pk)]})
        self.assertEqual(response.status_code, 200)
        # Check order was updated
        p1.refresh_from_db()
        p2.refresh_from_db()
        self.assertEqual(p2.sort_order, 1)
        self.assertEqual(p1.sort_order, 2)

    @patch('src.wagtail_orderable_viewset.viewset.reverse', lambda *a, **kw: '/mocked-url/')
    def test_index_view_kwargs_includes_reorder_context(self):
        context = self.viewset.get_index_view_kwargs()
        self.assertIn('extra_context', context)
        self.assertTrue(context['extra_context']['is_orderable'])
        self.assertEqual(context['extra_context']['sort_order_field'], 'sort_order')
