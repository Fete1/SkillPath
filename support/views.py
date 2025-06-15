from django.views.generic import ListView, DetailView, CreateView
# ... other views
class HelpCenterView(ListView):
    model = FAQ
    template_name = 'support/help_center.html'
    context_object_name = 'faqs'
    queryset = FAQ.objects.filter(is_active=True)