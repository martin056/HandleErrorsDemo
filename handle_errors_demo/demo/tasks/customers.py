from celery import shared_task, chain

from third_party import InvoicesPlusClient

from django.conf import settings

from demo.models import (
    User,
    Organisation,
    InvoicesPlusCustomer,
)
from demo.decorators import chainable

from .base import InvoicesPlusBaseTask


@shared_task(task=InvoicesPlusBaseTask)
def __get_invoices_plus_customer_from_db(organisation_id, user_id, **kwargs):
    result = {
        'ip_customer_id': None,
        'ip_member_id': None
    }

    ip_customer_qs = InvoicesPlusCustomer.objects.filter(
        organisation__id=organisation_id,
        user__id=user_id
    )

    if ip_customer_qs.exists():
        ip_customer = ip_customer_qs.get()

        result['ip_customer_id'] = ip_customer.id
        result['ip_member_id'] = ip_customer.member_id

    return result


@shared_task(task=InvoicesPlusBaseTask)
def __get_customer_from_invoices_plus(result, user_id, **kwargs):
    if result['ip_customer_id'] is not None:
        return result

    client = InvoicesPlusClient(api_key=settings.THIRD_PARTY_API_KEY)

    user = User.objects.get(id=user_id)

    payload = client.get_customer(email=user.email)

    if payload:
        result['ip_member_id'] = payload['member_id']

    return result


@shared_task(task=InvoicesPlusBaseTask)
def __create_customer_in_invoices_plus(result, user_id, **kwargs):
    if result['ip_customer_id'] is not None or result['ip_member_id'] is not None:
        return result

    client = InvoicesPlusClient(api_key=settings.THIRD_PARTY_API_KEY)

    user = User.objects.get(id=user_id)

    payload = client.add_customer(name=user.name, email=user.email)

    if payload:
        result['ip_member_id'] = payload['member_id']

    return result


@shared_task(task=InvoicesPlusBaseTask)
def __create_invoices_plus_customer_in_db(result, organisation_id, user_id, **kwargs):
    if result['ip_customer_id'] is not None:
        return result

    organisation = Organisation.objects.get(id=organisation_id)
    user = User.objects.get(id=user_id)

    ip_customer = InvoicesPlusCustomer.objects.create(
        organisation=organisation,
        user=user,
        member_id=result['ip_member_id']
    )

    result['ip_customer_id'] = ip_customer.id

    return result


# @shared_task(task=InvoicesPlusBaseTask)
@chainable
def ensure_customer(organisation_id, user_id, **kwargs):
    t1 = __get_invoices_plus_customer_from_db.s(organisation_id, user_id, **kwargs)
    t2 = __get_customer_from_invoices_plus.s(user_id, **kwargs)
    t3 = __create_customer_in_invoices_plus.s(user_id, **kwargs)
    t4 = __create_invoices_plus_customer_in_db.s(organisation_id, user_id, **kwargs)

    # return chain(t1, t2, t3, t4).delay()
    return t1, t2, t3, t4