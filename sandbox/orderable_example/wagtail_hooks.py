from wagtail import hooks
from .views import (
    testimonial_viewset,
    team_member_viewset,
    faq_item_viewset,
    service_viewset,
    PersonViewSet,
)

from wagtail.snippets.models import register_snippet


@hooks.register('register_admin_viewset')
def register_testimonial_viewset():
    return testimonial_viewset


@hooks.register('register_admin_viewset')
def register_team_member_viewset():
    return team_member_viewset


@hooks.register('register_admin_viewset')
def register_faq_item_viewset():
    return faq_item_viewset


@hooks.register('register_admin_viewset')
def register_service_viewset():
    return service_viewset


register_snippet(PersonViewSet)