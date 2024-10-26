from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import filesizeformat

from duplicati import models


def backup_size(request, job):
    job_obj = get_object_or_404(models.Job, id=job)
    # values = job_obj.runs.values_list('report', 'size')
    data = []
    for run in job_obj.runs.all():
        if run.backup_size():
            data.append({
                'time': run.report.date().isoformat(),
                # 'size': filesizeformat(run.backup_size())
                'size': run.backup_size()/pow(1024,3)
            })
    return JsonResponse(data, safe=False)
