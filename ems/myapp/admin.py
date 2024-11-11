from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.
class ProfileInline(admin.StackedInline):
  model = Profile
  can_delete = False

class CustomUserAdmin(UserAdmin):
  inlines = [ProfileInline]
  
class PositionInline(admin.StackedInline):
  model = Position
  extra = 0

class DepartmentAdmin(admin.ModelAdmin):
  model = Department
  inlines = [PositionInline]

class LetterInline(admin.StackedInline):
  model = Letter
  extra = 0

class TopicLetterAdmin(admin.ModelAdmin):
  model = TopicLetter
  inlines = [LetterInline]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Department, DepartmentAdmin)

admin.site.register(TopicLetter, TopicLetterAdmin)

admin.site.register(Sheet)