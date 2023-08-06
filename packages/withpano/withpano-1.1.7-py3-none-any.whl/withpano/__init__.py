import logging.config
import os
import socket
from pathlib import Path

import yaml
from flask import Blueprint
from flask_cors import CORS
from termcolor import colored
from waitress import serve

from .app import cache, create_auth_token
from .app.interface import api
from .app.interface.v1.scenes.business import CreatScenes
from .app.libraries import wpconfig
from .app.libraries.scenes import Scenes
from .app.routes import Router
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
        self.server.static_folder = os.path.normpath(
            os.path.join(os.path.dirname(__file__), f"../{self.server.config['STATIC_PATH']}"))
        # init_app cache app
        print(self.server.static_folder)
        self.cache.init_app(self.server)
        api.init_app(self.server)
        wpconfig.init_app(self.server)

    def template_builder(self):
        path = Path(os.path.join(self.server.static_folder, '../src'))
        print(path)
        if os.path.exists(path):
            build_path = os.path.normpath(os.path.join(os.path.dirname(__file__), f"../templates"))
            print(build_path)
            os.system(f"cd {build_path} ; npm run build")
            # subprocess.run(["npm", "run", "build"], cwd=build_path)

    def get_Host_name_IP(self):
        try:
            host_name = socket.gethostname().lower()
            host_ip = socket.gethostbyname(host_name)
            return host_name, host_ip
        except:
            raise "System Error for HOSTNAME"

    def server_start(self, host='0.0.0.0', port=8090, debug=True, threads=4, cleanup_interval=10, url_scheme='http'):
        # BUILD TEMPLATE
        # self.template_builder()
        # REGISTER MAIN PAGE ROUTER
        main_page = Router(app=self.server)
        self.server.register_blueprint(main_page.main_page_router())

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
        sys_host, sys_ip = self.get_Host_name_IP()
        log.info(f"SERVER STARTED ON: {host}:{port}")
        log.info(
            colored(f"APPLICATION WEB ACCESS URL: {url_scheme}://{sys_host}:{port}{self.server.config['APP_URL_PREFIX']}",
                    "green"))
        log.info(
            colored(
                f"APPLICATION WEB ACCESS URL: {url_scheme}://{sys_ip}:{port}{self.server.config['APP_URL_PREFIX']}",
                "green"))
        try:
            if debug:
                self.server.run(debug=True, threaded=True, host='0.0.0.0', port=8090, use_reloader=True)
            else:
                serve(self.server, host=host, port=port, ident="withpano", threads=threads,
                      cleanup_interval=cleanup_interval, url_scheme=url_scheme)
        except Exception as e:
            log.exception(e)
