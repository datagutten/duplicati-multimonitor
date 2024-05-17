from django.contrib import admin
from duplicati import models


# Register your models here.

@admin.register(models.Host)
class HostAdmin(admin.ModelAdmin):
    list_display = ['name', 'key', 'get_version']
    readonly_fields = ['key']

    @admin.display(description='Duplicati version')
    def get_version(self, obj: models.Host):
        return obj.get_version()


@admin.register(models.Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['host', 'name', 'lastrun_begin', 'lastrun_success']
    list_filter = ['host']

    @admin.display(description='Last run')
    def lastrun_begin(self, obj: models.Job):
        if obj.lastRun():
            return obj.lastRun().begin

    @admin.display(description='Success')
    def lastrun_success(self, obj: models.Job):
        if obj.lastRun():
            return obj.lastRun().success()


@admin.register(models.Run)
class RunAdmin(admin.ModelAdmin):
    list_display = ['host', 'job', 'begin', 'success']
    list_filter = ['job']
