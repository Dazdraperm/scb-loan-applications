from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import ModelForm, model_to_dict

from main.forms import LoanAppForm
from main.models import Client, LoanApplication


def get_info():
    return LoanApplication.objects.all().select_related('client_fk').order_by('id')


def create_paginator(request, data):
    object_list = data
    count_object_on_page = 15

    paginator = Paginator(object_list, count_object_on_page)  # 3 поста на каждой странице
    page = request.GET.get('page')

    try:
        return paginator.page(page), page
    except PageNotAnInteger:
        # Если страница не является целым числом, поставим первую страницу
        return paginator.page(1), page
    except EmptyPage:
        # Если страница больше максимальной, доставить последнюю страницу результатов
        return paginator.page(paginator.num_pages), page


def filling_forms_loan_app(loan_apps, forms):
    for loan_app in loan_apps:
        data = {'phone_number': loan_app.client_fk.phone_number,
                'product': loan_app.product,
                'solution': loan_app.solution,
                'date_application': loan_app.date_application,
                'comment': loan_app.text_comment
                }

        forms.append(LoanAppForm(initial=data))


def get_filling_forms_loan_app() -> list:
    loan_apps = get_info()
    forms = []
    filling_forms_loan_app(loan_apps, forms)

    return forms
