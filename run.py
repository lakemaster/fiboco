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
    cid: int = request.values.get("id")
    desc = request.values.get("desc")
    amount = request.values.get("amount")
    payer = request.values.get("payer")
    cdate = request.values.get("cdate")

    if cdate is None:
        cdate = date.today()

    print("Received: Cid=" + str(cid) + " - " + str(desc))
    return render_template("fiboco.html",
                           cid=cid, desc=desc, amount=amount, payer=payer, cdate=cdate, cost_map=cost_map)
