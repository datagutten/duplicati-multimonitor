import datetime
from collections import OrderedDict

from django.db.models import Max
from django.shortcuts import render, get_object_or_404
from duplicati import models


# Create your views here.

def jobs(request):
    hosts = models.Host.objects.all()
    return render(request, 'monitoring/jobs.html', {"active": {"jobs": True}, 'hosts': hosts})


def run_log(request, run=None):
    if not run:
        run = request.GET.get('run')
    run_obj = models.Run.objects.get(id=run)
    return render(request, 'monitoring/data.html', {"active": {"run_log": True}, 'run': run_obj})


def runs(request):
    job_runs = models.Run.objects.all().order_by('-report')
    return render(request, 'monitoring/runs.html', {"active": {"runs": True}, 'runs': job_runs})


def status_matrix(request, num_days=14):
    today = datetime.date.today()
    timeline = OrderedDict()
    last = today - datetime.timedelta(days=num_days)

    job_runs = models.Run.objects.filter(report__gte=last)
    jobs = models.Job.objects.all()
    jobs = jobs.annotate(last_success_date=Max("runs__begin"))
    jobs = jobs.order_by("host", "last_success_date")

    for job in jobs:
        if job.last_success_date:
            job.days_since_last_success = (today - job.last_success_date.date()).days
        else:
            job.days_since_last_success = 1000

        timeline[job] = []

        for i in range(num_days + 1):
            day = today - datetime.timedelta(days=i)
            classes = set()

            timeline[job].append([classes, day, None])

    for run in job_runs:
        day = (today - run.report.date()).days
        timeline[run.job][day][0].add("run")
        timeline[run.job][day][2] = run

    days = [today - datetime.timedelta(days=i) for i in range(num_days + 1)]
    return render(
        request,
        "monitoring/status_matrix.html",
        {"active": {"status_matrix": True}, "days": days, "timeline": timeline},
    )


def job_info(request, job):
    job_obj = get_object_or_404(models.Job, id=job)
    return render(request, 'monitoring/job.html', {'job': job_obj})


def host_info(request, host):
    pass
