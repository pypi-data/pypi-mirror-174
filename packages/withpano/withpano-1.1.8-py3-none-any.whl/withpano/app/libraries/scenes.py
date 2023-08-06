import json
import os


class Scenes:
    def __init__(self):
        self.scene_path = "./scenes"
        self.create_path()

    def create_path(self):
        if not os.path.exists(self.scene_path):
            # if the demo_folder2 directory is
            # not present then create it.
            os.makedirs(self.scene_path)

    def check_scene_exist(self, filepath, scene):
        file_path = os.path.join(filepath, f"{scene}.json")
        return (lambda x: True if os.path.exists(x) else False)(file_path)

    def create_scene(self, args, scene_name, file_name, mime_type, stylesheet, stylesheet_mime, filepath):
        # Data to be written
        dictionary = {
            "id": scene_name,
            "type": args['type'],
            "name": args['name'].upper(),
            "scene_image": file_name,
            "mime_type": mime_type,
            "stylesheet": stylesheet,
            "stylesheet_mime_type": stylesheet_mime,
            "levels": [
                {
                    "tileSize": 256,
                    "size": 256,
                    "fallbackOnly": True
                },
                {
                    "tileSize": 512,
                    "size": 512
                },
                {
                    "tileSize": 512,
                    "size": 1024
                },
                {
                    "tileSize": 512,
                    "size": 2048
                },
                {
                    "tileSize": 512,
                    "size": 4096
                }
            ],
            "faceSize": args['face_size'],
            "initialViewParameters": {
                "pitch": 0,
                "yaw": 0,
                "fov": 1.5707963267948966
            }
        }

        # Serializing json
        json_object = json.dumps(dictionary, indent=4)

        # Writing to sample.json
        with open(os.path.join(filepath, f"{scene_name}.json"), "w") as outfile:
            outfile.write(json_object)
        outfile.close()

    def save_scene(self, scene, filepath, data):
        print(scene, filepath, data)
        if self.check_scene_exist(filepath, scene):
            with open(os.path.join(filepath, f"{scene}.json"), "r") as outfile:
                scene_data = json.loads(outfile.read())
                print(scene_data)
                if 'hotspot' in scene_data:
                    del scene_data['hotspot']
                scene_data['hotspot'] = data
            with open(os.path.join(filepath, f"{scene}.json"), "w") as outfile:
                json_object = json.dumps(scene_data, indent=4)
                print(json_object)
                outfile.write(json_object)
            outfile.close()
            return json.loads(json_object)
        else:
            return None

    def get_scene(self, scene, filepath):
        if self.check_scene_exist(filepath, scene):
            with open(os.path.join(filepath, f"{scene}.json"), "r") as outfile:
                return json.loads(outfile.read())
        else:
            return {
                "id": scene,
                "scene_image": "default",
                "type": "360View",
                "name": "Default",
                "mime_type": "image/jpeg",
                "levels": [
                    {
                        "tileSize": 256,
                        "size": 256,
                        "fallbackOnly": True
                    },
                    {
                        "tileSize": 512,
                        "size": 512
                    },
                    {
                        "tileSize": 512,
                        "size": 1024
                    },
                    {
                        "tileSize": 512,
                        "size": 2048
                    },
                    {
                        "tileSize": 512,
                        "size": 4096
                    }
                ],
                "faceSize": 4096,
                "initialViewParameters": {
                    "pitch": 0,
                    "yaw": 0,
                    "fov": 1.5707963267948966
                }
            }
