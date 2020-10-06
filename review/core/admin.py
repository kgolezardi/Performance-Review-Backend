from django.contrib import admin

from core.models import Project, ProjectReview, PersonReview, ProjectComment, Settings, Round


class ProjectReviewAdmin(admin.ModelAdmin):
    list_display = ('project', 'reviewee', 'get_reviewers')

    def get_reviewers(self, obj):
        return ', '.join(obj.reviewers.values_list('username', flat=True))

    get_reviewers.short_description = 'Reviewers'


class ProjectCommentAdmin(admin.ModelAdmin):
    list_display = ('get_project', 'reviewer', 'get_reviewee')

    def get_project(self, obj):
        return obj.project_review.project

    get_project.short_description = 'Project'

    def get_reviewee(self, obj):
        return obj.project_review.reviewee

    get_reviewee.short_description = 'Reviewee'


class PersonReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'reviewee')


class RoundAdmin(admin.ModelAdmin):
    list_display = ('title', 'phase')


admin.site.register(Project)
admin.site.register(ProjectReview, ProjectReviewAdmin)
admin.site.register(ProjectComment, ProjectCommentAdmin)
admin.site.register(PersonReview, PersonReviewAdmin)
admin.site.register(Settings)
admin.site.register(Round, RoundAdmin)
