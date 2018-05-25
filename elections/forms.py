from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from elections.models import Candidate, Election, Answer


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
            if len(candidates_id) > self.election.votes_per_voter:
                self.add_error('candidates', 'Exceeded maximal number of votes')
            for c_id in candidates_id:
                try:
                    self.election.candidates.get(id=c_id)
                except Candidate.DoesNotExist:
                    self.add_error('candidates', 'Voted for nonexistent candidate')
        else:
            self.add_error('candidates', 'No vote was cast')

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
            if len(answers_id) > 1:
                self.add_error('answers', 'You can choose only one answer')
            for c_id in answers_id:
                try:
                    self.questionnaire.answer_set.get(id=c_id)
                except Candidate.DoesNotExist:
                    self.add_error('answers', 'Voted for nonexistent answer')
        else:
            self.add_error('answer', 'No vote was cast')

        return cleaned_data

        
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, help_text='Optional.')
    last_name = forms.CharField(max_length=30, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
