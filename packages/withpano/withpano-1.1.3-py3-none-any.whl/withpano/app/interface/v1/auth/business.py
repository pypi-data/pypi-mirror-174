import json
import logging
import os
from pathlib import Path

log = logging.getLogger('console')


class UserCreate:
    def __init__(self, username):
        self.username = username
        self.proj_base_path = f"./project_data/{username}"
        self.user_enc_salt_file = "./project_data/_salt.key.withpano"

    def create_user_path(self, user_data, salt):
        try:
            path = Path(f'{self.proj_base_path}')
            path.mkdir(parents=True, exist_ok=False)
            init_file = os.path.join(path, "user_data.json")
            try:
                with open(init_file, 'w') as fp:
                    fp.write(json.dumps(user_data))
                fp.close()
                if not os.path.exists(self.user_enc_salt_file):
                    with open(self.user_enc_salt_file, 'w+') as salt_file:
                        json.dump([{user_data['username']: salt}], salt_file)
                    salt_file.close()
                else:
                    with open(self.user_enc_salt_file, 'r') as sf:
                        data = json.load(sf)
                        data.append({user_data['username']: salt})
                    with open(self.user_enc_salt_file, "w") as file:
                        json.dump(data, file)
                return True, str(path)
            except Exception as e:
                log.exception(e)
                os.remove(init_file)
                os.rmdir(self.proj_base_path)
                return False, "Unable to Create"
        except FileExistsError as e:
            log.exception(e.filename)
            return False, "Record exist"

    def validate_user(self):
        try:
            path = Path(f'{self.proj_base_path}')
            init_file = os.path.join(path, "user_data.json")
            with open(self.user_enc_salt_file, 'r') as sf:
                data = json.load(sf)
            salt_key = next((sub for sub in data for key, item in sub.items() if key == self.username), None)
            with open(init_file, 'r') as fp:
                user_data = json.loads(fp.read())
            fp.close()
            return user_data, salt_key[self.username]
        except FileNotFoundError as e:
            log.exception(e.filename)
            return None
