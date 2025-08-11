from django.db import models
from wagtail.models import Orderable


class IncrementingOrderable(Orderable):
    """
    Abstract base model for orderable objects using a `sort_order` field.

    Inherit from this class to automatically add a `sort_order` IntegerField to your model.
    The field is managed so that new instances are appended to the end of the order by default.
    Provides a utility method to get the current maximum sort order value for the model.
    """

    class Meta:
        abstract = True

    def get_sort_order_max(self):
        """
        Returns the maximum value of the `sort_order` field for this model.
        Used to determine the next sort order value when creating new instances.
        If no instances exist, returns 0.
        """
        max_order = self.__class__.objects.aggregate(
            max_order=models.Max("sort_order")
        )["max_order"]
        return max_order or 0

    def save(self, *args, **kwargs):
        # On first save (object creation), set sort_order to max + 1 so new objects are appended.
        if self.pk is None:
            self.sort_order = self.get_sort_order_max() + 1
        super().save(*args, **kwargs)
