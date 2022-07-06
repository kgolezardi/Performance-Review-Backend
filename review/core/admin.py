from django.contrib import admin

from core.models import ProjectReview, PersonReview, ProjectComment, Settings, ManagerPersonReview, \
    ManagerProjectComment, Round, Participation, Answer, Question


class ProjectReviewAdmin(admin.ModelAdmin):
    list_display = ('round', 'project_name', 'reviewee', 'get_reviewers')

    def get_reviewers(self, obj):
        return ', '.join(obj.reviewers.values_list('username', flat=True))

    get_reviewers.short_description = 'Reviewers'


class ProjectCommentAdmin(admin.ModelAdmin):
    list_display = ('get_round', 'get_project_name', 'reviewer', 'get_reviewee')

    def get_round(self, obj):
        return obj.project_review.round

    get_round.short_description = 'Round'

    def get_project_name(self, obj):
        return obj.project_review.project_name

    get_project_name.short_description = 'Project name'

    def get_reviewee(self, obj):
        return obj.project_review.reviewee

    get_reviewee.short_description = 'Reviewee'


class PersonReviewAdmin(admin.ModelAdmin):
    list_display = ('round', 'reviewer', 'reviewee')


class ManagerProjectCommentAdmin(admin.ModelAdmin):
    list_display = ('get_round', 'get_project_name', 'get_reviewee')

    def get_round(self, obj):
        return obj.project_review.round

    get_round.short_description = 'Round'

    def get_project_name(self, obj):
        return obj.project_review.project_name

    get_project_name.short_description = 'Project name'

    def get_reviewee(self, obj):
        return obj.project_review.reviewee

    get_reviewee.short_description = 'Reviewee'


class ManagerPersonReviewAdmin(admin.ModelAdmin):
    list_display = ('round', 'reviewee')


class RoundAdmin(admin.ModelAdmin):
    list_display = ('title', 'phase')


class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('user', 'round', 'has_started_self_review', 'has_started_peer_review',
                    'has_started_manager_review', 'has_started_results')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('get_round', 'get_question_type', 'get_reviewer', 'get_reviewee', 'get_preview')

    def get_round(self, obj):
        if obj.projectreview_set.exists():
            return obj.projectreview_set.first().round
        if obj.projectcomment_set.exists():
            return obj.projectcomment_set.first().project_review.round
        return '----'

    get_round.short_description = 'Round'

    def get_question_type(self, obj):
        if obj.projectreview_set.exists():
            return 'Self project review'
        if obj.projectcomment_set.exists():
            return 'Peer project comment'
        return '----'

    get_question_type.short_description = 'Question Type'

    def get_reviewer(self, obj):
        if obj.projectreview_set.exists():
            return obj.projectreview_set.first().reviewee
        if obj.projectcomment_set.exists():
            return obj.projectcomment_set.first().reviewer
        return '----'

    get_reviewer.short_description = 'Reviewer'

    def get_reviewee(self, obj):
        if obj.projectreview_set.exists():
            return obj.projectreview_set.first().reviewee
        if obj.projectcomment_set.exists():
            return obj.projectcomment_set.first().project_review.reviewee
        return '----'

    get_reviewee.short_description = 'Reviewee'

    def get_preview(self, obj):
        return obj.value[:50] if obj.value else ''

    get_preview.short_description = 'Preview'


admin.site.register(ProjectReview, ProjectReviewAdmin)
admin.site.register(ProjectComment, ProjectCommentAdmin)
admin.site.register(PersonReview, PersonReviewAdmin)
admin.site.register(ManagerPersonReview, ManagerPersonReviewAdmin)
admin.site.register(ManagerProjectComment, ManagerProjectCommentAdmin)
admin.site.register(Round, RoundAdmin)
admin.site.register(Settings)
admin.site.register(Participation, ParticipationAdmin)
admin.site.register(Question)
admin.site.register(Answer, AnswerAdmin)
