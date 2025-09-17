from django.contrib import admin
from .models import Task

# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'owner', 'assignee', 'created_at')
    search_fields = ('title', 'description', 'owner__username', 'assignee__username')
