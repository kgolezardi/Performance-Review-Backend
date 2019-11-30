from django import forms

from core.models import CriterionEvaluation


class CriterionForm(forms.ModelForm):
    class Meta:
        model = CriterionEvaluation
        fields = ['rating', 'description']

    def __init__(self, *args, **kwargs):
        self.criterion = kwargs.pop('criterion', False)
        self.criterion_name = kwargs.pop('criterion_name', False)
        self.user = kwargs.pop('user', False)
        self.prefix = self.criterion
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        evaluation = super().save(commit=False)
        evaluation.criterion = self.criterion
        evaluation.user = self.user
        if commit:
            evaluation.save()
        return evaluation
