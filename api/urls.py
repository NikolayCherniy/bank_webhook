from django.urls import path

from api.views import BankWebhookView, OrganizationBalanceView

urlpatterns = [
    path("webhook/bank/", BankWebhookView.as_view()),
    path("organizations/<int:inn>/balance/", OrganizationBalanceView.as_view()),
]
