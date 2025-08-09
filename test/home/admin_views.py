from wagtail_orderable_viewset.viewset import OrderableModelViewSet, OrderableSnippetViewSet
from .models import Testimonial, TeamMember, FAQItem, Service, Person


class TestimonialViewSet(OrderableModelViewSet):
    model = Testimonial

    form_fields = ['name', 'company', 'content', 'rating', 'is_featured']
    # sort order is included for debugging only
    list_display = ['name', 'company', 'rating', 'is_featured', 'sort_order']
    list_filter = ['is_featured']
    list_export = ['name', 'company', 'rating', 'is_featured']
    search_fields = ['name', 'company', 'content']
    order_by = ['name']

    menu_label = 'Testimonials'
    icon = 'folder-open-1'
    menu_order = 100
    
    add_to_admin_menu = True


testimonial_viewset = TestimonialViewSet('testimonial')


class TeamMemberViewSet(OrderableModelViewSet):
    model = TeamMember

    form_fields = ['name', 'position', 'bio', 'email', 'photo']
    list_display = ['name', 'position', 'email']
    search_fields = ['name', 'position', 'bio', 'email']
    order_by = ['name']

    menu_label = 'Team members'
    icon = 'user'
    menu_order = 110
    add_to_admin_menu = True


team_member_viewset = TeamMemberViewSet('team_member')


class FAQItemViewSet(OrderableModelViewSet):
    model = FAQItem

    form_fields = ['question', 'answer', 'category', 'is_active']
    list_display = ['question', 'category', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['question', 'answer']
    order_by = ['question']

    menu_label = 'FAQ items'
    icon = 'help'
    menu_order = 120
    add_to_admin_menu = True


faq_item_viewset = FAQItemViewSet('faq_item')


class ServiceViewSet(OrderableModelViewSet):
    model = Service

    form_fields = ['title', 'description', 'price', 'is_featured']
    list_display = ['title', 'price', 'is_featured']
    list_filter = ['is_featured']
    search_fields = ['title', 'description']
    order_by = ['title']

    menu_label = 'Services'
    icon = 'tag'
    menu_order = 130
    add_to_admin_menu = True


service_viewset = ServiceViewSet('service')


class PersonViewSet(OrderableSnippetViewSet):
    model = Person
    # sort order is included for debugging only
    list_display = ['name', 'age', 'city', 'team', 'is_active', 'sort_order']
    order_by = ['name']
    list_export = ['name', 'age', 'city', 'team', 'is_active']

person_viewset = PersonViewSet()