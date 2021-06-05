from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import ModelForm, model_to_dict

from main.forms import LoanAppForm
from main.models import Client, LoanApplication


def get_loan_app():
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
        data = {
            'id': loan_app.id,
            'phone_number': loan_app.client_fk.phone_number,
            'product': loan_app.product,
            'solution': loan_app.solution,
            'date_application': loan_app.date_application,
            'comment': loan_app.text_comment
        }
        forms.append(LoanAppForm(initial=data))


def get_completed_forms_loan_app() -> list:
    loan_apps = get_loan_app()
    forms = []
    filling_forms_loan_app(loan_apps, forms)

    return forms


def save_loan_app(id_loan_app, phone_number, product, solution, comment):
    try:
        client = Client.objects.get(phone_number=phone_number)
        loan_app = LoanApplication.objects.get(id=id_loan_app)
        loan_app.client_fk = client
        loan_app.product = product
        loan_app.solution = solution
        loan_app.text_comment = comment

        loan_app.save()
    except Client.DoesNotExist:
        return None
    except LoanApplication.DoesNotExist:
        return None


def create_loan_app(phone_number, product, solution, comment):
    client = Client.objects.get_or_create(phone_number=phone_number)
    LoanApplication.objects.create(client_fk=client[0], solution=solution, text_comment=comment, product=product)


def save_or_create_loan_app_or_none(request):
    form = LoanAppForm(request.POST)

    if form.is_valid():
        id_loan_app = form.cleaned_data['id']
        phone_number = form.cleaned_data['phone_number']
        product = form.cleaned_data['product']
        solution = form.cleaned_data['solution']
        comment = form.cleaned_data['comment']

        # Если id уже есть, значит есть и loan_app
        if id_loan_app:
            save_loan_app(id_loan_app, phone_number, product, solution, comment)
        else:
            create_loan_app(phone_number, product, solution, comment)

    else:
        return None
