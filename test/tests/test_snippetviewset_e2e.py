from django.test import TestCase
from wagtail.test.utils import WagtailTestUtils
from home.models import Person

class SnippetViewsetE2ETests(WagtailTestUtils, TestCase):
    def setUp(self):
        super().setUp()
        self.login()

    def test_snippetviewset_order_page_and_update(self):
        a = Person.objects.create(name="Alice", age=30, city="London", team="engineering")
        b = Person.objects.create(name="Bob", age=31, city="Paris", team="engineering")
        c = Person.objects.create(name="Carol", age=32, city="Berlin", team="engineering")

        resp_index = self.client.get("/admin/snippets/home/person/")
        self.assertEqual(resp_index.status_code, 200)
        self.assertIn('href="/admin/snippets/home/person/order/"', resp_index.content.decode())

        resp_order = self.client.get("/admin/snippets/home/person/order/", follow=True)
        self.assertEqual(resp_order.status_code, 200)
        self.assertIn('id="orderable-list"', resp_order.content.decode())

        resp_update = self.client.post("/admin/snippets/home/person/update-order/", {"object_ids": [a.id, c.id, b.id]})
        self.assertEqual(resp_update.status_code, 200)
        self.assertJSONEqual(resp_update.content.decode(), {"success": True, "updated": 3})

        a.refresh_from_db()
        b.refresh_from_db()
        c.refresh_from_db()
        self.assertEqual([a.sort_order, c.sort_order, b.sort_order], [1, 2, 3])
