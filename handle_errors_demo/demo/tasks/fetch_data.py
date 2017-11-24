from third_party import InvoicesPlusClient
from celery import shared_task, chain

from django.db import transaction
from django.conf import settings

from handle_errors_demo.demo.models import ThirdPartyDataStorage, AsyncActionReport

from .base import InvoicesPlusBaseTask


@shared_task(base=InvoicesPlusBaseTask)
def __fetch_data(**kwargs):
    """
    Expected kwargs: 'async_action_report_id': AsyncActionReport.id.

    This kwargs is going to be passed to the constructor of
    the ThirdPartyBaseTask so we can handle the exceptions and store it
    in the AsyncActionReport model.
    """
    client = InvoicesPlusClient(api_key=settings.THIRD_PARTY_API_KEY)
    fetched_data = client.fetch_data_method()

    return fetched_data


@shared_task
@transaction.atomic  # In case you have complex logic connected to DB transactions
def __store_data(fetched_data):
    container = ThirdPartyDataStorage(**fetched_data)
    container.save()

    return container.id


@shared_task
def fetch_data_and_store_it():
    async_action_report = AsyncActionReport.objects.create()
    t1 = __fetch_data.s(async_action_report_id=async_action_report.id)
    t2 = __store_data.s()

    return chain(t1, t2).delay()
