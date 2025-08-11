from django.db import models
from wagtail_orderable_viewset.models import IncrementingOrderable

from wagtail.models import Page


class HomePage(Page):
    pass


class Testimonial(IncrementingOrderable):
    """
    Example model for testimonials which includes a incrementing sort_order field.
    """

    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.company}"


class TeamMember(IncrementingOrderable):
    """
    Example model for team members which includes a incrementing sort_order field.
    """

    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    email = models.EmailField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.position}"


class Person(IncrementingOrderable):
    """
    Example model for people which includes a incrementing sort_order field.
    """

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    city = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    team = models.CharField(
        max_length=50,
        choices=[
            ("engineering", "Engineering"),
            ("marketing", "Marketing"),
            ("sales", "Sales"),
            ("support", "Support"),
            ("hr", "HR"),
        ],
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Person"
        verbose_name_plural = "People"

    def __str__(self):
        return self.name
