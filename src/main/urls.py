from django.urls import path

from main.views import LoanAppView

urlpatterns = [
    path('', LoanAppView.as_view(), name='loan_application')
]