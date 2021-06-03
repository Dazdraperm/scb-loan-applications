import re

from django.core.exceptions import ValidationError
from django.db import models
from djchoices import DjangoChoices, ChoiceItem


""" ↓ Дополнительные классы, для модели LoanApplication ↓ """


class Solutions(DjangoChoices):
    Auto = ChoiceItem('Auto')
    Consumer = ChoiceItem('Потреб')
    Deposit = ChoiceItem('Залог')
    Mortgage = ChoiceItem('Ипотека')


class Products(DjangoChoices):
    Approved = ChoiceItem('Одобрено')
    Denied = ChoiceItem('Отказано')
    Temporary_refusal = ChoiceItem('Временный отказ')


""" ↑ """


class Client(models.Model):
    phone_number = models.CharField(max_length=10, verbose_name='Номер клиента', primary_key=True)

    def clean(self):
        if not re.match(r'[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]', str(self.phone_number)):
            return ValidationError('Number phone is not correct, please enter number for mask - 0000000000')


class LoanApplication(models.Model):
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    date_application = models.DateTimeField(auto_now=True, verbose_name='Время подачи заявки')
    product = models.CharField(choices=Products.choices, verbose_name='На что кредит', max_length=15)
    solution = models.CharField(choices=Solutions.choices, verbose_name='Решение по кредиту', max_length=15, null=True,
                                blank=True)


class Comment(models.Model):
    # Выбрал не TextField, чтобы задать длину, для большего контроля за памятью
    text_comment = models.CharField(max_length=250, verbose_name='Текст комментария')
    loan_app = models.ForeignKey(LoanApplication, on_delete=models.CASCADE)
