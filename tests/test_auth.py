from stackoverflowlite import app
from db.dbconfig import open_connection,close_connection
from flask import json
import pytest


@pytest.fixture
def client():
    test_client = app.test_client()
    return test_client


def test_signup(client):
    user = {"username": "Joekim", "email": "joekim@gmail.com", "password": "password"}
    response = client.post('api/v1/signup', data=json.dumps(user))
    assert json.loads(response.data)["message"] == "User registered successfully"
    conn = open_connection()
    cur = conn.cursor()
    cur.execute("delete from users where username = '{}'".format(user['username']))
    close_connection(conn)

def test_login(client):
    user = {"email": "mirrmaina@gmail.com", "password": "password"}
    response = client.post('api/v1/login', data=json.dumps(user))
    assert response.status_code == 200


def test_empty_email_login(client):
    user = {"email": " ", "password": "password"}
    response = client.post('/api/v1/login', data=json.dumps(user))
    assert response.status_code == 400


def test_empty_username_signup(client):
    response = client.post('api/v1/login', data=dict(username=" ", email="mirrmaina@gmail,com", password="password"))
    assert response.status_code == 400


def test_empty_email_signup(client):
    user = {"username": "username", "email": " ", "password": "password"}
    response = client.post('api/v1/signup', data=json.dumps(user))
    assert response.status_code == 400


def test_empty_password_login(client):
    response = client.post('api/v1/login', data=dict(email="mirrmaina@gmail,com", password=" "))
    assert response.status_code == 400


def test_empty_password_signup(client):
    response = client.post('api/v1/signup', data=dict(email="mirrmaina@gmail,com", password=""))
    assert response.status_code == 400


