# coding=utf-8
from datetime import date
from decimal import Decimal


class Expense:
    def __init__(self, description: str, amount: Decimal, payer: str, edate: date):
        self.description: str = description
        self.amount: Decimal = amount
        self.payer: str = payer
        self.date: date = edate

    def __str__(self):
        return "Expense(" \
               + "description=" + self.description + ", " \
               + "amount=" + str(self.amount) + ", " \
               + "payer=" + self.payer + ", " \
               + "date=" + str(self.date) + ")"
