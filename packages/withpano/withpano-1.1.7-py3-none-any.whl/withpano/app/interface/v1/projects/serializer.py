from flask_restx import fields

from withpano.app.interface import api

project_model = api.model(
    'Project Model', {
        'name': fields.String(required=True),
        # 'type': fields.String(),
    },
    # mask='{name}'
)
parser = api.parser()
# From the request headers
parser.add_argument('x-access-token', location='headers')
