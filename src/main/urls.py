from django.urls import path

from main.views import LoanAppView, search, auth_page, registration_page, logout_page

urlpatterns = [
    path('', LoanAppView.as_view(), name='loan_application'),
    path('search', search, name='search'),
    path('auth/', auth_page, name='auth'),
    path('logout/', logout_page, name='logout'),
    path('registration/', registration_page, name='registration'),

]
