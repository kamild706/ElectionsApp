from operator import itemgetter

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import ElectionVoteForm, SignUpForm, QuestionnaireVoteForm
from .models import Election, Participation, Questionnaire
from .email import *


def reject_access():
    return Http404('Wskazana strona nie istnieje lub nie masz do niej dostępu')


def index(request):
    if request.user.is_authenticated:
        elections = Election.objects.filter(start_date__lte=timezone.now(),
                                            end_date__gte=timezone.now(),
                                            voters=request.user,
                                            participation__voted=False)

        questionnaires = Questionnaire.objects.filter(start_date__lte=timezone.now(),
                                                      end_date__gte=timezone.now(),
                                                      voters=request.user,
                                                      participation__voted=False)

        context = {'active_elections': elections,
                   'active_questionnaires': questionnaires}
    else:
        context = None

    return render(request, 'elections/index.html', context)


@login_required(login_url='/login')
def election_detail(request, election_id):
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
        form = ElectionVoteForm(election=election)
    else:
        form = ElectionVoteForm(election=election, data=request.POST)
        if form.is_valid():
            participation.voted = True
            participation.save()

            candidates = form.cleaned_data['candidates']
            election.candidacy_set.filter(candidate_id__in=candidates).update(votes=F('votes') + 1)

            sent = send_confirmation_email(request.user, election_id)

            return render(request, 'elections/successful_vote.html', {'eid': election_id,
                                                                      'email_sent': sent})

    return render(request, 'elections/election_detail.html', {
        'form': form,
        'election': election
    })


@login_required(login_url='/login')
def questionnaire_detail(request, election_id):
    try:
        questionnaire = Questionnaire.objects.get(pk=election_id)
    except Questionnaire.DoesNotExist:
        raise reject_access()

    if not questionnaire.is_active():
        raise reject_access()

    try:
        participation = questionnaire.participation_set.get(voter=request.user)
    except Participation.DoesNotExist:
        raise reject_access()

    if participation.voted:
        raise reject_access()

    if request.method == 'GET':
        form = QuestionnaireVoteForm(questionnaire=questionnaire)
    else:
        form = QuestionnaireVoteForm(questionnaire=questionnaire, data=request.POST)
        if form.is_valid():
            participation.voted = True
            participation.save()

            answers = form.cleaned_data['answers']
            questionnaire.answer_set.filter(id__in=answers).update(votes=F('votes') + 1)

            sent = send_confirmation_email(request.user, election_id)

            return render(request, 'elections/successful_vote.html', {'eid': election_id,
                                                                      'email_sent': sent})

    return render(request, 'elections/questionnaire_detail.html', {
        'form': form,
        'questionnaire': questionnaire
    })


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            send_registration_email(user)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'elections/signup.html', {'form': form})


def show_election_report(request, election_id):
    try:
        election = Election.objects.get(pk=election_id)
    except Election.DoesNotExist:
        raise reject_access()

    if not election.is_finished():
        raise reject_access()

    present_voters = election.participation_set.filter(voted=True).count()
    all_voters = election.voters.count()
    attendance = round(present_voters / all_voters * 100, 2)
    candidacies = election.candidacy_set.all()
    casted_votes = sum([e.votes for e in candidacies])

    results = []
    for c in candidacies:
        result = {
            'first_name': c.candidate.first_name,
            'last_name': c.candidate.last_name,
            'votes': c.votes,
            'percent': round(c.votes / casted_votes * 100 if casted_votes > 0 else 0, 2)
        }
        results.append(result)

    sorted_results = sorted(results, key=itemgetter('votes'), reverse=True)

    context = {
        'all_voters': all_voters,
        'election': election,
        'present_voters': present_voters,
        'candidacies': sorted_results,
        'casted_votes': casted_votes,
        'attendance': attendance
    }

    return render(request, 'reports/election_report.html', context)


def show_questionnaire_report(request, questionnaire_id):
    try:
        questionnaire = Questionnaire.objects.get(pk=questionnaire_id)
    except Questionnaire.DoesNotExist:
        raise reject_access()

    if not questionnaire.is_finished():
        raise reject_access()

    present_voters = questionnaire.participation_set.filter(voted=True).count()
    all_voters = questionnaire.voters.count()
    attendance = round(present_voters / all_voters * 100, 2)
    answers = questionnaire.answer_set.all()
    casted_votes = sum([a.votes for a in answers])

    results = []
    for c in answers:
        result = {
            'text': c.text,
            'votes': c.votes,
            'percent': round(c.votes / casted_votes * 100 if casted_votes > 0 else 0, 2)
        }
        results.append(result)

    sorted_results = sorted(results, key=itemgetter('votes'), reverse=True)

    context = {
        'all_voters': all_voters,
        'questionnaire': questionnaire,
        'present_voters': present_voters,
        'answers': sorted_results,
        'casted_votes': casted_votes,
        'attendance': attendance
    }

    return render(request, 'reports/questionnaire_report.html', context)


@login_required(login_url='/login')
def show_report(request, pk):
    try:
        Questionnaire.objects.get(pk=pk)
        return show_questionnaire_report(request, pk)
    except Questionnaire.DoesNotExist:
        try:
            Election.objects.get(pk=pk)
            return show_election_report(request, pk)
        except Election.DoesNotExist:
            raise reject_access()
