from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'menus/home.html'


class AboutView(TemplateView):
    template_name = 'menus/about.html'


class ServicesView(TemplateView):
    template_name = 'menus/services.html'


class ContactView(TemplateView):
    template_name = 'menus/contact.html'
