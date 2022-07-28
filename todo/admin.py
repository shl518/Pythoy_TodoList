from django.contrib import admin
from .models import Todo
#admin bug solving
class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(Todo, TodoAdmin) #This will be registered in admin
