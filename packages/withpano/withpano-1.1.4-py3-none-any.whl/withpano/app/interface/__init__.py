# Create an APISpec
import logging
import os
from functools import wraps
from pathlib import Path

import jwt
from flask import request
from flask_restx import Api, abort

# from main import server

log = logging.getLogger('console')

authorizations = {
    'api_key': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'x-access-token'
    }
}
api = Api(authorizations=authorizations, title='WITHPANO_API', doc='/doc', prefix='/withpano')
# api = Api(server, authorizations=authorizations, title='WITHPANO_API', doc='/doc', prefix='/withpano')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"].split(" ")[1]
        if not token:
            return {
                       "message": "Authentication Token is missing!",
                       "data": None,
                       "error": "Unauthorized"
                   }, 401
        try:
            data = jwt.decode(token, server.config["SECRET_KEY"], algorithms=["HS256"])
            print(data)
            # current_user = models.User().get_by_id(data["user"])
            current_user = data["username"]
            if current_user is None:
                return {
                           "message": "Invalid Authentication token!",
                           "data": None,
                           "error": "Unauthorized"
                       }, 401
            if not current_user:
                abort(403)
        except Exception as e:
            log.exception(e)
            return {
                       "message": "Something went wrong",
                       "data": None,
                       "error": str(e)
                   }, 500

        return f(current_user, *args, **kwargs)

    return decorated


def auth_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "x-auth-token" in request.headers:
            token = request.headers["x-auth-token"]
        if not token:
            return {
                       "message": "Platform Auth Token is missing!",
                       "error": "Unauthorized"
                   }, 401
        try:
            path = Path(f'./project_data/')
            path.mkdir(parents=True, exist_ok=True)
            init_file = os.path.join(path, "_secret.withpano")
            with open(init_file, 'r') as fp:
                auth_token = fp.read()
            fp.close()
            if auth_token != token:
                return {
                           "message": "Invalid Authentication token!",
                           "data": None,
                           "error": "Unauthorized"
                       }, 401
            if not auth_token:
                abort(403)
        except Exception as e:
            log.exception(e)
            return {
                       "message": "Something went wrong",
                       "data": None,
                       "error": str(e)
                   }, 500
        return f(*args, **kwargs)

    return decorated


def get_token_decoded():
    token = request.headers["x-access-token"].split(" ")[1]
    data = jwt.decode(token, server.config["SECRET_KEY"], algorithms=["HS256"])
    current_user = data["username"]
    return token, current_user


def extract_token(token):
    data = jwt.decode(token, server.config["SECRET_KEY"], algorithms=["HS256"])
    current_user = data["username"]
    return token, current_user


def create_jwt(data):
    encode_data = jwt.encode(data, server.config["SECRET_KEY"], algorithm="HS256")
    return encode_data
