from django.db import models
from wagtail.models import Orderable


class IncrementingOrderable(Orderable):
    """
    Abstract model that provides a sort_order field for ordering functionality.
    
    This mixin adds a sort_order IntegerField to any model that inherits from it.
    The field is managed by the ordering functionality.
    """

    class Meta:
        abstract = True

    def get_sort_order_max(self):
        """
        Get the maximum sort_order value for this model.
        Useful when creating new instances.
        """
        max_order = self.__class__.objects.aggregate(
            max_order=models.Max('sort_order')
        )['max_order']
        return max_order or 0

    def save(self, *args, **kwargs):
        if self.pk is None:
            setattr(self, self.sort_order_field, self.get_sort_order_max() + 1)
        super().save(*args, **kwargs)
