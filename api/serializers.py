from rest_framework import serializers

from api.models import Organization


class PaymentSerializer(serializers.Serializer):
    operation_id = serializers.UUIDField()
    amount = serializers.IntegerField()
    payer_inn = serializers.CharField(max_length=12)
    document_number = serializers.CharField()
    document_date = serializers.DateTimeField()


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ("inn", "balance")
