from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Candidate(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name = "Kandydat"
        verbose_name_plural = "Kandydaci"


class Election(models.Model):
    description = models.CharField(max_length=150)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    votes_per_voter = models.IntegerField()
    voters = models.ManyToManyField(User, through='Participation')
    candidates = models.ManyToManyField(Candidate, through='Candidacy')

    def candidates_number(self):
        return self.candidates.count()
    candidates_number.short_description = 'Number of candidates'

    def is_active(self):
        return self.start_date <= timezone.now() <= self.end_date

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Wybory"
        verbose_name_plural = "Wybory"


class Participation(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    voted = models.BooleanField(default=False)

    class Meta:
        unique_together = ['election', 'voter']

    def __str__(self):
        return str(self.election)


class Candidacy(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)

    class Meta:
        unique_together = ['candidate', 'election']

    def __str__(self):
        return str(self.election) + " " + str(self.candidate) + " " + str(self.votes)
