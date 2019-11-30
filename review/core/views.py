from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from core.forms import CriterionForm
from .models import CRITERIA, CriterionEvaluation


@login_required
def overview(request):
    return render(request, 'core/overview.html')


@login_required
def criteria(request):
    evaluations = {}
    forms = []
    for criterion, human_name in CRITERIA:
        qs = CriterionEvaluation.objects.filter(user=request.user, criterion=criterion)
        if len(qs) > 0:
            evaluations[criterion] = qs[0]
        else:
            evaluations[criterion] = None

    if request.method == 'POST':
        try:
            for criterion, human_name in CRITERIA:
                forms += [CriterionForm(request.POST, instance=evaluations[criterion], criterion=criterion,
                                        user=request.user)]
                if not forms[-1].is_valid():
                    raise ValidationError
                for form in forms:
                    form.save()
        except ValidationError:
            # ToDo: handle messages
            raise ValidationError
    else:
        for criterion, human_name in CRITERIA:
            forms += [CriterionForm(instance=evaluations[criterion], criterion=criterion, criterion_name=human_name)]
    return render(request, 'core/criteria.html', {'forms': forms})


@login_required
def projects(request):
    return render(request, 'core/projects.html')
