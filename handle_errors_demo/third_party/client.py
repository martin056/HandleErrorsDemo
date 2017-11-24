import time
import uuid
from copy import deepcopy

from django.core.exceptions import PermissionDenied

from exceptions import (
    CustomerDoesntExist,
    CustomerAlreadyExists,
    NegativeAmount,
)


CUSTOMERS = [
    {'customer_id': 1, 'name': 'Martin', 'email': 'martin@demo.com'},
    {'customer_id': 2, 'name': 'Rado', 'email': 'rado@demo.com'},
    {'customer_id': 3, 'name': 'Pesho', 'email': 'pesho@demo.com'}
]


INVOICES = [
    {'id': '19df4745-7c49-48a9-8caa-3cb0a7e3fed7', 'amount': '20.00'},
    {'id': 'd968422d-543e-4b9d-968b-97f68dc4d6bb', 'amount': '22.00'},
    {'id': 'b1d1f336-b2dd-40c6-a16f-f02b4119f41e', 'amount': '24.00'},
    {'id': 'e433c07f-b596-47d4-867e-3ca99d52b0dc', 'amount': '26.00'},
    {'id': 'dd5e113d-6aaf-4f8e-8b78-88408a2416b5', 'amount': '28.00'},
    {'id': 'b8fcb080-eade-49e5-8f03-a0e40e5ab42c', 'amount': '30.00'},
    {'id': '095e5068-c31a-4c19-bd08-94b7890a9424', 'amount': '32.00'},
    {'id': '9895249d-a683-4959-9e2e-3fb57722558d', 'amount': '34.00'},
    {'id': '081f361b-f726-48d4-9f6e-ff323ab206ee', 'amount': '36.00'},
    {'id': 'b41b4c12-e0da-475c-a564-ce9b21d3db05', 'amount': '37.00'},
]


CUSTOMERS_INVOICES = {
    1: [
        '19df4745-7c49-48a9-8caa-3cb0a7e3fed7',
        'd968422d-543e-4b9d-968b-97f68dc4d6bb',
        'b1d1f336-b2dd-40c6-a16f-f02b4119f41e',
    ],
    2: [
        'e433c07f-b596-47d4-867e-3ca99d52b0dc',
        'dd5e113d-6aaf-4f8e-8b78-88408a2416b5',
        'b8fcb080-eade-49e5-8f03-a0e40e5ab42c',
    ],
    3: [
        '095e5068-c31a-4c19-bd08-94b7890a9424',
        '9895249d-a683-4959-9e2e-3fb57722558d',
        '081f361b-f726-48d4-9f6e-ff323ab206ee',
        'b41b4c12-e0da-475c-a564-ce9b21d3db05',
    ]
}


class InvoicesPlusClient:
    def __init__(self, api_key):
        # Used to demonstrate a usecase where the API may return 403
        if api_key == 'burgas':
            self.api_key = api_key
        else:
            raise PermissionDenied('Wrong API key!')

    def __validate_customer(self, *, customer_id: int) -> None:
        customer = None
        for customer_ in CUSTOMERS:
            if customer_['customer_id'] == customer_id:
                customer_ = customer

        if customer is None:
            raise CustomerDoesntExist(f'Customer with id: {customer_id} doesn\'t exist.')

    def fetch_data_method(self):
        time.sleep(3)
        raise InvoicesPlusClientException('Something went wrong...')

    def get_customers(self, *, exclude_emails: list=None) -> list:
        time.sleep(3)
        customers = deepcopy(CUSTOMERS)

        if exclude_emails is not None:
            for i, customer in enumerate(customers):
                if customer['email'] in exclude_emails:
                    del customers[i]

        return customers

    def add_customer(self, *, name: str, email: str) -> dict:
        time.sleep(3)

        for customer in CUSTOMERS:
            if customer['email'] == email:
                raise CustomerAlreadyExists(f'Customer `{email}` already exists.')

        customer_id = CUSTOMERS[-1]['customer_id'] + 1

        customer = {'customer_id': customer_id, 'name': name, 'email': email}

        CUSTOMERS.append(customer)
        CUSTOMERS_INVOICES[customer_id] = []

        return customer

    def get_invoices(self, *, customer_id: int) -> list:
        time.sleep(3)

        customer = self.__get_customer(customer_id=customer_id)

        return CUSTOMERS_INVOICES[customer['customer_id']]

    def add_invoice(self, *, customer_id: int, amount: float) -> dict:
        time.sleep(3)

        self.__validate_customer(customer_id=customer_id)

        if amount < 0:
            raise NegativeAmount(f'Can\'t create invoice with negative amount: {amount}')

        invoice_id = uuid.uuid4()
        invoice = {'id': invoice_id, amount: round(amount, 2)}

        if len(CUSTOMERS_INVOICES[customer_id]) == 0:
            CUSTOMERS_INVOICES[customer_id] = [invoice]
        else:
            CUSTOMERS_INVOICES[customer_id].append(invoice)

        return invoice
