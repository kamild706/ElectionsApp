from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from elections.models import Candidate, Answer


class ElectionVoteForm(forms.Form):
    candidates = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

    def __init__(self, election=None, *args, **kwargs):
        super(ElectionVoteForm, self).__init__(*args, **kwargs)

        if election is not None:
            self.election = election
            items = [(i.id, i.get_full_name()) for i in Candidate.objects.filter(election=election)]
            self.fields['candidates'].choices = items

    def clean(self):
        cleaned_data = super(ElectionVoteForm, self).clean()
        candidates_id = cleaned_data.get('candidates')
        if candidates_id is not None:
            if len(candidates_id) == 0:
                self.add_error('candidates', 'Nie oddano głosu')
            if len(candidates_id) > self.election.votes_per_voter:
                self.add_error('candidates', 'Zagłosowano na więcej kandydatów niż dozwolono')
            for c_id in candidates_id:
                try:
                    self.election.candidates.get(id=c_id)
                except Candidate.DoesNotExist:
                    self.add_error('candidates', 'Zagłosowano na nieistniejącego kandydata')
        else:
            self.add_error('candidates', 'Nie oddano głosu')

        return cleaned_data


class QuestionnaireVoteForm(forms.Form):
    answers = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

    def __init__(self, questionnaire=None, *args, **kwargs):
        super(QuestionnaireVoteForm, self).__init__(*args, **kwargs)

        if questionnaire is not None:
            self.questionnaire = questionnaire
            items = [(i.id, i.text) for i in Answer.objects.filter(questionnaire=questionnaire)]
            self.fields['answers'].choices = items

    def clean(self):
        cleaned_data = super(QuestionnaireVoteForm, self).clean()
        answers_id = cleaned_data.get('answers')
        if answers_id is not None:
            if len(answers_id) != 1:
                self.add_error('answers', 'Możesz oddac tylko jeden glos')
            for c_id in answers_id:
                try:
                    self.questionnaire.answer_set.get(id=c_id)
                except Candidate.DoesNotExist:
                    self.add_error('answers', 'Zagłosowano na nieistniejącą odpowiedź...')
        else:
            self.add_error('answer', 'Głos nie został oddany')

        return cleaned_data


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, help_text='Opcjonalnie.', label='Imię')
    last_name = forms.CharField(max_length=30, help_text='Opcjonalnie.', label='Nazwisko')
    email = forms.EmailField(max_length=254, help_text='Wymagane. Podaj prawidłowy adres')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
