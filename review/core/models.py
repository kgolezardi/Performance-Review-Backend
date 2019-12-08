from django.contrib.postgres.fields import ArrayField
from django.db import models

from accounts.models import User
from core.enums import Evaluations


class Project(models.Model):
    name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.name


class ProjectReview(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    reviewee = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.CharField(max_length=512, blank=False)
    rating = models.IntegerField(choices=Evaluations.choices(), blank=False)


class ProjectComment(models.Model):
    project_review = models.ForeignKey(ProjectReview, on_delete=models.PROTECT)
    reviewer = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.CharField(max_length=512, blank=False)
    rating = models.IntegerField(choices=Evaluations.choices(), blank=False)


class PersonReview(models.Model):
    reviewee = models.ForeignKey(User, on_delete=models.PROTECT, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='authored_reviews')
    sahabiness_rating = models.IntegerField(choices=Evaluations.choices(), blank=False)
    sahabiness_comment = models.CharField(max_length=280, blank=False)
    problem_solving_rating = models.IntegerField(choices=Evaluations.choices(), blank=False)
    problem_solving_comment = models.CharField(max_length=280, blank=False)
    execution_rating = models.IntegerField(choices=Evaluations.choices(), blank=False)
    execution_comment = models.CharField(max_length=280, blank=False)
    thought_leadership_rating = models.IntegerField(choices=Evaluations.choices(), blank=False)
    thought_leadership_comment = models.CharField(max_length=280, blank=False)
    leadership_rating = models.IntegerField(choices=Evaluations.choices(), blank=False)
    leadership_comment = models.CharField(max_length=280, blank=False)
    presence_rating = models.IntegerField(choices=Evaluations.choices(), blank=False)
    presence_comment = models.CharField(max_length=280, blank=False)
    strengths = ArrayField(models.CharField(max_length=280), size=3)
    weaknesses = ArrayField(models.CharField(max_length=280), size=3)
