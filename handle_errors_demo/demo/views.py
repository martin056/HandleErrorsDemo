from django.shortcuts import render, reverse
from django.http import HttpResponseNotAllowed, HttpResponseRedirect

from handle_errors_demo.demo.tasks import fetch_data_and_store_it
from handle_errors_demo.demo.models import AsyncActionReport


def index(request):
    if request.method == 'GET':
        async_action_report = AsyncActionReport.objects.last()

        if async_action_report:
            status = async_action_report.status
            error_message = async_action_report.error_message

            if not error_message:
                fetch_data_and_store_it.delay()

        else:
            fetch_data_and_store_it.delay()

        return render(request, 'index.html', locals())

    if request.method == 'POST':
        AsyncActionReport.objects.create()

        return HttpResponseRedirect(reverse('demo:index'))

    return HttpResponseNotAllowed(['GET', 'POST'])
