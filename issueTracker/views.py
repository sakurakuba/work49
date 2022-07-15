from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views import View
from django.views.generic import TemplateView

from issueTracker.models import Issue


class IndexView(View):
    def get(self, request, *args, **kwargs):
        issues = Issue.objects.order_by('-created_at')
        context = {'issues': issues}
        return render(request, "index.html", context)


class IssueView(TemplateView):
    template_name = 'issue_view.html'

    def get_context_data(self, **kwargs):
        pk = kwargs.get("pk")
        issue = get_object_or_404(Issue, pk=pk)
        kwargs["issue"] = issue
        return super().get_context_data(**kwargs)
