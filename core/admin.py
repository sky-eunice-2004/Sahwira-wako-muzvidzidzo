from django.contrib import admin
from .models import Branch, Tag, Project, StudentProject, Suggestion, UserProfile

admin.site.register(Branch)
admin.site.register(Tag)
admin.site.register(Project)
admin.site.register(StudentProject)
admin.site.register(Suggestion)
admin.site.register(UserProfile)
