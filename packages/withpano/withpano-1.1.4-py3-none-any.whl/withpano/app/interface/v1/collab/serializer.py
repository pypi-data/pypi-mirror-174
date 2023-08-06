from flask_restx import fields

from withpano.app.interface import api

email_login_model = api.model(
    'Email Login Model', {
        'username': fields.String(required=True),
        'email': fields.String(required=True),
        'server': fields.String(required=True, default="outlook.office365.com"),
        'password': fields.String(required=True),
    },
)
parser = api.parser()
# From the request headers
parser.add_argument('x-access-token', location='headers')
