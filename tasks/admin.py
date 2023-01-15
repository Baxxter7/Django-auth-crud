from django.contrib import admin
from .models import Task

#Para mostrar el campo de fecha de creacion en el panel de administrador
class TaskAdmin(admin.ModelAdmin):
  readonly_fields = ("created", )

# Register your models here.
admin.site.register(Task, TaskAdmin)