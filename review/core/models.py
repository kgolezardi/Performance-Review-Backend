from django.contrib.postgres.fields import ArrayField
from django.db import models

from accounts.models import User
from core.enums import Evaluation, Phase, State

MAX_TEXT_LENGTH = 10000


class Project(models.Model):
    name = models.CharField(max_length=255, blank=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Round(models.Model):
    title = models.CharField(max_length=512, null=False, blank=True)
    phase = models.IntegerField(choices=Phase.choices(), null=False, blank=False)
    participants = models.ManyToManyField(User)
    projects = models.ManyToManyField(Project)
    start_text_self_review = models.TextField(blank=True, null=True)
    start_text_peer_review = models.TextField(blank=True, null=True)
    start_text_manager_review = models.TextField(blank=True, null=True)
    start_text_results = models.TextField(blank=True, null=True)
    start_text_idle = models.TextField(blank=True, null=True)
    manager_overall_review_text = models.TextField(blank=True, null=True)

    def is_at_phase(self, phase):
        return self.phase == phase.value

    @property
    def start_text(self):
        if self.is_at_phase(Phase.SELF_REVIEW):
            return self.start_text_self_review
        if self.is_at_phase(Phase.PEER_REVIEW):
            return self.start_text_peer_review
        if self.is_at_phase(Phase.MANAGER_REVIEW):
            return self.start_text_manager_review
        if self.is_at_phase(Phase.RESULTS):
            return self.start_text_results
        if self.is_at_phase(Phase.IDLE):
            return self.start_text_idle

    def __str__(self):
        return self.title


class ProjectReview(models.Model):
    round = models.ForeignKey(Round, on_delete=models.PROTECT)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    reviewee = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.TextField(blank=True, null=True)
    rating = models.IntegerField(choices=Evaluation.choices(), blank=True, null=True)
    reviewers = models.ManyToManyField(User, related_name='project_reviews_to_comment')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class ProjectComment(models.Model):
    project_review = models.ForeignKey(ProjectReview, on_delete=models.PROTECT)
    reviewer = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.TextField(blank=True, null=True)
    rating = models.IntegerField(choices=Evaluation.choices(), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class ManagerProjectComment(models.Model):
    project_review = models.ForeignKey(ProjectReview, on_delete=models.PROTECT)
    rating = models.IntegerField(choices=Evaluation.choices(), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class PersonReview(models.Model):
    round = models.ForeignKey(Round, on_delete=models.PROTECT)
    reviewee = models.ForeignKey(User, on_delete=models.PROTECT, related_name='person_reviews')
    reviewer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='authored_person_reviews')
    sahabiness_rating = models.IntegerField(choices=Evaluation.choices(), null=True, blank=True)
    sahabiness_comment = models.TextField(null=True, blank=True)
    problem_solving_rating = models.IntegerField(choices=Evaluation.choices(), null=True, blank=True)
    problem_solving_comment = models.TextField(null=True, blank=True)
    execution_rating = models.IntegerField(choices=Evaluation.choices(), null=True, blank=True)
    execution_comment = models.TextField(null=True, blank=True)
    thought_leadership_rating = models.IntegerField(choices=Evaluation.choices(), null=True, blank=True)
    thought_leadership_comment = models.TextField(null=True, blank=True)
    leadership_rating = models.IntegerField(choices=Evaluation.choices(), null=True, blank=True)
    leadership_comment = models.TextField(null=True, blank=True)
    presence_rating = models.IntegerField(choices=Evaluation.choices(), null=True, blank=True)
    presence_comment = models.TextField(null=True, blank=True)
    strengths = ArrayField(models.TextField(), size=3, null=True, blank=True)
    weaknesses = ArrayField(models.TextField(), size=3, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    state = models.IntegerField(choices=State.choices(), default=State.TODO.value)

    def is_self_review(self):
        return self.reviewee == self.reviewer

    class Meta:
        ordering = ['created_at']


class ManagerPersonReview(models.Model):
    round = models.ForeignKey(Round, on_delete=models.PROTECT)
    reviewee = models.ForeignKey(User, on_delete=models.PROTECT, related_name='manager_person_reviews')
    sahabiness_rating = models.IntegerField(choices=Evaluation.choices(), null=True, blank=True)
    problem_solving_rating = models.IntegerField(choices=Evaluation.choices(), null=True, blank=True)
    execution_rating = models.IntegerField(choices=Evaluation.choices(), null=True, blank=True)
    thought_leadership_rating = models.IntegerField(choices=Evaluation.choices(), null=True, blank=True)
    leadership_rating = models.IntegerField(choices=Evaluation.choices(), null=True, blank=True)
    presence_rating = models.IntegerField(choices=Evaluation.choices(), null=True, blank=True)
    overall_rating = models.IntegerField(choices=Evaluation.choices(), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class Settings(models.Model):
    active_round = models.ForeignKey(Round, on_delete=models.PROTECT)
    idle_page_url = models.CharField(max_length=512, null=True, blank=True)
    login_background_image = models.CharField(max_length=512, null=True, blank=True)
    logo_url = models.CharField(max_length=512, null=True, blank=True)
    light_logo_url = models.CharField(max_length=512, null=True, blank=True)

    class Meta:
        verbose_name_plural = "settings"

    def __str__(self):
        return 'Settings: %s (%s)' % (self.active_round, self.active_round.phase)

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            # Admin should create settings with the desired round
            raise cls.DoesNotExist


class Participation(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    round = models.ForeignKey(Round, on_delete=models.PROTECT)
    has_started_self_review = models.BooleanField(default=False, null=False, blank=False)
    has_started_peer_review = models.BooleanField(default=False, null=False, blank=False)
    has_started_manager_review = models.BooleanField(default=False, null=False, blank=False)
    has_started_results = models.BooleanField(default=False, null=False, blank=False)
