from django.contrib import admin

from core.models import Project, ProjectReview, PersonReview, ProjectComment, Settings, ManagerPersonReview, \
    ManagerProjectComment, Round, Participation


class ProjectReviewAdmin(admin.ModelAdmin):
    list_display = ('round', 'project', 'reviewee', 'get_reviewers')

    def get_reviewers(self, obj):
        return ', '.join(obj.reviewers.values_list('username', flat=True))

    get_reviewers.short_description = 'Reviewers'


class ProjectCommentAdmin(admin.ModelAdmin):
    list_display = ('get_round', 'get_project', 'reviewer', 'get_reviewee')

    def get_round(self, obj):
        return obj.project_review.round

    get_round.short_description = 'Round'

    def get_project(self, obj):
        return obj.project_review.project

    get_project.short_description = 'Project'

    def get_reviewee(self, obj):
        return obj.project_review.reviewee

    get_reviewee.short_description = 'Reviewee'


class PersonReviewAdmin(admin.ModelAdmin):
    list_display = ('round', 'reviewer', 'reviewee')


class ManagerProjectCommentAdmin(admin.ModelAdmin):
    list_display = ('get_round', 'get_project', 'get_reviewee')

    def get_round(self, obj):
        return obj.project_review.round

    get_round.short_description = 'Round'

    def get_project(self, obj):
        return obj.project_review.project

    get_project.short_description = 'Project'

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


admin.site.register(Project)
admin.site.register(ProjectReview, ProjectReviewAdmin)
admin.site.register(ProjectComment, ProjectCommentAdmin)
admin.site.register(PersonReview, PersonReviewAdmin)
admin.site.register(ManagerPersonReview, ManagerPersonReviewAdmin)
admin.site.register(ManagerProjectComment, ManagerProjectCommentAdmin)
admin.site.register(Round, RoundAdmin)
admin.site.register(Settings)
admin.site.register(Participation, ParticipationAdmin)
