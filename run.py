# coding=utf-8
import csv
import uuid
import os
from flask import Flask, render_template, request, redirect, url_for
from datetime import date, datetime
from Expense import Expense
from ExpenseForm import ExpenseForm

app = Flask(__name__)


@app.route("/fiboco", methods=['GET'])
def handle_get():
    form = ExpenseForm(request.args)
    cid: int = form.id.data
    expense: Expense = Expense("", None, "", date.today())
    action: str = "Add"

    if not empty(cid):
        expense = expense_map[int(cid)]
        form.description.data = expense.description
        form.amount.data = expense.amount
        form.payer.data = expense.payer
        form.date.data = expense.date
        action = "Update"

    if empty(expense.date):
        expense.date = date.today()

    print("Get: cid=" + str(cid) + ": " + str(expense))
    print_expense_map("handle_get")

    return render_template("fiboco.html", form=form, expense_map=expense_map, action=action)


@app.route("/fiboco", methods=['POST'])
def handle_post():
    if request.form['submit'] == 'Add' or request.form['submit'] == 'Update':
        form = ExpenseForm(request.form)
        if form.validate():
            cid: int = form.id.data
            expense = Expense(form.description.data, float(form.amount.data), form.payer.data, form.date.data)

            if empty(expense.date):
                expense.date = date.today()

            if empty(cid):
                if not empty(expense.description):
                    add(expense)
            else:
                update(cid, expense)
        else:
            print('validation failed')
            return render_template("fiboco.html", expense_map=expense_map, form=form, action=request.form['submit'])
    elif request.form['submit'] == 'Delete':
        remove(request.form["id"])

    return redirect(url_for("handle_get", id=None))


@app.route('/fiboco/update/<cid>')
def handle_update(cid):
    return redirect(url_for("handle_get", id=cid))


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
                expenses.append(Expense(row[0], float(row[1]), row[2], datetime.strptime(row[3], '%d.%m.%Y').date()))
        print('Expense read from file: ' + str(len(expenses)))
    except FileNotFoundError:
        print('No expense file found')

    return expenses


def write_expenses():
    os.rename(get_file_path(), get_file_path(True))
    with open(get_file_path(), "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for expense in expense_map.values():
            csv_writer.writerow([expense.description, expense.amount, expense.payer,
                                 date.strftime(expense.date, '%d.%m.%Y')])
    print(str(len(expense_map)) + " expenses written to file")


def print_expense_map(context):
    print("Expense map after " + context)
    for cid, expense in expense_map.items():
        print("cid=" + str(cid) + ": " + str(expense))


def get_file_path(unique_extension: bool = False):
    ext = '-' + str(uuid.uuid4()) if unique_extension else ''
    dirpath = os.environ.get('FIBOCO_DATA')
    if empty(dirpath):
        raise ValueError('Environment variable FIBOCO_DATA not set')
    path = os.path.abspath(dirpath + os.sep + 'fiboco' + ext + '.csv')
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

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5001)
