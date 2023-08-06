import logging
import secrets

from flask import request
from flask_restx import Resource

from withpano.app import create_hash, decipher_hash
from withpano.app.interface import api, create_jwt, auth_token_required
from withpano.app.interface.v1.auth.business import UserCreate
from withpano.app.interface.v1.auth.serializer import signin_model, register_model, parser

log = logging.getLogger('console')

ns = api.namespace('auth', description='Add/Update/Comment')


@ns.route('/login')
class SignRequest(Resource):
    @api.expect(signin_model)
    def post(self):
        args = request.json
        print(args)
        users = UserCreate(args['username'])
        try:
            validate_user, salt_key = users.validate_user()
            decode_pass = decipher_hash(salt_key, validate_user['password'])
            if decode_pass == args['password']:
                del validate_user['password']
                encoded_jwt = create_jwt(validate_user)
                return {"token": encoded_jwt}, 200
            else:
                raise "Invalid Credentials"
        except Exception:
            return {
                       "message": "Invalid authentication details!",
                       "data": None,
                       "error": "Unauthorized"
                   }, 401


@ns.route('/register')
@api.expect(parser)
class RegisterRequest(Resource):
    @api.expect(register_model)
    @auth_token_required
    def post(self):
        args = request.json
        token = secrets.token_urlsafe(8)
        hash_value, salt = create_hash(token)
        args['password'] = hash_value
        user_create = UserCreate(args['username'])
        status, path = user_create.create_user_path(args, salt.decode())
        if status:
            return {"username": args['username'], "password": token}, 201
        else:
            return {"message": path}, 403
