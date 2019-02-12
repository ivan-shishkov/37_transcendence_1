from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse


class HomePageView(TemplateView):
    template_name = 'pages/home.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse('users:user_detail', args=[request.user.id]),
            )
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
