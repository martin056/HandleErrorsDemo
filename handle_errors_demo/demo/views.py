from django.shortcuts import render
from django.http import HttpResponseNotAllowed

from .tasks import fetch_data_and_store_it
from .models import AsyncActionReport


def index(request):
    if request.method == 'GET':
        async_action_report = AsyncActionReport.objects.last()

        if async_action_report:
            status = async_action_report.status
            error_message = async_action_report.error_message
        else:
            fetch_data_and_store_it.delay()

        return render(request, 'index.html', locals())

    return HttpResponseNotAllowed(['GET'])
