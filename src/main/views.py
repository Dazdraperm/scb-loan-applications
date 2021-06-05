from django.shortcuts import render
from django.views import View
from main.services import create_paginator, get_filling_forms_loan_app


# View для отображение таблицы данных с заявками
class LoanAppView(View):
    def get(self, request):
        forms = get_filling_forms_loan_app()
        info_in_page, page = create_paginator(request, forms)

        context = {'page': page, 'info_in_page': info_in_page}

        return render(request, 'main/LoanApp.html', context)

    def post(self, request):
        pass
