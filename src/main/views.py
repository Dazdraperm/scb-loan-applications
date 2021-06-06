from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from main.forms import LoanAppForm, AuthForm, RegistrationForm
from main.services import create_paginator, get_completed_forms_loan_app, save_or_create_loan_app_or_none, \
    get_json_loan_app, register_user, get_status_on_loan_app, set_status_on_loan_app, delete_status_on_loan_app


def auth_page(request):
    form = AuthForm()
    if request.method == "POST":
        form = AuthForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)

            if user is None:
                form.add_error("email", "Неправильный логин или пароль")
            else:
                login(request, user)
                return redirect("loan_application")

    return render(request, "main/auth.html", {"form": form})


def registration_page(request):
    form = AuthForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = register_user(email, password)
            login(request, user)
            return redirect("loan_application")

    return render(request, "main/registration.html", {"form": form})


def logout_page(request):
    logout(request)
    return redirect("loan_application")


# View для отображение таблицы данных с заявками
class LoanAppView(LoginRequiredMixin, View):
    def get(self, request):
        # Для создания новой заявки
        form = LoanAppForm

        # Все заявки. Принимаемый парамаетр - это сортировка
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

        # Принимаемый парамаетр - это сортировка
        forms = get_completed_forms_loan_app(None)
        info_in_page, page = create_paginator(request, forms)
        context = {'page': page, 'info_in_page': info_in_page, 'form': form}

        return render(request, 'main/loan_app.html', context)


@login_required
def search(request):
    json = get_json_loan_app(request)

    return HttpResponse(json)


@login_required
def check_status(request):
    return HttpResponse(get_status_on_loan_app(request))


@login_required
def set_status(request):
    set_status_on_loan_app(request)
    return HttpResponse('')


@login_required
def delete_status(request):
    delete_status_on_loan_app(request)
    return HttpResponse('')
