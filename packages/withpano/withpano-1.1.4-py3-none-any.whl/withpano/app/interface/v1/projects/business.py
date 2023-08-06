import logging
import os
import textwrap
from pathlib import Path

log = logging.getLogger('console')


class ProjectCreate:
    def __init__(self, username):
        self.proj_base_path = f"./project_data/{username}"

    def create_project_path(self, project_name):
        try:
            path = Path(f'{self.proj_base_path}/{project_name}')
            path.mkdir(parents=True, exist_ok=True)
            init_file = os.path.join(path, "__init__.py")
            with open(init_file, 'w') as fp:
                fp.write(textwrap.dedent('''\
                            def print_success():
                                print("sucesss")        
                                '''))
            fp.close()
            return True, str(path)
        except FileExistsError as e:
            log.exception(e.filename)
            return False, None

    def get_projects(self):
        return next(os.walk(self.proj_base_path))[1]

    def get_project_data(self, project):
        path = os.path.join(self.proj_base_path, project)
        dir_list = os.listdir(path)
        return dir_list, path
