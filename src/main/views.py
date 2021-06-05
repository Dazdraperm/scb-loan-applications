from django.shortcuts import render, redirect
from django.views import View

from main.forms import LoanAppForm
from main.services import create_paginator, get_completed_forms_loan_app, save_or_create_loan_app_or_none


# View для отображение таблицы данных с заявками

class LoanAppView(View):
    def get(self, request):
        form = LoanAppForm
        forms = get_completed_forms_loan_app()
        info_in_page, page = create_paginator(request, forms)

        context = {'page': page, 'info_in_page': info_in_page, 'form': form}

        return render(request, 'main/LoanApp.html', context)

    def post(self, request):
        save_or_create_loan_app_or_none(request)

        return redirect('loan_application')
