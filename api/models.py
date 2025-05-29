from django.db import models


class Organization(models.Model):
    inn = models.CharField(max_length=12, unique=True)
    balance = models.PositiveBigIntegerField(default=0)


class BalanceLog(models.Model):
    operation_id = models.UUIDField(unique=True)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="balance_logs",
    )
    delta = models.BigIntegerField()
    document_number = models.CharField(max_length=64)
    document_date = models.DateTimeField()
