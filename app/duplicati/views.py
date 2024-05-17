import json
import os.path
import re
from datetime import datetime

import django.conf
from dateutil.parser import parse
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
        data = json.loads(request.body)
    except Exception as e:
        path = django.conf.settings.MEDIA_ROOT
        date = datetime.now().isoformat().replace(':', '-')
        with open(os.path.join(path, 'body-%s.json' % date), 'wb') as fp:
            fp.write(request.body)
            return HttpResponse('Data saved as %s' % date)
        pass
    # pprint(data)
    job_name = data['Extra']['backup-name']
    data = data['Data']

    job, created = models.Job.objects.get_or_create(name=job_name, host=host)
    run = models.Run(job=job, data=data)
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
