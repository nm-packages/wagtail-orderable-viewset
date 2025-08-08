from django.db import models
from wagtail_orderable_viewset.models import IncrementingOrderable


class Testimonial(IncrementingOrderable):
    """
    Example snippet that uses the default sort_order field.
    """
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.company}"


class TeamMember(IncrementingOrderable):
    """
    Example snippet for team members with ordering.
    """
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    email = models.EmailField(blank=True)
    photo = models.ImageField(upload_to='team_photos/', blank=True, null=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.position}"


class FAQItem(IncrementingOrderable):
    """
    Example model with custom ordering field.
    """
    question = models.CharField(max_length=200)
    answer = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('general', 'General'),
        ('technical', 'Technical'),
        ('billing', 'Billing'),
    ])
    display_order = models.IntegerField(default=0, editable=False)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['question']
    
    def __str__(self):
        return self.question


class Service(IncrementingOrderable):
    """
    Example model for services with custom ordering.
    """
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    service_order = models.IntegerField(default=0, editable=False)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['title']
    
    def __str__(self):
        return self.title

class Person(IncrementingOrderable):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    city = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    team = models.CharField(max_length=100, choices=[
        ('engineering', 'Engineering'),
        ('marketing', 'Marketing'),
        ('sales', 'Sales'),
        ('support', 'Support'),
        ('hr', 'HR'),
    ])

    class Meta:
        ordering = ['name']
        verbose_name = 'Person'
        verbose_name_plural = 'People'

    def __str__(self):
        return self.name