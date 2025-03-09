from django.views import generic


class RootView(generic.TemplateView):
    template_name = 'root.html'
