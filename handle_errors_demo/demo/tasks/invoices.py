from celery import shared_task, chain

from third_party import InvoicesPlusClient

from django.conf import settings

from demo.models import InvoicesPlusCustomer, AsyncActionReport

from .customers import ensure_customer
from .base import InvoicesPlusBaseTask


@shared_task(task=InvoicesPlusBaseTask)
def create_invoice_in_invoices_plus(user_id, amount, **kwargs):
    client = InvoicesPlusClient(api_key=settings.THIRD_PARTY_API_KEY)

    ip_customer = InvoicesPlusCustomer.objects.get(user__id=user_id)

    invoice = client.add_invoice(member_id=ip_customer.member_id, amount=amount)

    return invoice


@shared_task(task=InvoicesPlusBaseTask)
def create_invoice_for_non_existing_customer(organisation_id, user_id, amount, **kwargs):
    async_action_report = AsyncActionReport.objects.create(
        action='Ensuring customer in order to create invoice.',
        system_call=True
    )

    ensure_customer_signatures = ensure_customer(
        organisation_id=organisation_id,
        user_id=user_id
    )

    # create_invoice_signature = create_invoice_in_invoices_plus.s(
    #     user_id=user_id,
    #     amount=amount,
    #     async_action_report_id=async_action_report.id
    # )
    create_invoice_signature = create_invoice_in_invoices_plus.s(
        user_id=user_id,
        amount=amount,
        async_action_report_id=async_action_report.id
    ).set(countdown=0.5)

    return chain(*ensure_customer_signatures, create_invoice_signature).delay()
