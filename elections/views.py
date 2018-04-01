from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import generic

from elections.models import Election


# def index(request):
#     if request.user.is_authenticated:
#         return HttpResponse("You are in")
#     else:
#         return HttpResponse("You must log in")


class IndexView(generic.ListView):
    template_name = 'elections/index.html'
    context_object_name = 'active_elections'

    def get_queryset(self):
        return Election.objects.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now())
