from django.test import TestCase
from wagtail.test.utils import WagtailTestUtils
from home.models import Testimonial, TeamMember

class ModelViewsetE2ETests(WagtailTestUtils, TestCase):
    def setUp(self):
        super().setUp()
        self.login()

    def test_modelviewset_order_page_and_update(self):
        a = Testimonial.objects.create(name="Alice", company="Acme", content="x")
        b = Testimonial.objects.create(name="Bob", company="Beta", content="y")
        c = Testimonial.objects.create(name="Carol", company="Corp", content="z")

        resp_index = self.client.get("/admin/testimonial/")
        self.assertEqual(resp_index.status_code, 200)
        self.assertIn('href="/admin/testimonial/order/"', resp_index.content.decode())

        resp_order = self.client.get("/admin/testimonial/order/", follow=True)
        self.assertEqual(resp_order.status_code, 200)
        self.assertIn('id="orderable-list"', resp_order.content.decode())
        self.assertIn("/admin/testimonial/update-order/", resp_order.content.decode())

        resp_update = self.client.post("/admin/testimonial/update-order/", {"object_ids": [c.id, a.id, b.id]}, follow=True)
        self.assertEqual(resp_update.status_code, 200)
        self.assertJSONEqual(resp_update.content.decode(), {"success": True, "updated": 3})

        a.refresh_from_db()
        b.refresh_from_db()
        c.refresh_from_db()
        self.assertEqual([c.sort_order, a.sort_order, b.sort_order], [1, 2, 3])

    def test_modelviewset_team_member_order_update(self):
        a = TeamMember.objects.create(name="Alice", position="Eng", bio="x")
        b = TeamMember.objects.create(name="Bob", position="Eng", bio="y")
        c = TeamMember.objects.create(name="Carol", position="Eng", bio="z")

        resp_update = self.client.post("/admin/team_member/update-order/", {"object_ids": [b.id, c.id, a.id]}, follow=True)
        self.assertEqual(resp_update.status_code, 200)
        self.assertJSONEqual(resp_update.content.decode(), {"success": True, "updated": 3})

        a.refresh_from_db()
        b.refresh_from_db()
        c.refresh_from_db()
        self.assertEqual([b.sort_order, c.sort_order, a.sort_order], [1, 2, 3])
