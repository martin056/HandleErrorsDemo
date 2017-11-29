from celery import shared_task, chain

from third_party.client import InvoicesPlusClient

from demo.models import (
    Organisation,
    InvoicesPlusCustomer,
    AsyncActionReport
)

from .customers import ensure_customer
from .base import InvoicesPlusBaseTask


@shared_task(task=InvoicesPlusBaseTask)
def create_invoice_in_invoices_plus(organisation_id, user_id, amount, **kwargs):
    organisation = Organisation.objects.get(id=organisation_id)

    client = InvoicesPlusClient(group_name=organisation.name)

    ip_customer = InvoicesPlusCustomer.objects.get(user__id=user_id)

    invoice = client.add_invoice(member_id=ip_customer.member_id, amount=amount)

    print(f'Created invoice with amount {amount}')
    return invoice


@shared_task(task=InvoicesPlusBaseTask)
def create_invoice_for_non_existing_customer(organisation_id, user_id, amount, **kwargs):
    async_action_report = AsyncActionReport.objects.create(
        action='Ensuring customer in order to create invoice.'
    )

    ensure_customer_signatures = ensure_customer(
        organisation_id=organisation_id,
        user_id=user_id
    )

    create_invoice_signature = create_invoice_in_invoices_plus.si(
        organisation_id=organisation_id,
        user_id=user_id,
        amount=amount,
        async_action_report_id=async_action_report.id
    ).set(countdown=0.5)

    return chain(*ensure_customer_signatures, create_invoice_signature).delay()
