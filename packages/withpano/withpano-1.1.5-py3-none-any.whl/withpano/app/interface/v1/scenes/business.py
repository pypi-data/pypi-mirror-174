import os
from pathlib import Path

import cssutils
from werkzeug.utils import secure_filename

from withpano.app.libraries.scenes import Scenes


class CreatScenes:
    def __init__(self, username, project):
        self.project = project
        self.proj_base_path = f"./project_data/{username}/{self.project}"

    def save_scene_image(self, args, scene_name, uploaded_file, uploaded_style_sheet):
        # SAVE SCENE IMAGE
        filename = secure_filename(uploaded_file.filename)
        extension = filename.split('.')[-1]
        new_filename = "upload-{}.{}".format(
            scene_name, extension
        )
        path = Path(f"{self.proj_base_path}/scene_uploaded_img")
        path.mkdir(parents=True, exist_ok=True)
        uploaded_file.save(os.path.join(path, new_filename))
        ######################################################################
        # SAVE UPLOADED STYLESHEET
        style_new_filename = None
        uploaded_style_sheet_mime = None
        if uploaded_style_sheet is not None:
            style_filename = secure_filename(uploaded_style_sheet.filename)
            extension = style_filename.split('.')[-1]
            style_new_filename = "upload-{}.{}".format(
                scene_name, extension
            )
            path = Path(f"{self.proj_base_path}/scene_stylesheet")
            path.mkdir(parents=True, exist_ok=True)
            uploaded_style_sheet.save(os.path.join(path, style_new_filename))
            uploaded_style_sheet_mime = uploaded_style_sheet.content_type
            # Parse the stylesheet, replace color
            parser = cssutils.parseFile(os.path.join(path, style_new_filename))
            for rule in parser.cssRules:
                try:
                    rule.selectorText = f"#{scene_name} {rule.selectorText}"
                except AttributeError as e:
                    pass  # Ignore error if the rule does not have background
            # Write to a new file
            with open(os.path.join(path, style_new_filename), 'wb') as f:
                f.write(parser.cssText)
        ######################################################################
        scene = Scenes()
        scene.create_scene(args, scene_name, new_filename, uploaded_file.content_type, style_new_filename,
                           uploaded_style_sheet_mime, self.proj_base_path)
        return uploaded_file.filename

    def check_scene_exist(self, scene_name):
        file_path = os.path.join(self.proj_base_path, f"{scene_name}.json")
        return (lambda x: True if os.path.exists(x) else False)(file_path)
