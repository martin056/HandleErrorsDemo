import time
import uuid
from copy import deepcopy

from django.core.exceptions import PermissionDenied

from .exceptions import (
    CustomerDoesntExist,
    CustomerAlreadyExists,
    NegativeAmount,
)


CUSTOMERS = [
    {'member_id': '946ef82f-0ecb-4bad-9751-83d38d24e485',
     'name': 'Martin',
     'email': 'martin@demo.com'},
    {'member_id': 'e1fe17c9-bc41-4754-904b-220c798b3fc6',
     'name': 'Rado',
     'email': 'rado@demo.com'},
    {'member_id': '20334e60-e9a0-4d73-b7f0-60659f328cef',
     'name': 'Pesho',
     'email': 'pesho@demo.com'}
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
    '946ef82f-0ecb-4bad-9751-83d38d24e485': [
        '19df4745-7c49-48a9-8caa-3cb0a7e3fed7',
        'd968422d-543e-4b9d-968b-97f68dc4d6bb',
        'b1d1f336-b2dd-40c6-a16f-f02b4119f41e',
    ],
    'e1fe17c9-bc41-4754-904b-220c798b3fc6': [
        'e433c07f-b596-47d4-867e-3ca99d52b0dc',
        'dd5e113d-6aaf-4f8e-8b78-88408a2416b5',
        'b8fcb080-eade-49e5-8f03-a0e40e5ab42c',
    ],
    '20334e60-e9a0-4d73-b7f0-60659f328cef': [
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

    def __validate_customer(self, *, member_id: int) -> None:
        customer = None
        for customer_ in CUSTOMERS:
            if customer_['member_id'] == member_id:
                customer_ = customer

        if customer is None:
            raise CustomerDoesntExist(f'Customer with id: {member_id} doesn\'t exist.')

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

    def get_customer(self, *, email: str) -> dict:
        time.sleep(3)

        for customer in CUSTOMERS:
            if customer['email'] == email:
                return customer

        raise CustomerDoesntExist(f'Customer with email: {email} doesn\'t exist.')

    def add_customer(self, *, name: str, email: str) -> dict:
        time.sleep(3)

        for customer in CUSTOMERS:
            if customer['email'] == email:
                raise CustomerAlreadyExists(f'Customer `{email}` already exists.')

        member_id = uuid.uuid4()

        customer = {'member_id': member_id, 'name': name, 'email': email}

        CUSTOMERS.append(customer)
        CUSTOMERS_INVOICES[member_id] = []

        return customer

    def get_invoices(self, *, member_id: int) -> list:
        time.sleep(3)

        customer = self.__get_customer(member_id=member_id)

        return CUSTOMERS_INVOICES[customer['member_id']]

    def add_invoice(self, *, member_id: int, amount: float) -> dict:
        time.sleep(3)

        self.__validate_customer(member_id=member_id)

        if amount < 0:
            raise NegativeAmount(f'Can\'t create invoice with negative amount: {amount}')

        invoice_id = uuid.uuid4()
        invoice = {'id': invoice_id, amount: round(amount, 2)}

        if len(CUSTOMERS_INVOICES[member_id]) == 0:
            CUSTOMERS_INVOICES[member_id] = [invoice]
        else:
            CUSTOMERS_INVOICES[member_id].append(invoice)

        return invoice
