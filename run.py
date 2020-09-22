# coding=utf-8
from flask import Flask, render_template, request
from datetime import datetime, date
app = Flask(__name__)

cost_map = {
    1: ["Rolle für Trailer", 20.00, "Dierk", date(2020, 9, 8)],
    2: ["Aufkleber Jodijo", 6.99, "Jochen", date(2020, 9, 17)]
}


@app.route("/", methods=['GET', 'POST'])
def hello():
    cid: int = request.values.get("cid")
    desc = request.values.get("desc")
    amount = request.values.get("amount")
    payer = request.values.get("payer")
    cdate = request.values.get("cdate")

    if cdate is None:
        cdate = date.today()

    if empty(cid) and not empty(desc) and not empty(amount) and not empty(payer):
        add(desc, amount, payer, cdate)

    if not empty(cid) and not empty(desc) and not empty(amount) and not empty(payer):
        update(cid, desc, amount, payer, cdate)

    print("Received: cid=<" + str(cid)
          + "> desc=<" + str(desc)
          + "> amount=<" + str(amount)
          + "> payer=<" + str(payer)
          + "> cdate=<" + str(cdate))

    return render_template("fiboco.html",
                           cid=cid, desc=desc, amount=amount, payer=payer, cdate=cdate, cost_map=cost_map)

def empty(x):
    return x is None or not x

def add(desc, amount, payer, cdate):
    cid = max(cost_map.keys()) + 1
    print("Add: cid=<" + str(cid)
          + "> desc=<" + str(desc)
          + "> amount=<" + str(amount)
          + "> payer=<" + str(payer)
          + "> cdate=<" + str(cdate))

    cost_map[cid] = [desc, amount, payer, cdate]

def update(cid, desc, amount, payer, cdate):
    print("Update: cid=<" + str(cid)
          + "> desc=<" + str(desc)
          + "> amount=<" + str(amount)
          + "> payer=<" + str(payer)
          + "> cdate=<" + str(cdate))

    cost_map[cid] = [desc, amount, payer, cdate]
