import re

from django.core.exceptions import ValidationError
from django.db import models
from djchoices import DjangoChoices, ChoiceItem

""" ↓ Дополнительные классы, для модели LoanApplication ↓ """


class Solutions(DjangoChoices):
    Approved = ChoiceItem('Одобрено')
    Denied = ChoiceItem('Отказано')
    Temporary_refusal = ChoiceItem('Временный отказ')


class Products(DjangoChoices):
    Auto = ChoiceItem('Авто')
    Consumer = ChoiceItem('Потреб')
    Deposit = ChoiceItem('Залог')
    Mortgage = ChoiceItem('Ипотека')


""" ↑ """

# По сути рудимент ,т.к. я взял за p_k номер клиента =>  в LoanApplication fk = phone_number
class Client(models.Model):
    phone_number = models.CharField(max_length=10, verbose_name='Номер клиента', primary_key=True)

    def clean(self):
        if not re.match(r'[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]', str(self.phone_number)):
            return ValidationError('Number phone is not correct, please enter number for mask - 0000000000')


class LoanApplication(models.Model):
    client_fk = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    date_application = models.DateTimeField(verbose_name='Время подачи заявки', auto_now_add=True)
    product = models.CharField(choices=Products.choices, verbose_name='На что кредит', max_length=15)
    solution = models.CharField(choices=Solutions.choices, verbose_name='Решение по кредиту', max_length=15, null=True,
                                blank=True)
    # Выбрал не TextField, чтобы задать длину, для большего контроля за памятью
    text_comment = models.CharField(max_length=250, verbose_name='Текст комментария', null=True, blank=True)

    class Meta:
        ordering = ['-client_fk_id']


# Таблица для задания статуса edit/not edit для 4 задания
class StatusEdit(models.Model):
    status = models.BooleanField(verbose_name='Статус поля')
    # True - можно менять
    loan_app = models.OneToOneField(LoanApplication, on_delete=models.CASCADE, default=True)
