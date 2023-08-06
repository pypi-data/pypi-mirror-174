import logging

from flask import request
from flask_restx import Resource

from withpano.app import cache
from withpano.app.interface import api, token_required, get_token_decoded
from withpano.app.interface.v1.collab.serializer import email_login_model
from withpano.app.libraries.email_extractor import EmailExtractor

log = logging.getLogger('console')

ns = api.namespace('collab', description='Add/Update/Comment')


@cache.cached(timeout=50)
@ns.route('/mails/')
class EmailsRequest(Resource):
    @api.expect(email_login_model)
    # @token_required
    def post(self):
        # token, user = get_token_decoded()
        args = request.json
        email_extractor = EmailExtractor(args['server'], args['email'], args['username'], args['password'])
        emails = email_extractor.get_recent_emails('Inbox', 100)
        return email_extractor.all_emails(emails), 200
