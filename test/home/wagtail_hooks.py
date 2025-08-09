from wagtail import hooks
from home.admin_views import (
    person_viewset,
    testimonial_viewset,
    team_member_viewset,
    faq_item_viewset,
    service_viewset,
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


register_snippet(person_viewset)