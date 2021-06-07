import json

from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.serializers.json import DjangoJSONEncoder
from django.forms import model_to_dict

from main.forms import LoanAppForm
from main.models import Client, LoanApplication, StatusEdit
from django.core.exceptions import FieldError
from django.db.utils import DataError


def register_user(email, password):
    """Регистрация нового пользователя"""
    user = User(email=email, username=email)
    user.set_password(password)
    user.save()
    return user


def get_loan_app(field_sort=None):
    try:
        if field_sort:
            split_field_sort = field_sort.split('-')
            if split_field_sort[1] == 'from_top':
                return LoanApplication.objects.all().select_related().order_by(split_field_sort[0])[::-1]
            elif split_field_sort[1] == 'from_down':
                return LoanApplication.objects.all().select_related().order_by(split_field_sort[0])
    except FieldError:
        pass
    return LoanApplication.objects.all().select_related().order_by('id')


def create_paginator(request, data):
    object_list = data
    count_object_on_page = 15

    paginator = Paginator(object_list, count_object_on_page)
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
    """ Заполняет формы данными """

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


def get_completed_forms_loan_app(field_sort) -> list:
    """ Отдает список с заполненными формами """
    loan_apps = get_loan_app(field_sort)
    forms = []

    # Меняет словарь, поэтому ничего не возвращает
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


def create_loan_app_and_client(phone_number, product, solution, comment):
    client = Client.objects.get_or_create(phone_number=phone_number)
    LoanApplication.objects.create(client_fk=client[0], solution=solution, text_comment=comment, product=product)


def save_or_create_loan_app_or_none(form):
    id_loan_app = form.cleaned_data['id']
    phone_number = form.cleaned_data['phone_number']
    product = form.cleaned_data['product']
    solution = form.cleaned_data['solution']
    comment = form.cleaned_data['comment']

    # Если id уже есть, значит есть и loan_app
    if id_loan_app:
        save_loan_app(id_loan_app, phone_number, product, solution, comment)
    else:
        create_loan_app_and_client(phone_number, product, solution, comment)


def get_json_loan_app(request):
    name_field = request.GET.get('what').split('_', 1)[1]
    value_field = request.GET.get('value')

    # LIMIT 1, чтобы не мучаться с парсингом json на фронте
    # Запрос работает в консоли, а здесь нет
    # SELECT * FROM main_loanapplication WHERE client_fk_id LIKE '%111%' ORDER BY date_application LIMIT 1;
    # TODO почему-то LIKE не работает в SQL raw, скорее всего из-за того, что здесь как-то переопределен символ %
    try:
        loan_apps = LoanApplication.objects.raw(
            f'SELECT * FROM main_loanapplication WHERE {name_field} = \'{value_field}\' ORDER BY date_application desc LIMIT 1;')

        loan_app = loan_apps[0]
        dict_loan_app = model_to_dict(loan_app)
        dict_loan_app['date_application'] = loan_app.date_application

        return json.dumps(dict_loan_app, cls=DjangoJSONEncoder)
    except IndexError:
        return None
    except DataError:
        return None


def get_loan_app_on_id_or_none(id):

    try:
        loan_app = LoanApplication.objects.get(id=id)
        return loan_app
    except LoanApplication.DoesNotExist:
        pass
    return None


def get_status_on_loan_app(request):
    loan_app = request.GET.get('loan_application')
    user = int(request.GET.get('user'))
    try:
        status_edit = StatusEdit.objects.get(loan_app=loan_app)
        if not status_edit.status and status_edit.user.id == user:
            return True
        else:
            return False

    except StatusEdit.DoesNotExist:
        return True


def set_status_on_loan_app(request):
    loan_app_id = int(request.GET.get('loan_application'))
    user_id = int(request.GET.get('user'))
    loan_app = get_loan_app_on_id_or_none(loan_app_id)
    user = User.objects.get(id=user_id)
    try:
        status_edit = StatusEdit.objects.get(loan_app=loan_app)
        status_edit.user = user
        status_edit.status = False
        status_edit.save()

    except StatusEdit.DoesNotExist:

        status_edit = StatusEdit(loan_app=loan_app, user=user, status=False)
        status_edit.save()
        return True


def delete_status_on_loan_app(request):
    loan_app_id = int(request.GET.get('loan_application'))
    loan_app = get_loan_app_on_id_or_none(loan_app_id)
    try:
        status_edit = StatusEdit.objects.get(loan_app=loan_app)
        status_edit.delete()
    except StatusEdit.DoesNotExist:
        pass



