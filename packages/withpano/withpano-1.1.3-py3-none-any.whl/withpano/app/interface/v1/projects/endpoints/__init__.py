import json
import logging
import os

from flask import request
from flask_restx import Resource

from withpano.app import cache
from withpano.app.interface import api, token_required, get_token_decoded
from withpano.app.interface.v1.projects.business import ProjectCreate
from withpano.app.interface.v1.projects.serializer import project_model, parser

log = logging.getLogger('console')

ns = api.namespace('project', description='Add/Update/Comment')


@ns.route('/create/')
@api.expect(parser)
class ProjectCreateRequest(Resource):
    @api.expect(project_model)
    @token_required
    def post(self, current_user):
        token, user = get_token_decoded()
        args = request.json
        if args['name']:
            create_proj = ProjectCreate(user)
            status, path = create_proj.create_project_path(args['name'])
            return {'status': status, 'path': path}, 201
        else:
            return {'status': "Failed"}, 400
        # return args


@cache.cached(timeout=50)
@ns.route('/list/')
# @api.expect(parser)
class ProjectListRequest(Resource):
    @token_required
    def get(self, current_user):
        token, user = get_token_decoded()
        create_proj = ProjectCreate(user)

        return create_proj.get_projects(), 200


@cache.cached(timeout=50)
@ns.route('/project/view/<string:project>')
@api.expect(parser)
class ProjectViewRequest(Resource):
    @token_required
    def get(self, current_user, project):
        token, user = get_token_decoded()
        create_proj = ProjectCreate(user)
        project_data, path = create_proj.get_project_data(project)
        data_record = []
        for data in project_data:
            if not os.path.isdir(os.path.join(path, data)):
                with open(os.path.join(path, data)) as file_data:
                    data_record.append({"name": data.replace(".json", ""), "record": json.load(file_data)})
        return data_record, 200
