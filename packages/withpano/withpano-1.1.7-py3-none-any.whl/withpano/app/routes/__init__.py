import io
import os

from flask import Blueprint, send_from_directory, request, send_file
from flask_cors import CORS

from withpano import cache, Scenes, CreatScenes
from withpano.app.interface.decorator import extract_token


class Router:
    def __init__(self, app):
        self.server = app
        self.main_page = Blueprint('WithPano', __name__, url_prefix=self.server.config['APP_URL_PREFIX'],
                                   template_folder=os.path.normpath(os.path.join(os.path.dirname(__file__),
                                                                                 f"../{self.server.config['STATIC_PATH']}")))
        CORS(self.main_page, resources='*', allow_headers='*', origins='*', expose_headers='Authorization',
             send_wildcard=True)

    def main_page_router(self):
        @cache.cached(timeout=50)
        @self.main_page.route("/", defaults={'path': ''})
        @self.main_page.route("/<string:path>")
        def serve_main(path):
            return send_from_directory(self.server.static_folder, 'index.html')

        @cache.cached(timeout=50)
        @self.main_page.route("/manifest.json")
        def manifest():
            return send_from_directory(self.server.static_folder, 'manifest.json')

        @cache.cached(timeout=50)
        @self.main_page.route('/favicon.ico')
        def favicon():
            return send_from_directory(self.server.static_folder, 'favicon.ico')

        # SERVER ROUTER

        @cache.memoize(timeout=50)
        @self.main_page.route('/scene/image/<string:scene>/<string:project>')
        def get_scene_image(scene, project):
            args = request.args
            token, user = extract_token(args['token'])
            scenes = Scenes()
            project_scene = CreatScenes(user, project)
            scene = scenes.get_scene(scene, project_scene.proj_base_path)
            return send_file(f'{project_scene.proj_base_path}/scene_uploaded_img/{scene["scene_image"]}',
                             mimetype=scene["mime_type"])

        @cache.memoize(timeout=50)
        @self.main_page.route('/scene/style/<string:scene>/<string:project>')
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

        return self.main_page
