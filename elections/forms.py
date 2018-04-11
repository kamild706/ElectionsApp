from django import forms

from elections.models import Candidate, Election


class VoteForm(forms.Form):
    candidates = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

    def __init__(self, election=None, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)

        if election is not None:
            self.election = election
            items = [(i.id, i.get_full_name()) for i in Candidate.objects.filter(election=election)]
            self.fields['candidates'].choices = items

    def clean(self):
        cleaned_data = super(VoteForm, self).clean()
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
