import os
from urllib.error import HTTPError
import urllib.request
from uuid import uuid4
from urllib.parse import quote_plus

from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, redirect, request, abort, render_template
from flask_httpauth import HTTPBasicAuth

from data import get_config


USERNAME = os.environ.get('USER_NAME','admin')
PASSWORD = generate_password_hash(os.environ.get('USER_PASS', 'admin'))
ADMIN_URL = os.environ.get('ADMIN_URL', 'user-admin')
NOTIFY_URL = os.environ.get('NOTIFY_URL', 'notify')


app = Flask(__name__)
auth = HTTPBasicAuth()
config = get_config()


def send_message(bot_token, user_id, message):
    urllib.request.urlopen(
        f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={user_id}&text={quote_plus(message)}'
    )
    return


@auth.verify_password
def verify_password(username, password):
    if username == USERNAME and check_password_hash(PASSWORD, password):
        return username


@app.route(f'/{NOTIFY_URL}/', methods=['POST'])
def get_data():
    try:
        content = request.json
    except BadRequest:
        content = request.form
    if content.get('key') != config.api_token:
        abort(404)
    try:
        send_message(bot_token=config.bot_token, user_id=config.user_id, message=content.get('message'))
    except HTTPError:
        return {'error': 'Invalid user id or bot token'}, 400

    return {'message': 'OK'}


@app.route(f'/{ADMIN_URL}/', methods=['GET', 'POST'])
@auth.login_required
def user_admin():
    if request.method == 'POST':
        if request.form.get('new_token'):
            config.api_token = str(uuid4())
            config.save()
            return redirect(request.url)

        config.user_id = request.form['user_id']
        config.bot_token = request.form['bot_token']
        config.save()
        return redirect(request.url)
    
    return render_template('admin.html', **config.__dict__)
