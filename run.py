# coding=utf-8
from flask import Flask, render_template, request
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def hello():
    cid: int = request.values.get("id")
    desc = request.values.get("desc")
    amount = request.values.get("amount")
    payer = request.values.get("payer")
    date = request.values.get("date")
    print("Received: Cid=" + str(cid) + " - " + str(desc))
    return render_template("fiboco.html", cid=cid, desc=desc, amount=amount, payer=payer, date=date)
