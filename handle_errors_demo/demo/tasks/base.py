from celery import Task

from demo.mixins import BaseErrorHandlerMixin


class InvoicesPlusBaseTask(BaseErrorHandlerMixin, Task):
    pass
