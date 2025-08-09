from wagtail_orderable_viewset.viewset import OrderableModelViewSet, OrderableSnippetViewSet
from .models import Testimonial, TeamMember, Person


class TestimonialViewSet(OrderableModelViewSet):
    model = Testimonial

    # sort order is included for debugging only
    list_display = ['name', 'company', 'rating', 'is_featured', 'sort_order']
    list_filter = ['is_featured']
    list_export = ['name', 'company', 'rating', 'is_featured']
    
    form_fields = ['name', 'company', 'content', 'rating', 'is_featured']

    search_fields = ['name', 'company', 'content']
    order_by = ['name']

    menu_label = 'Testimonials'
    icon = 'folder-open-1'
    menu_order = 100
    add_to_admin_menu = True


testimonial_viewset = TestimonialViewSet('testimonial')


class TeamMemberViewSet(OrderableModelViewSet):
    model = TeamMember

    # sort order is included for debugging only
    list_display = ['name', 'position', 'email', 'sort_order']
    
    form_fields = ['name', 'position', 'bio', 'email']
    
    order_by = ['name']

    menu_label = 'Team members'
    icon = 'user'
    menu_order = 110
    add_to_admin_menu = True


team_member_viewset = TeamMemberViewSet('team_member')


class PersonViewSet(OrderableSnippetViewSet):
    model = Person

    # sort order is included for debugging only
    list_display = ['name', 'age', 'city', 'team', 'is_active', 'sort_order']
    list_export = ['name', 'age', 'city', 'team', 'is_active']
    
    order_by = ['name']

    icon = 'user'

person_viewset = PersonViewSet()