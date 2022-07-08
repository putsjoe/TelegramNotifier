
from unittest import mock
from unittest.mock import patch
from urllib.error import HTTPError

import pytest

from app import app as notifyapp
from app import auth
from data import Config


@pytest.fixture()
def app():
    app = notifyapp
    app.config.update({
        'TESTING': True,
    })
    yield app


@pytest.fixture()
def client(app, monkeypatch):
    monkeypatch.setattr('app.config', Config(None, None, 'Nothing'))
    return app.test_client()


@pytest.fixture()
def auth_client(app, monkeypatch):
    client = app.test_client()
    monkeypatch.setattr(auth, 'authenticate', lambda x, y: True)
    monkeypatch.setattr('app.config', Config(None, None, 'Nothing'))
    yield client


class R: pass
def mockr(url): return R()
def mock_error(bot_token, user_id, message):
    raise HTTPError(url='', code=404, msg='error', hdrs='', fp='')


def test_notify_json(client):
    """Test notify works with a json post"""
    with patch('app.urllib.request.urlopen', mockr):
        response = client.post('/notify', json={
            'message': 'Hello',
            'key': 'Nothing',
        })
    assert response.status_code == 200
    assert response.json == {'message': 'OK'}


def test_notify_form(client):
    """Test notify works with form POST"""
    with patch('app.urllib.request.urlopen', mockr):
        response = client.post('/notify', data={
            'message': 'Hello',
            'key': 'Nothing',
        })
    assert response.status_code == 200
    assert response.json == {'message': 'OK'}


def test_user_admin_auth(client):
    """Test that a request to the admin page is rejected if not authenticated"""
    response = client.get('/user-admin')
    assert response.status_code == 401


def test_user_admin(auth_client):
    """Test the user admin page can be accessed"""
    response = auth_client.get('/user-admin')
    assert response.status_code == 200


def test_invalid_telegram_request(client):
    """Test the 400 response when the Telegram API cant be connected to"""
    with patch('app.send_message', mock_error):
        response = client.post('/notify', data={
            'message': 'Hello',
            'key': 'Nothing',
        })
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid user id or bot token'}



