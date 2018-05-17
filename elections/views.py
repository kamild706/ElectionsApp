from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db.models import F
from django.http import Http404
from django.utils import timezone
from django.views import generic
from django.shortcuts import render, redirect

from elections.forms import VoteForm, SignUpForm
from elections.models import Election, Participation


class IndexView(generic.ListView):
    template_name = 'elections/index.html'
    context_object_name = 'active_elections'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Election.objects.filter(start_date__lte=timezone.now(),
                                           end_date__gte=timezone.now(),
                                           voters=self.request.user,
                                           participation__voted=False)


@login_required(login_url='/login')
def detail(request, election_id):
    def reject_access():
        return Http404('Wskazane wybory nie istnieją lub nie masz do nich dostępu')

    try:
        election = Election.objects.get(pk=election_id)
    except Election.DoesNotExist:
        raise reject_access()

    if not election.is_active():
        raise reject_access()

    try:
        participation = election.participation_set.get(voter=request.user)
    except Participation.DoesNotExist:
        raise reject_access()

    if participation.voted:
        raise reject_access()

    if request.method == 'GET':
        form = VoteForm(election=election)
    else:
        form = VoteForm(election=election, data=request.POST)
        if form.is_valid():
            participation.voted = True
            participation.save()

            candidates = form.cleaned_data['candidates']
            election.candidacy_set.filter(candidate_id__in=candidates).update(votes=F('votes') + 1)

            return render(request, 'elections/successful_vote.html')

    return render(request, 'elections/election_detail.html', {
        'form': form,
        'election': election
    })


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'elections/signup.html', {'form': form})