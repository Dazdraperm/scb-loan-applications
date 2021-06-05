from django.shortcuts import render, redirect
from django.views import View
from main.forms import LoanAppForm
from main.services import create_paginator, get_completed_forms_loan_app, save_or_create_loan_app_or_none, \
    get_count_loan_app_in_months


# View для отображение таблицы данных с заявками
class LoanAppView(View):
    def get(self, request):

        # Для создания новой заявки
        form = LoanAppForm

        # Все заявки
        forms = get_completed_forms_loan_app(request.GET.get('sort'))

        # Заявки разделенные на страницы
        forms_on_page, page = create_paginator(request, forms)

        context = {'page': page, 'info_in_page': forms_on_page, 'form': form}

        return render(request, 'main/loan_app.html', context)

    def post(self, request):
        form = LoanAppForm(request.POST)

        if form.is_valid():
            save_or_create_loan_app_or_none(form)

            return redirect('loan_application')

        forms = get_completed_forms_loan_app(None)
        info_in_page, page = create_paginator(request, forms)
        context = {'page': page, 'info_in_page': info_in_page, 'form': form}

        return render(request, 'main/loan_app.html', context)


def count_loan_app_in_months_page(request):

    context = {'data': get_count_loan_app_in_months()}
    return render(request, 'main/loan_app.html', context)
