from django.contrib import admin
from django.contrib import admin
from .models import Challenge


# Register your models here.


class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'challenge_user', 'tag', 'challenge_type')
    list_filter = ('date', 'challenge_type')
    search_fields = ('title',)
    prepopulated_fields = {'tag': ('title',)}
    date_hierarchy = 'date'


admin.site.register(Challenge, ChallengeAdmin)
