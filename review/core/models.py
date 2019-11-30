from django.db import models

from accounts.models import User


CRITERIA = [('sahabiness', 'Sahabiness'), ('problem-solving', 'Problem solving'), ('execution', 'Execution'),
            ('thought-leadership', 'Thought leadership'), ('leadership', 'Leadership'), ('presence', 'Presence')]
EVALUATIONS = [(1, 'Needs improvement'), (2, 'Consistently meets expectations'), (3, 'Exceeds expectations'),
               (4, 'Strongly exceeds expectations'), (5, 'Superb')]


class CriterionEvaluation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    criterion = models.CharField(max_length=20, choices=CRITERIA, blank=False)
    rating = models.IntegerField(choices=EVALUATIONS, blank=False)
    description = models.CharField(max_length=100, blank=False)


# class Projects(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

