from celery import shared_task

from third_party.client import InvoicesPlusClient

from demo.models import (
    User,
    Organisation,
    InvoicesPlusCustomer,
)
from demo.decorators import chainable
from demo.services import get_signature_and_make_system_call

from .base import InvoicesPlusBaseTask


@shared_task(task=InvoicesPlusBaseTask)
def __get_invoices_plus_customer_from_db(organisation_id, user_id, **kwargs):
    print('Entering t1: ', __get_invoices_plus_customer_from_db.__name__)
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

    print('Exiting t1: ', __get_invoices_plus_customer_from_db.__name__)
    return result


@shared_task(task=InvoicesPlusBaseTask)
def __get_customer_from_invoices_plus(result, organisation_id, user_id, **kwargs):
    print('Entering t2: ', __get_customer_from_invoices_plus.__name__)
    if result['ip_customer_id'] is not None:
        return result

    organisation = Organisation.objects.get(id=organisation_id)

    client = InvoicesPlusClient(group_name=organisation.name)

    user = User.objects.get(id=user_id)

    payload = client.get_customer(email=user.email)

    if payload:
        result['ip_member_id'] = payload['member_id']

    print('Exiting t2: ', __get_customer_from_invoices_plus.__name__)
    return result


@shared_task(task=InvoicesPlusBaseTask)
def __create_customer_in_invoices_plus(result, organisation_id, user_id, **kwargs):
    print('Entering t3: ', __create_customer_in_invoices_plus.__name__)
    if result['ip_customer_id'] is not None or result['ip_member_id'] is not None:
        return result

    organisation = Organisation.objects.get(id=organisation_id)

    client = InvoicesPlusClient(group_name=organisation.name)

    user = User.objects.get(id=user_id)

    payload = client.add_customer(name=user.name, email=user.email)

    if payload:
        result['ip_member_id'] = payload['member_id']

    print('Exiting t3: ', __create_customer_in_invoices_plus.__name__)
    return result


@shared_task(task=InvoicesPlusBaseTask)
def __create_invoices_plus_customer_in_db(result, organisation_id, user_id, **kwargs):
    print('Entering t4: ', __create_invoices_plus_customer_in_db.__name__)
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

    print('Exiting t4: ', __create_invoices_plus_customer_in_db.__name__)
    return result


@chainable
def ensure_customer(organisation_id, user_id, **kwargs):
    task_kwargs = {
        'organisation_id': organisation_id,
        'user_id': user_id
    }

    t1 = get_signature_and_make_system_call(
        action='Getting InvoicesPlusCustomer from DB.',
        task=__get_invoices_plus_customer_from_db,
        task_kwargs=task_kwargs
    )

    t2 = get_signature_and_make_system_call(
        action='Getting Customer from InvoicesPlus.',
        task=__get_customer_from_invoices_plus,
        task_kwargs=task_kwargs
    )

    t3 = get_signature_and_make_system_call(
        action='Creating customer in InvoicesPlus.',
        task=__create_customer_in_invoices_plus,
        task_kwargs=task_kwargs
    )

    t4 = get_signature_and_make_system_call(
        action='Creating InvoicesPlusCustomer in DB.',
        task=__create_invoices_plus_customer_in_db,
        task_kwargs=task_kwargs
    )

    return t1, t2, t3, t4
