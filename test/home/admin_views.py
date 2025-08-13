from wagtail_orderable_viewset.viewsets import (
    OrderableModelViewSet,
    OrderableSnippetViewSet,
)
from .models import Testimonial, TeamMember, Person


class TestimonialViewSet(OrderableModelViewSet):
    """
    This viewset provides CRUD functionality for the Testimonial model with ordering capabilities.

    It's based on the OrderableModelViewSet which inherits from Wagtail's ModelViewset

    `search_fields` & `list_filter` is included to demonstrate that the reorder button position
    which will be right aligned in the slim header.
    """

    model = Testimonial

    # sort order is included for debugging only
    list_display = ["name", "company", "rating", "is_featured", "sort_order"]
    list_filter = ["is_featured"]
    list_export = ["name", "company", "rating", "is_featured"]

    form_fields = ["name", "company", "content", "rating", "is_featured"]

    search_fields = ["name", "company", "content"]
    order_by = ["name"]

    menu_label = "Testimonials"
    icon = "folder-open-1"
    menu_order = 100
    add_to_admin_menu = True


testimonial_viewset = TestimonialViewSet("testimonial")


class TeamMemberViewSet(OrderableModelViewSet):
    """
    This viewset provides CRUD functionality for the TeamMember model with ordering capabilities.

    It's based on the OrderableModelViewSet which inherits from Wagtail's ModelViewset.

    `search_fields` & `list_filter` is not included to demonstrate that the reorder button position
    which will be left aligned in the slim header.
    """

    model = TeamMember

    # sort order is included for debugging only
    list_display = ["name", "position", "email", "sort_order"]

    form_fields = ["name", "position", "bio", "email"]

    order_by = ["name"]

    menu_label = "Team members"
    icon = "user"
    menu_order = 110
    add_to_admin_menu = True


team_member_viewset = TeamMemberViewSet("team_member")


class PersonViewSet(OrderableSnippetViewSet):
    """
    This viewset provides CRUD functionality for the Person model with ordering capabilities.

    It's based on the OrderableSnippetViewSet which inherits from Wagtail's SnippetViewset.

    `search_fields` & `list_filter` is included to demonstrate that the reorder button position
    which will be right aligned in the slim header.
    """

    model = Person

    # sort order is included for debugging only
    list_display = ["name", "age", "city", "team", "is_active", "sort_order"]
    list_export = ["name", "age", "city", "team", "is_active"]
    list_filter = ["is_active", "team"]
    search_fields = ["name", "city", "team"]

    order_by = ["name"]

    icon = "user"


person_viewset = PersonViewSet()
