import time
import random

from django.core.exceptions import PermissionDenied

from .models import (
    Group,
    Customer,
    CustomerFromGroup,
    Invoice,
)

from .exceptions import (
    InvoicesPlusClientException,
    CustomerDoesntExist,
    NegativeAmount,
)


class InvoicesPlusClient:
    def __init__(self, group_name, api_key=None):
        self.api_key = api_key

        # Used to demonstrate a usecase where the API may return 403
        if group_name == 'Burgas':
            self.group_name = group_name
        else:
            raise PermissionDenied('Wrong Group name!')

    def __customer_to_dict(self, *, customer: Customer) -> dict:
        return {
            'member_id': customer.customers_from_group.get(group__name=self.group_name).member_id,
            'name': customer.name,
            'email': customer.email,
            'groups': customer.customers_from_group.values_list('group__name')
        }

    def __invoice_to_dict(self, *, invoice: Invoice) -> dict:
        return {
            'identifier': invoice.identifier,
            'amount': invoice.amount,
            'customer': invoice.customer
        }

    def fetch_data_method(self):
        time.sleep(random.randint(0, 3))
        raise InvoicesPlusClientException('Something went wrong...')

    def get_customer(self, *, email: str=None) -> dict:
        time.sleep(3)

        customer_qs = Customer.objects.filter(email=email)

        if customer_qs.exists():
            customer = customer_qs.get()

            return self.__customer_to_dict(customer=customer)

        return {}

    def add_customer(self, *, name: str, email: str) -> dict:
        time.sleep(random.randint(0, 3))

        customer = Customer.objects.create(name=name, email=email)

        group = Group.objects.get(name=self.group_name)

        CustomerFromGroup.objects.create(
            group=group,
            customer=customer
        )

        return self.__customer_to_dict(customer=customer)

    def get_invoices(self, *, member_id: str) -> list:
        time.sleep(random.randint(0, 3))

        qs = CustomerFromGroup.objects.filter(member_id=member_id)

        if qs.exist():
            customer_from_group = qs.get()

            invoices = []
            for invoice in customer_from_group.invoices:
                inv_dict = self.__invoice_to_dict(invoice=invoice)

                invoices.append(inv_dict)

            return invoices

        raise CustomerDoesntExist(f'Customer with member_id: {member_id} is not in {self.group_name}')

    def add_invoice(self, *, member_id: str, amount: float) -> dict:
        time.sleep(random.randint(0, 3))

        if amount < 0:
            raise NegativeAmount(f'Cannot create invoice with amount {amount}')

        qs = CustomerFromGroup.objects.filter(member_id=member_id)

        if qs.exists():
            customer_from_group = qs.get()

            invoice = Invoice.objects.create(amount=amount, customer_from_group=customer_from_group)

            return self.__invoice_to_dict(invoice=invoice)

        raise CustomerDoesntExist(f'Customer with member_id: {member_id} is not in {self.group_name}')
