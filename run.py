# coding=utf-8
from flask import Flask, render_template, request, redirect, url_for
from datetime import date
from Expense import Expense
app = Flask(__name__)


app.jinja_env.globals.update(str=str)

cost_map = {
    1: Expense("Rolle für Trailer", 20.00, "Dierk", date(2020, 9, 8)),
    2: Expense("Aufkleber Jodijo", 6.99, "Jochen", date(2020, 9, 17))
}


@app.route("/", methods=['GET'])
def handle_get():
    cid: int = request.args.get("cid")
    expense: Expense = Expense("", 0, "", date.today())
    action: str = "Add"

    if not empty(cid):
        expense = cost_map[int(cid)]
        action = "Update"

    if empty(expense.date):
        expense.date = date.today()

    print("Get: cid=" + str(cid) + ": " + str(expense))

    return render_template("fiboco.html", cid=cid, expense=expense, action=action, cost_map=cost_map)


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
    cid = max(cost_map.keys()) + 1
    print("Add: cid=" + str(cid) + ": " + str(expense))
    cost_map[cid] = expense


def update(cid, expense):
    print("Add: cid=" + str(cid) + ": " + str(expense))
    cost_map[int(cid)] = expense


def remove(cid):
    if not empty(cid):
        cost_map.pop(int(cid))
