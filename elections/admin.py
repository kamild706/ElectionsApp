from django.contrib import admin

from .models import Candidate, CandidateInElection, Election, VoterInElection


class ElectionAdmin(admin.ModelAdmin):
    list_display = ('description', 'start_date', 'end_date', 'candidates_number')
    exclude = ('voters',)


class CandidateAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')


class CandidateInElectionAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'election', 'votes')
    exclude = ('votes',)


class VoterInElectionAdmin(admin.ModelAdmin):
    list_display = ('voter', 'election', 'voted')
    exclude = ('voted',)


admin.site.register(Candidate, CandidateAdmin)
admin.site.register(CandidateInElection, CandidateInElectionAdmin)
admin.site.register(Election, ElectionAdmin)
admin.site.register(VoterInElection, VoterInElectionAdmin)
