from django.contrib import admin

from core.models import Project, ProjectReview, PersonReview, ProjectComment, Settings


class ProjectReviewAdmin(admin.ModelAdmin):
    list_display = ('project', 'reviewee')


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


admin.site.register(Project)
admin.site.register(ProjectReview, ProjectReviewAdmin)
admin.site.register(ProjectComment, ProjectCommentAdmin)
admin.site.register(PersonReview, PersonReviewAdmin)
admin.site.register(Settings)
