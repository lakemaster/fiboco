# coding=utf-8
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, date
app = Flask(__name__)


app.jinja_env.globals.update(str=str)

cost_map = {
    1: ["Rolle für Trailer", 20.00, "Dierk", date(2020, 9, 8)],
    2: ["Aufkleber Jodijo", 6.99, "Jochen", date(2020, 9, 17)]
}



@app.route("/", methods=['GET'])
def handleGet():
    cid: int = request.args.get("cid")
    desc: str = None
    amount: str = None
    payer: str = None
    cdate: date = None
    action: str = "Add"

    if not empty(cid):
        desc = cost_map[int(cid)][0]
        amount = cost_map[int(cid)][1]
        payer = cost_map[int(cid)][2]
        cdate = cost_map[int(cid)][3]
        action = "Update"

    if empty(cdate):
        cdate = date.today()

    print("Get: cid=<" + str(cid)
          + "> desc=<" + str(desc)
          + "> amount=<" + str(amount)
          + "> payer=<" + str(payer)
          + "> cdate=<" + str(cdate))

    return render_template("fiboco.html", cid=cid, desc=desc, amount=amount,
                           payer=payer, cdate=cdate, action=action, cost_map=cost_map)


@app.route("/", methods=['POST'])
def handlePost():
    if request.form['submit'] == 'Add' or request.form['submit'] == 'Update':
        cid: int = request.form["cid"]
        desc = request.form["desc"]
        amount = request.form["amount"]
        payer = request.form["payer"]
        cdate = request.form["cdate"]

        if cdate is None:
            cdate = date.today()

        if empty(cid):
            if not empty(desc):
                add(desc, amount, payer, cdate)
        else:
            update(cid, desc, amount, payer, cdate)

        printMap()

    elif request.form['submit'] == 'Delete':
            delete(request.form["cid"])

    return redirect(url_for("handleGet", cid=None))

@app.route('/update/<cid>')
def handleUpdate(cid):
    return redirect(url_for("handleGet", cid=cid))


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

    cost_map[int(cid)] = [desc, amount, payer, cdate]

def delete(cid):
    if not empty(cid):
        cost_map.pop(int(cid))

def printMap():
    for cid in cost_map:
        print(cid, type(cid))
