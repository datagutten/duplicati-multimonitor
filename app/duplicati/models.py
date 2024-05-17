import json
import uuid

from django.db import models
from django.utils.timesince import timesince


# Create your models here.
class Host(models.Model):
    # ip = models.GenericIPAddressField(primary_key=True)
    key = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    url = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    version = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name or self.key

    def last_run(self) -> 'Run':
        jobs = self.jobs.exclude(runs=None).order_by('runs__begin')
        if jobs:
            return jobs.last().runs.last()
        pass

    def get_version(self):
        if self.version:
            return self.version
        else:
            last_run = self.last_run()
            # jobs = self.jobs.exclude(runs=None)
            if last_run and last_run.end:
                version = last_run.data['Version']
                self.version = version
                self.save()
                return version


class Job(models.Model):
    host = models.ForeignKey(Host, related_name='jobs', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def lastRun(self) -> 'Run':
        return self.runs.last()

    def lastSuccess(self) -> 'Run':
        return self.runs.exclude(end=None).last()

    def size(self):
        run = self.lastSuccess()
        if run:
            return run.data['SizeOfExaminedFiles']

    class Meta:
        ordering = ['name']


class Run(models.Model):
    job = models.ForeignKey(Job, related_name='runs', on_delete=models.CASCADE)
    report = models.DateTimeField(auto_now_add=True)
    begin = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    data = models.JSONField()
    # data_raw = models.TextField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)

    # size = models.BigIntegerField()

    class Meta:
        unique_together = ['job', 'begin']

    def success(self):
        return self.end is not None

    def host(self):
        return self.job.host

    def runtime(self):
        if self.begin and self.end:
            # return self.end - self.begin
            return timesince(self.end, self.begin)

    def get_status(self):
        if self.result:
            return self.result
        else:
            if 'ParsedResult' in self.data:
                self.result = self.data['ParsedResult']
            elif not self.end:
                self.result = 'Failed'
            self.save()
            return self.result
        pass

    def status_class(self):
        if not self.begin:
            return 'Error'
        if not self.end:
            # return 'text-bg-warning'
            return 'Warning'
        if self.success():
            return 'Success'
        return ''
        # status = self.get_status()
        # mappings = {
        #     'Success': 'alert-success text-bg-success',
        #     'Failed': 'alert-danger text-bg-danger',
        #     # 'Warning': 'text-bg-warning',
        # }
        # if status in mappings:
        #     return mappings[status]
        # else:
        #     return status

    def status_style_var(self):
        if 'Message' in self.data:
            return 'var(--bs-danger-bg-subtle)'
        if not self.end:
            return 'var(--bs-warning-bg-subtle)'

        mappings = {
            'Success': '--bs-success-bg-subtle',
            'Failed': '--bs-danger-bg-subtle',
            'Warning': '--bs-warning-bg-subtle',
        }
        status = self.get_status()
        if status in mappings:
            return 'var(%s)' % mappings[status]
        else:
            return 'none'

    @property
    def size(self):
        if 'SizeOfExaminedFiles' in self.data:
            return self.data['SizeOfExaminedFiles']
        else:
            return None

    def backup_size(self):
        if 'BackendStatistics' in self.data:
            return self.data['BackendStatistics']['KnownFileSize']

    def size_class(self):
        if self.size == 0:
            return 'alert-danger'
        elif self.size is None:
            return 'alert-warning'
        else:
            return 'alert-success'
