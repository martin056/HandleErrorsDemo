from third_party import ThirdPartyClient
from celery import shared_task, Task, chain

from django.db import transaction
from django.conf import settings

from .models import ThirdPartyDataStorage, AsyncActionReport
from .mixins import BaseErrorHandlerMixin


class ThirdPartyBaseTask(BaseErrorHandlerMixin, Task):
    pass


@shared_task(base=ThirdPartyBaseTask)
def fetch_data(**kwargs):
    """
    Expected kwargs: 'async_action_report_id': AsyncActionReport.id.

    This kwargs is going to be passed to the constructor of
    the ThirdPartyBaseTask so we can handle the exceptions and store it
    in the AsyncActionReport model.
    """
    client = ThirdPartyClient(api_key=settings.THIRD_PARTY_API_KEY)
    fetched_data = client.fetch_data_method()

    return fetched_data


@shared_task
@transaction.atomic  # In case you have complex logic connected to DB transactions
def store_data(fetched_data):
    container = ThirdPartyDataStorage(**fetched_data)
    container.save()

    return container.id


@shared_task
def fetch_data_and_store_it():
    async_action_report = AsyncActionReport.objects.create()
    t1 = fetch_data.s(async_action_report_id=async_action_report.id)
    t2 = store_data.s()

    return chain(t1, t2).delay()
