from flask_restx import fields

from withpano.app.interface import api

signin_model = api.model(
    'Signin Model', {
        'username': fields.String(),
        'password': fields.String(),
    }
)
# FOR USER REGISTER
parser = api.parser()
# From the request headers
parser.add_argument('x-auth-token', location='headers')

register_model = api.model(
    'SignUp Model', {
        'username': fields.String(),
        'full_name': fields.String(),
        # 'role': fields.String(),
        # 'access_limit': fields.List(fields.String()),
    }
)
