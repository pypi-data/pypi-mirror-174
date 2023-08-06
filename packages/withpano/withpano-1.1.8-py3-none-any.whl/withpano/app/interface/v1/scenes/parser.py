from werkzeug.datastructures import FileStorage

from withpano.app.interface import api

upload_parser = api.parser()
upload_parser.add_argument('name', location='form', help="Name cannot be blank!", required=True)
upload_parser.add_argument('face_size', location='form', help="FaceSize cannot be blank!", required=True)
upload_parser.add_argument('type', location='form', help="FaceSize cannot be blank!", required=True)
upload_parser.add_argument('project', location='form', help="FaceSize cannot be blank!", required=True)
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)
upload_parser.add_argument('stylesheet', location='files', type=FileStorage, required=False)
