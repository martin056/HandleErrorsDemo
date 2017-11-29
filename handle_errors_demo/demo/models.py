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
    action = models.CharField(max_length=255)
    system_call = models.BooleanField(default=False)
    error_message = models.TextField(null=True, blank=True)
    error_traceback = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.status


class ThirdPartyDataStorage(models.Model):
    data = models.CharField(max_length=255, null=True, blank=True)


# Extended example models
class Organisation(models.Model):
    name = models.CharField(max_length=255)


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)


class InvoicesPlusCustomer(models.Model):
    member_id = models.CharField(max_length=255, unique=True)

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='invoices_plus_customers')
    organisation = models.ForeignKey(Organisation,
                                     on_delete=models.CASCADE,
                                     related_name='invoices_plus_customers')

    class Meta:
        unique_together = (('organisation', 'member_id'), )

    def __str__(self):
        return self.name

    @property
    def name(self):
        return self.user.name

    @property
    def email(self):
        return self.user.email
