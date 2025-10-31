from django.contrib import admin
from .models import Challenge, Submission, UserProfile


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'difficulty', 'max_score', 'is_active', 'created_at']
    list_filter = ['difficulty', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active']

    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'name', 'description', 'max_score')
        }),
        ('Configuration', {
            'fields': ('difficulty', 'is_active')
        }),
        ('Evaluation', {
            'fields': ('evaluation_code',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'challenge', 'score', 'passed', 'submitted_at']
    list_filter = ['passed', 'challenge', 'submitted_at']
    search_fields = ['user__username', 'challenge__name']
    readonly_fields = ['submitted_at', 'execution_time']
    date_hierarchy = 'submitted_at'

    fieldsets = (
        ('Submission Info', {
            'fields': ('user', 'challenge', 'submitted_at')
        }),
        ('Results', {
            'fields': ('score', 'passed', 'feedback', 'execution_time')
        }),
        ('Code', {
            'fields': ('code', 'error_message'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_score', 'get_challenges_completed', 'get_rank', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['total_score', 'created_at']

    def get_challenges_completed(self, obj):
        return obj.get_challenges_completed()
    get_challenges_completed.short_description = 'Challenges Completed'

    def get_rank(self, obj):
        return obj.get_rank()
    get_rank.short_description = 'Rank'
