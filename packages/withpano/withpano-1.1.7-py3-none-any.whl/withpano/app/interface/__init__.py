# Create an APISpec
import logging

from flask_restx import Api


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
