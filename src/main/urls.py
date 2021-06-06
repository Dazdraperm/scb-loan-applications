from django.urls import path

from main.views import LoanAppView, search, auth_page, registration_page, logout_page, check_status, set_status, \
    delete_status

urlpatterns = [
    path('', LoanAppView.as_view(), name='loan_application'),
    path('search', search, name='search'),
    path('auth/', auth_page, name='auth'),
    path('logout/', logout_page, name='logout'),
    path('registration/', registration_page, name='registration'),
    path('check_status/', check_status, name='check_status'),
    path('set_status/', set_status, name='set_status'),
    path('delete_status/', delete_status, name='delete_status')

]
