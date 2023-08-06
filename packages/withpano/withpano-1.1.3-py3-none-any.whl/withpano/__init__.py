import io
import logging.config
import os

import yaml
from flask import Blueprint, send_from_directory, send_file, request
from flask_cors import CORS
from waitress import serve

from .app import cache, create_auth_token
from .app.interface import api, extract_token
from .app.interface.v1.scenes.business import CreatScenes
from .app.libraries.scenes import Scenes
from .config import BaseConfig

# Initialize Logging
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'logging.conf'))
logging.config.dictConfig(yaml.safe_load(open(logging_conf_path)))
# logging.captureWarnings(True)
log = logging.getLogger('console')


class WithPano:
    def __init__(self):
        self.server = None
        self.config = None
        self.cache = cache

    def init_app(self, app, config=None):
        self.server = app
        self.config = self.server.config.from_object(config if config else BaseConfig)
        self.server.static_folder = self.server.config['STATIC_PATH']
        # init_app cache app
        self.cache.init_app(self.server)
        api.init_app(self.server)

    def server_start(self, host='0.0.0.0', port=8090, debug=True, threads=4, cleanup_interval=10, url_scheme='http'):
        @self.cache.cached(timeout=50)
        @self.server.route("/", defaults={'path': ''})
        @self.server.route("/<string:path>")
        def serve_main(path):
            return send_from_directory(self.server.static_folder, 'index.html')

        @self.cache.cached(timeout=50)
        @self.server.route("/manifest.json")
        def manifest():
            return send_from_directory(self.server.static_folder, 'manifest.json')

        @self.cache.cached(timeout=50)
        @self.server.route('/favicon.ico')
        def favicon():
            return send_from_directory(self.server.static_folder, 'favicon.ico')

        @self.server.route('/cache')
        def get_cache_data():
            print(self.cache.get_dict())
            return send_from_directory(self.server.static_folder, 'favicon.ico')

        # SERVER ROUTER

        @self.cache.memoize(timeout=50)
        @self.server.route('/scene/image/<string:scene>/<string:project>')
        def get_scene_image(scene, project):
            args = request.args
            token, user = extract_token(args['token'])
            scenes = Scenes()
            project_scene = CreatScenes(user, project)
            scene = scenes.get_scene(scene, project_scene.proj_base_path)
            return send_file(f'{project_scene.proj_base_path}/scene_uploaded_img/{scene["scene_image"]}',
                             mimetype=scene["mime_type"])

        @self.cache.memoize(timeout=50)
        @self.server.route('/scene/style/<string:scene>/<string:project>')
        def get_scene_stylesheet(scene, project):
            args = request.args
            token, user = extract_token(args['token'])
            scenes = Scenes()
            project_scene = CreatScenes(user, project)
            scene = scenes.get_scene(scene, project_scene.proj_base_path)
            if 'stylesheet' in scene and scene['stylesheet'] is not None:
                return send_file(f'{project_scene.proj_base_path}/scene_stylesheet/{scene["stylesheet"]}',
                                 mimetype=scene["stylesheet_mime_type"])
            else:
                proxy = io.StringIO()
                # Creating the byteIO object from the StringIO Object
                mem = io.BytesIO()
                mem.write(proxy.getvalue().encode())
                # seeking was necessary. Python 3.5.2, Flask 0.12.2
                mem.seek(0)
                proxy.close()
                return send_file(mem, mimetype="text/css")

        # Import Namespace
        from withpano.app.interface.v1.auth.endpoints import ns as auth_ns
        from withpano.app.interface.v1.projects.endpoints import ns as project_ns
        from withpano.app.interface.v1.scenes.endpoints import ns as scene_ns
        from withpano.app.interface.v1.collab.endpoints import ns as collab_ns

        # API Interface register
        blueprint_api = Blueprint(
            'api', __name__,
            url_prefix='{}api/v1'.format(self.server.config['APP_URL_PREFIX']),
            # static_url_path='/static/site',
            static_folder='static'
        )
        CORS(blueprint_api, resources='*', allow_headers='*', origins='*', expose_headers='Authorization',
             send_wildcard=True)

        api.init_app(blueprint_api)
        api.add_namespace(scene_ns)
        api.add_namespace(auth_ns)
        api.add_namespace(project_ns)
        api.add_namespace(collab_ns)
        self.server.register_blueprint(blueprint_api)

        # AUTH TOKEN GENERATE
        create_auth_token()

        # SERVE APPLICATION ON WEB SERVER
        log.info(f"SERVER STARTED ON: {host}:{port}")
        try:
            if debug:
                self.server.run(debug=True, threaded=True, host='0.0.0.0', port=8090, use_reloader=True)
            else:
                serve(self.server, host=host, port=port, ident="withpano", threads=threads,
                      cleanup_interval=cleanup_interval, url_scheme=url_scheme)
        except Exception as e:
            log.exception(e)
