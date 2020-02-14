from django.contrib.postgres.fields import ArrayField
from django.db import models

from accounts.models import User
from core.enums import Evaluation, Phase


class Project(models.Model):
    name = models.CharField(max_length=255, blank=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ProjectReview(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    reviewee = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.CharField(max_length=512, blank=True, null=True)
    rating = models.IntegerField(choices=Evaluation.choices(), blank=True, null=True)
    reviewers = models.ManyToManyField(User, related_name='project_reviews_to_comment')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class ProjectComment(models.Model):
    project_review = models.ForeignKey(ProjectReview, on_delete=models.PROTECT)
    reviewer = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.CharField(max_length=512, blank=True, null=True)
    rating = models.IntegerField(choices=Evaluation.choices(), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class PersonReview(models.Model):
    reviewee = models.ForeignKey(User, on_delete=models.PROTECT, related_name='person_reviews')
    reviewer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='authored_person_reviews')
    sahabiness_rating = models.IntegerField(choices=Evaluation.choices(), null=True, blank=True)
    sahabiness_comment = models.CharField(max_length=280, null=True, blank=True)
    problem_solving_rating = models.IntegerField(choices=Evaluation.choices(), null=True, blank=True)
    problem_solving_comment = models.CharField(max_length=280, null=True, blank=True)
    execution_rating = models.IntegerField(choices=Evaluation.choices(), null=True, blank=True)
    execution_comment = models.CharField(max_length=280, null=True, blank=True)
    thought_leadership_rating = models.IntegerField(choices=Evaluation.choices(), null=True, blank=True)
    thought_leadership_comment = models.CharField(max_length=280, null=True, blank=True)
    leadership_rating = models.IntegerField(choices=Evaluation.choices(), null=True, blank=True)
    leadership_comment = models.CharField(max_length=280, null=True, blank=True)
    presence_rating = models.IntegerField(choices=Evaluation.choices(), null=True, blank=True)
    presence_comment = models.CharField(max_length=280, null=True, blank=True)
    strengths = ArrayField(models.CharField(max_length=280), size=3, null=True, blank=True)
    weaknesses = ArrayField(models.CharField(max_length=280), size=3, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    final_submit = models.BooleanField(default=False, null=False, blank=False)

    def is_self_review(self):
        return self.reviewee == self.reviewer

    class Meta:
        ordering = ['created_at']


class Settings(models.Model):
    phase = models.IntegerField(choices=Phase.choices(), null=False, blank=False)
    due_date = models.DateTimeField(null=True)
    idle_page_url = models.CharField(max_length=512, null=True, blank=True)
    login_background_image = models.CharField(max_length=512, null=True, blank=True)

    class Meta:
        verbose_name_plural = "settings"

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls.objects.get_or_create(phase=Phase.SELF_REVIEW.value)
