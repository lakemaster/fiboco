# coding=utf-8
import csv
import os

from flask import Flask, render_template, request, redirect, url_for
from datetime import date
from Expense import Expense
app = Flask(__name__)


@app.route("/", methods=['GET'])
def handle_get():
    cid: int = request.args.get("cid")
    expense: Expense = Expense("", None, "", date.today())
    action: str = "Add"

    if not empty(cid):
        expense = expense_map[int(cid)]
        action = "Update"

    if empty(expense.date):
        expense.date = date.today()

    print("Get: cid=" + str(cid) + ": " + str(expense))
    print_expense_map("handle_get")

    return render_template("fiboco.html", cid=cid, expense=expense, action=action, expense_map=expense_map)


@app.route("/", methods=['POST'])
def handle_post():
    if request.form['submit'] == 'Add' or request.form['submit'] == 'Update':
        cid: int = request.form["cid"]
        expense = Expense(request.form["desc"], request.form["amount"], request.form["payer"], request.form["cdate"])

        if empty(expense.date):
            expense.date = date.today()

        if empty(cid):
            if not empty(expense.description):
                add(expense)
        else:
            update(cid, expense)
    elif request.form['submit'] == 'Delete':
        remove(request.form["cid"])

    return redirect(url_for("handle_get", cid=None))


@app.route('/update/<cid>')
def handle_update(cid):
    return redirect(url_for("handle_get", cid=cid))


def empty(x):
    return x is None or not x


def add(expense: Expense):
    cid = 0 if len(expense_map) == 0 else max(expense_map.keys()) + 1
    print("Add: cid=" + str(cid) + ": " + str(expense))
    expense_map[cid] = expense
    write_expenses()


def update(cid, expense):
    print("Add: cid=" + str(cid) + ": " + str(expense))
    expense_map[int(cid)] = expense
    write_expenses()


def remove(cid):
    if not empty(cid):
        expense_map.pop(int(cid))
    write_expenses()


def read_expenses(file_path):
    expenses: list = []
    try:
        with open(file_path, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')
            for row in csv_reader:
                expenses.append(Expense(row[0], row[1], row[2], row[3]))
        print('Expense read from file: ' + str(len(expenses)))
    except FileNotFoundError:
        print('No expense file found')

    return expenses


def write_expenses():
    with open(get_file_path(), "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for expense in expense_map.values():
            csv_writer.writerow([expense.description, expense.amount, expense.payer, expense.date])
    print(str(len(expense_map)) + " expenses written to file")


def print_expense_map(context):
    print("Expense map after " + context)
    for cid, expense in expense_map.items():
        print("cid=" + str(cid) + ": " + str(expense))


def get_file_path():
    dirpath = os.environ.get('FIBOCO_DATA')
    if empty(dirpath):
        raise ValueError('Environment variable FIBOCO_DATA not set')
    path = os.path.abspath(dirpath + os.sep + 'fiboco.csv')
    print('Filepath=' + path)
    return path


def create_expenses_map(source_expences_list):
    expenses = sorted(source_expences_list, key=lambda e: e.date, reverse=True)
    local_expense_map: dict = {}
    i = 0
    for expence in expenses:
        local_expense_map[i] = expence
        i += 1
    return local_expense_map


app.jinja_env.globals.update(str=str)
expense_map: dict = create_expenses_map(read_expenses(get_file_path()))

