from django.db import models

# Base example models
class AsyncActionReport(models.Model):
    PENDING = 'pending'
    OK = 'ok'
    FAILED = 'failed'

    STATUS_CHOICES = (
        (PENDING, 'pending'),
        (OK, 'ok'),
        (FAILED, 'failed')
    )

    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default=PENDING)
    error_message = models.TextField(null=True, blank=True)
    error_traceback = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.status


class ThirdPartyDataStorage(models.Model):
    data = models.CharField(max_length=255, null=True, blank=True)


# Extended example models
class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)


class InvoicesPlusCustomer(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    customer_id = models.CharField(max_length=255, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
