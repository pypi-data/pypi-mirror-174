import io
import logging
import re
from http.client import responses

from flask import request, send_file
from flask_restx import Resource

from withpano.app import cache
from withpano.app.interface import api, token_required, get_token_decoded, extract_token
from withpano.app.interface.v1.scenes.business import CreatScenes
from withpano.app.interface.v1.scenes.parser import upload_parser
from withpano.app.interface.v1.scenes.type import FileValidation
from withpano.app.libraries.hotspot import Hotspot
from withpano.app.libraries.scenes import Scenes

log = logging.getLogger('console')

ns = api.namespace('scenes', description='Add/Update/Comment')

@ns.route('/create/')
class SceneCreate(Resource):
    @token_required
    @api.expect(upload_parser)
    def post(self, current_user):
        token, user = get_token_decoded()
        args = upload_parser.parse_args()
        uploaded_file = args['file']  # This is FileStorage instance
        uploaded_style_sheet = args['stylesheet']  # This is FileStorage instance
        validate = FileValidation.allowed_file(uploaded_file)

        try:
            validate_stylesheet = FileValidation.allowed_stylesheet_file(uploaded_style_sheet)
        except Exception:
            return {"message": "Stylesheet File Format not supported"}, 500

        scene = CreatScenes(user, args['project'])
        s = args['name']
        s = re.sub(r'[^a-zA-Z1-9\s-]+', '', s)  # remove anything that isn't a letter, space, or hyphen
        s = re.sub(r'\s+', '-', s)  # replace all spaces with hyphens
        if not scene.check_scene_exist(s.lower()):
            if validate and validate_stylesheet:
                fname = scene.save_scene_image(args, s.lower(), uploaded_file, uploaded_style_sheet)
                return {"message": "Scene Information Successfully Saved", "url": fname}, 201
            return {"message": "File Format not supported"}, 500
        return {"message": "Scene Already exist, Try Different Name"}, 500


@cache.cached(timeout=50)
@ns.route('/scene/<string:scene>/<string:project>')
class SceneRequest(Resource):
    @ns.doc(responses=responses)
    @token_required
    def get(self, current_user, scene, project):
        token, user = get_token_decoded()
        scenes = Scenes()
        project_scene = CreatScenes(user, project)
        return scenes.get_scene(scene, project_scene.proj_base_path)


@ns.route('/scene/save/<string:scene>/<string:project>')
class SceneSaveDataRequest(Resource):
    @ns.doc(responses=responses)
    @token_required
    def post(self, current_user, scene, project):
        token, user = get_token_decoded()
        scenes = Scenes()
        project_scene = CreatScenes(user, project)
        return scenes.save_scene(scene, project_scene.proj_base_path, request.json)


# HOTSPOT
@cache.cached(timeout=50)
@ns.route('/hotspot/<string:scene>')
class SceneHotsPotRequest(Resource):
    @ns.doc(responses=responses)
    def get(self, scene):
        hotspot = Hotspot()
        return hotspot.get_all_hotspot(scene)


@cache.cached(timeout=50)
@ns.route('/scene/hotspot/<string:scene>/<string:hid>')
class SceneHotsPotRequest(Resource):
    @ns.doc(responses=responses)
    def get(self, scene, hid):
        hotspot = Hotspot()
        return hotspot.get_hotspot(scene, hid)


# @crossdomain(origin='*', headers=['Access-Control-Allow-Origin', '*'])
@ns.route('/scene/hotspot/<string:scene>')
class SceneHotsPotCreateRequest(Resource):
    @ns.doc(responses=responses)
    # @ns.expect(create_model)
    def post(self, scene):
        print(scene)
        print(request.json)
        # hotspot = Hotspot()
        # return hotspot.create_hotspot(scene, request.json)
        return None
