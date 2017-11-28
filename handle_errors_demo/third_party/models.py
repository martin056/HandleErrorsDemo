import uuid

from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name} {self.email}'


class CustomerFromGroup(models.Model):
    member_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    group = models.ForeignKey(Group,
                              on_delete=models.CASCADE,
                              related_name='customers_from_group')
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE,
                                 related_name='customers_from_group')

    class Meta:
        unique_together = (('member_id', 'group'), )

    def __str__(self):
        return f'{self.customer.name} from {self.group.name}'


class Invoice(models.Model):
    identifier = models.UUIDField(primary_key=True, default=uuid.uuid4)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    customer_from_group = models.ForeignKey(CustomerFromGroup,
                                            on_delete=models.CASCADE,
                                            related_name='invoices')

    @property
    def customer(self):
        return self.customer_from_group.customer
