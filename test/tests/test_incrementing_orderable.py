from django.test import TestCase
from home.models import Person, TeamMember, Testimonial


class IncrementingOrderableTests(TestCase):
    def test_sort_order_increments_on_create(self):
        p1 = Person.objects.create(name="Alice", age=30, city="London", team="engineering")
        self.assertEqual(p1.sort_order, 1)
        p2 = Person.objects.create(name="Bob", age=25, city="Manchester", team="marketing")
        self.assertEqual(p2.sort_order, 2)
        p3 = Person.objects.create(name="Charlie", age=28, city="Bristol", team="sales")
        self.assertEqual(p3.sort_order, 3)

    def test_get_sort_order_max_returns_max(self):
        temp = TeamMember(name="Zed", position="Eng", bio="")
        self.assertEqual(temp.get_sort_order_max(), 0)
        t1 = TeamMember.objects.create(name="Ann", position="Dev", bio="")
        self.assertEqual(t1.get_sort_order_max(), 1)
        t2 = TeamMember.objects.create(name="Ben", position="PM", bio="")
        self.assertEqual(t2.get_sort_order_max(), 2)

    def test_save_does_not_change_existing_sort_order(self):
        p = Person.objects.create(name="Alice", age=30, city="London", team="engineering")
        self.assertEqual(p.sort_order, 1)
        p.city = "Leeds"
        p.age = 31
        p.save()
        p.refresh_from_db()
        self.assertEqual(p.sort_order, 1)

    def test_manual_sort_order_is_overridden_on_create(self):
        p = Person(name="X", age=22, city="York", team="support")
        p.sort_order = 42
        p.save()
        self.assertEqual(p.sort_order, 1)
        q = Person(name="Y", age=23, city="Bath", team="hr")
        q.sort_order = 99
        q.save()
        self.assertEqual(q.sort_order, 2)

    def test_works_across_multiple_models(self):
        a = Testimonial.objects.create(name="A", company="Co", content="c")
        b = Testimonial.objects.create(name="B", company="Co", content="c")
        self.assertEqual((a.sort_order, b.sort_order), (1, 2))
        x = TeamMember.objects.create(name="X", position="Dev", bio="")
        y = TeamMember.objects.create(name="Y", position="PM", bio="")
        z = TeamMember.objects.create(name="Z", position="UX", bio="")
        self.assertEqual((x.sort_order, y.sort_order, z.sort_order), (1, 2, 3))

    def test_incrementing_orderable_methods(self):
        self.assertEqual(Testimonial.objects.count(), 0)
        obj1 = Testimonial.objects.create(name="First", company="A", content="Test", rating=5)
        self.assertEqual(obj1.sort_order, 1)
        obj2 = Testimonial.objects.create(name="Second", company="B", content="Test", rating=4)
        self.assertEqual(obj2.sort_order, 2)
        objs = list(Testimonial.objects.order_by("sort_order"))
        self.assertEqual([o.sort_order for o in objs], [1, 2])
        self.assertEqual(obj2.sort_order, 2)
        self.assertEqual(obj2.get_sort_order_max(), 2)




