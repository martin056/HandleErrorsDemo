class InvoicesPlusClientException(Exception):
    pass


class CustomerDoesntExist(InvoicesPlusClientException):
    pass


class CustomerAlreadyExists(InvoicesPlusClientException):
    pass


class NegativeAmount(InvoicesPlusClientException):
    pass
