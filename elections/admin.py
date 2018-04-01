from django.contrib import admin

from .models import Candidate, CandidateInElection, Election, ElectionAccess


admin.site.register(Candidate)
admin.site.register(CandidateInElection)
admin.site.register(Election)
admin.site.register(ElectionAccess)
