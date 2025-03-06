from django.views.generic import TemplateView

class RootView(TemplateView):
    template_name = "common/root.html"