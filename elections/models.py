from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Candidate(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Election(models.Model):
    description = models.CharField(max_length=50)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    votes_per_user = models.IntegerField()
    voters = models.ManyToManyField(User, blank=True)
    candidates = models.ManyToManyField(Candidate, through='CandidateInElection',)

    def is_active(self):
        return self.start_date <= timezone.now() <= self.end_date

    def __str__(self):
        return self.description


class ElectionAccess(models.Model):
    election = models.OneToOneField(Election, on_delete=models.CASCADE, default=None)
    users = models.ManyToManyField(User)

    def __str__(self):
        return str(self.election)


class CandidateInElection(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return str(self.election) + " " + str(self.candidate) + " " + str(self.votes)
