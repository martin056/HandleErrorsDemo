from celery import Task

from handle_errors_demo.demo.mixins import BaseErrorHandlerMixin


class InvoicesPlusBaseTask(BaseErrorHandlerMixin, Task):
    pass
