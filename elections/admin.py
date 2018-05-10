from django.contrib import admin

from .models import Candidate, Candidacy, Election, Participation


class CandidacyInline(admin.TabularInline):
    model = Candidacy
    extra = 1
    exclude = ('votes',)
    
    
class ParticipationInline(admin.TabularInline):
    model = Participation
    extra = 1
    exclude = ('voted',)
    
class ElectionAdmin(admin.ModelAdmin):
    list_display = ('description', 'start_date', 'end_date', 'candidates_number')
    inlines = (CandidacyInline, ParticipationInline)


class CandidateAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')


class CandidacyAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'election', 'votes')
    exclude = ('votes',)


class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('voter', 'election', 'voted')
    exclude = ('voted',)


admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Candidacy, CandidacyAdmin)
admin.site.register(Election, ElectionAdmin)
admin.site.register(Participation, ParticipationAdmin)
