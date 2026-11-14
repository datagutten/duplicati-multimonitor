import json
import os.path
import re
from datetime import datetime

import django.conf
from dateutil.parser import parse
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from duplicati import models


# Create your views here.

@csrf_exempt
def report(request, key):
    host = get_object_or_404(models.Host, key=key)
    if request.method == 'GET':
        return HttpResponse('Hello %s' % host.name)

    try:
        data_full = json.loads(request.body)
    except Exception as e:
        path = django.conf.settings.MEDIA_ROOT
        date = datetime.now().isoformat().replace(':', '-')
        with open(os.path.join(path, 'body-%s.json' % date), 'wb') as fp:
            fp.write(request.body)
            return HttpResponse('Data saved as %s' % date)
        pass
    # pprint(data)

    if host.machine_id is None:
        host.machine_id = data_full['Extra']['machine-id']
        host.save()
    job_name = data_full['Extra']['backup-name']
    backup_id = data_full['Extra']['backup-id']

    data = data_full['Data']
    if host.version != data['Version']:
        host.version = data['Version']
        host.save()

    try:
        job = host.jobs.get(Q(backup_id=backup_id) | Q(name=job_name))
    except models.Job.DoesNotExist:
        job = models.Job(host=host, name=job_name, backup_id=backup_id)
        job.save()

    if job.backup_id is None:
        job.backup_id = backup_id
        job.save()
    run = models.Run(job=job, data=data_full)
    if 'BeginTime' in data:
        run.begin = data['BeginTime']
        run.end = data['EndTime']
    elif 'Message' in data:
        matches = re.search(r'([\d/]+\s[\d:]+)', data['Message'])
        if matches:
            run.begin = parse(matches.group(1))

    run.save()
    return HttpResponse('OK %d' % run.id)
    pass
