from django.contrib import admin

from .models import Candidate, Candidacy, Election, Participation, Answer, Questionnaire


class CandidacyInline(admin.TabularInline):
    model = Candidacy
    extra = 1
    exclude = ('votes',)


class ParticipationInline(admin.TabularInline):
    model = Participation
    extra = 1
    exclude = ('voted',)


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1
    exclude = ('votes',)


class ElectionAdmin(admin.ModelAdmin):
    list_display = ('description', 'start_date', 'end_date', 'candidates_number')
    inlines = (CandidacyInline, ParticipationInline)


class CandidateAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')


class QuestionnaireAdmin(admin.ModelAdmin):
    inlines = (ParticipationInline, AnswerInline)


admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Election, ElectionAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin)
