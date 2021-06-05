from django.shortcuts import render, redirect
from django.views import View
from main.services import create_paginator, get_completed_forms_loan_app, save_loan_app_or_none


# View для отображение таблицы данных с заявками

class LoanAppView(View):
    def get(self, request):
        forms = get_completed_forms_loan_app()
        info_in_page, page = create_paginator(request, forms)

        context = {'page': page, 'info_in_page': info_in_page}

        return render(request, 'main/LoanApp.html', context)

    def post(self, request):
        save_loan_app_or_none(request)

        return redirect('loan_application')
