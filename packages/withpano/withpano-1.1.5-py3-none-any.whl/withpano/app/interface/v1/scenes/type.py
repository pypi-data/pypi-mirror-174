ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf', 'xls', 'xlsx', 'csv'}
ALLOWED_STYLESHEET_EXTENSIONS = {'css'}


class FileValidation:

    def allowed_file(file):
        filename = file.filename
        return filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def allowed_stylesheet_file(file):
        if file is not None:
            filename = file.filename
            validation = filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_STYLESHEET_EXTENSIONS
            if validation:
                return validation
            else:
                raise "File not supported"
        else:
            return True
