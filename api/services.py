from django.db import IntegrityError, transaction
from django.db.models import F

from api.models import BalanceLog, Organization


@transaction.atomic
def apply_incoming_payment(payment_data):
    try:
        organization = Organization.objects.select_for_update().get(
            inn=payment_data["payer_inn"],
        )
    except Organization.DoesNotExist:
        try:
            with transaction.atomic():
                organization = Organization.objects.create(
                    inn=payment_data["payer_inn"],
                )
        except IntegrityError:
            organization = Organization.objects.select_for_update().get(
                inn=payment_data["payer_inn"],
            )

    try:
        BalanceLog.objects.create(
            operation_id=payment_data["operation_id"],
            delta=payment_data["amount"],
            document_number=payment_data["document_number"],
            document_date=payment_data["document_date"],
            organization=organization,
        )
    except IntegrityError:
        return

    organization.balance = F("balance") + payment_data["amount"]
    organization.save(update_fields=["balance"])
