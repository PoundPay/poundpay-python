#!/usr/bin/env python
from __future__ import unicode_literals
import json
import optparse
import pprint

import poundpay
from flask import (
    Flask, render_template, request, session, abort, make_response)

import config


app = Flask(__name__, static_folder='./fe/static')
app.secret_key = config.SECRET_KEY


@app.route('/')
def index():
    default_payment = config.DEFAULT_PAYMENT
    return render_template(
        'create_payment.html',
        iframe_root_uri=config.IFRAME_ROOT_URI,
        payment_details=session.get('payment_details', default_payment),
        )


@app.route('/user', methods=['POST'])
def create_user():
    user = poundpay.User(**{
        'first_name': request.form['user_first_name'],
        'last_name': request.form['user_last_name'],
        'email_address': request.form['user_email_address'],
    }).save()
    response = make_response(json.dumps(user.__dict__))
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/charge_permission', methods=['POST'])
def create_charge_perm():
    charge_perm_details = request.form.to_dict()
    session['charge_perm_details'] = charge_perm_details
    charge_perm = poundpay.ChargePermission(**charge_perm_details).save()
    response = make_response(json.dumps(charge_perm.__dict__))
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/charge_permission/find', methods=['POST'])
def find_charge_perm():
    email_address = request.form['email_address']
    charge_perms = poundpay.ChargePermission.all(email_address=email_address)
    if not charge_perms:
        abort(404)
    charge_perms = [charge_perm.__dict__ for charge_perm in charge_perms]
    return pprint.pformat(charge_perms)


@app.route('/charge_permission/deactivate', methods=['POST'])
def deactivate_charge_perm():
    charge_perm = poundpay.ChargePermission.find(sid=request.form['sid'])
    charge_perm.state = 'INACTIVE'
    charge = charge_perm.save()
    response = make_response(json.dumps(charge.__dict__))
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/payment', methods=['POST'])
def post_payment():
    payment_details = session['payment_details'] = request.form.to_dict()
    payment = poundpay.Payment(**payment_details).save()
    response = make_response(json.dumps(payment.__dict__))
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/payment/authorize', methods=['POST'])
def authorize_payment():
    sids = request.form.getlist('sid') or request.form.getlist('sid[]')
    if len(sids) > 1:
        payments = poundpay.Payment.batch_update(
            *sids, state='AUTHORIZED')
    else:
        payments = [poundpay.Payment(sid=sids[0], state='AUTHORIZED').save()]
    if len(payments) == 1:
        return pprint.pformat(payments[0].__dict__)
    else:
        return pprint.pformat([p.__dict__ for p in payments])


@app.route('/payment/escrow', methods=['POST'])
def escrow_payment():
    sids = request.form.getlist('sid') or request.form.getlist('sid[]')
    if len(sids) > 1:
        payments = poundpay.Payment.batch_update(
            *sids, state='ESCROWED')
    else:
        payments = [poundpay.Payment(sid=sids[0], state='ESCROWED').save()]
    if len(payments) == 1:
        return pprint.pformat(payments[0].__dict__)
    else:
        return pprint.pformat([p.__dict__ for p in payments])


@app.route('/payment/release', methods=['POST'])
def release_payment():
    payment = poundpay.Payment.find(sid=request.form['sid'])
    payment.release()
    return pprint.pformat(payment.__dict__)


@app.route('/payment/cancel', methods=['POST'])
def cancel_payment():
    payment = poundpay.Payment.find(sid=request.form['sid'])
    payment.cancel()
    return pprint.pformat(payment.__dict__)


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--environment', '-e', default='sandbox')
    parser.add_option('--port', '-p', default=3000, type=int)
    parser.add_option('--host', '-s', default='127.0.0.1')
    options, _args = parser.parse_args()
    poundpay.configure(**config.get_credentials_for_env(options.environment))
    app.run(debug=True, host=options.host, port=options.port)
