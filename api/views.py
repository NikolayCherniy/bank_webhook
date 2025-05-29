from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Organization
from api.serializers import OrganizationSerializer, PaymentSerializer
from api.services import apply_incoming_payment


class BankWebhookView(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        apply_incoming_payment(serializer.validated_data)
        return Response(status=status.HTTP_200_OK)


class OrganizationBalanceView(RetrieveAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    lookup_field = "inn"
