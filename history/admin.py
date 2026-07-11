from django.contrib import admin
from .models import SearchHistory, ViewHistory

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('query_text', 'user', 'created_at')

@admin.register(ViewHistory)
class ViewHistoryAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'viewed_at')
