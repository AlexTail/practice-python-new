from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

usd = 56.80
eur = 70.53
rub = 1.0
eur_to_usd = 1.24


class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float)
    currency = db.Column(db.String(3))
    overdraft = db.Column(db.Boolean)

    def __init__(self, balance, currency, overdraft):
        self.currency = currency
        self.overdraft = overdraft
        self.balance = balance


class BankAccountSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'balance', 'currency', 'overdraft')


ba_schema = BankAccountSchema()
ba_schema = BankAccountSchema(many=True)


# endpoint to create new bank account
@app.route("/newba", methods=["POST"])
def add_ba():
    balance = request.json['balance']
    currency = request.json['currency']
    overdraft = request.json['overdraft']
    new_ba = BankAccount(balance, currency, overdraft)
    db.session.add(new_ba)
    db.session.commit()
    return jsonify(new_ba.id)


# endpoint to show all accounts
@app.route("/allbas", methods=["GET"])
def get_bas():
    all_ba = BankAccount.query.all()
    result = ba_schema.dump(all_ba)
    return jsonify(result)


# endpoint to show account
@app.route("/ba", methods=["POST"])
def get_ba():
    id = request.json['accountID']
    ba = BankAccount.query.get(id)
    print(ba)
    balance = ba.balance
    print(balance)
    currency = ba.currency
    print(currency)
    return jsonify(str(balance) + ' ' + str(currency))


# endpoint to delete bank account
@app.route("/deleteaccount", methods=["DELETE"])
def ba_delete():
    id = request.json['accountID']
    ba = BankAccount.query.get(id)
    db.session.delete(ba)
    db.session.commit()
    resp = 'Account was deleted'
    return jsonify(resp)


# endpoint to do transaction
@app.route("/transaction", methods=["PUT"])
def transaction():
    _json = request.json
    donorID = _json['donorID']
    recipientID = _json['recipientID']
    value = _json['value']

    donor = BankAccount.query.get(donorID)
    recipient = BankAccount.query.get(recipientID)
    
    donor_cur = donor.currency
    recipient_cur = recipient.currency
    transaction_cur = donor_cur

    if donor_cur != 'RUB':
        if donor_cur == 'EUR':
            donor_balance = donor.balance * eur
        if donor_cur == 'USD':
            donor_balance = donor.balance * usd
    else:
        donor_balance = donor.balance

    if recipient_cur != 'RUB':
        if recipient_cur == 'EUR':
            recipient_balance = recipient.balance * eur
        if recipient_cur == 'USD':
            recipient_balance = recipient.balance * usd
    else:
        recipient_balance = recipient.balance

    if donor.balance >= value or donor.overdraft == True:
        donor.balance = donor.balance - value
        
        if recipient_cur != donor_cur:
            if recipient_cur == 'EUR' and donor_cur == 'USD':
                recipient.balance = recipient.balance + value / eur_to_usd
            if recipient_cur == 'USD' and donor_cur == 'EUR':
                recipient.balance = recipient.balance + value * eur_to_usd

            if recipient_cur == 'RUB' and donor_cur == 'EUR':
                recipient.balance = recipient.balance  + value * eur    
            if recipient_cur == 'EUR' and donor_cur == 'RUB':
                recipient.balance = recipient.balance  + value/eur

            if recipient_cur == 'USD' and donor_cur == 'RUB':
                recipient.balance = recipient.balance  + value/usd
            if recipient_cur == 'RUB' and donor_cur == 'USD':
                recipient.balance = recipient.balance  + value * usd                            
        
        else:
            recipient.balance = recipient.balance + value

        resp = 'Success'
    else:
        resp = 'Error'
    db.session.commit()
    return jsonify(resp)


if __name__ == '__main__':
    app.run(debug=True)