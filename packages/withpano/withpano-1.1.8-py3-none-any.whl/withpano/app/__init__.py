import logging
import os
from pathlib import Path
from secrets import token_urlsafe
from cryptography.fernet import Fernet
from flask_caching import Cache
from termcolor import colored

log = logging.getLogger('console')

# Instantiation of cache class
cache = Cache(config={
    "DEBUG": True,  # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
})


# generate a key for encryption and decryption
# You can use fernet to generate
# the key or use random key generator
# here I'm using fernet to generate key

def create_hash(token):
    key = Fernet.generate_key()
    # Instance the Fernet class with the key
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(token.encode()).decode()
    return encrypted_data, key


def decipher_hash(salt, token):
    # Instance the Fernet class with the key
    fernet = Fernet(salt.encode())
    decrypted_data = fernet.decrypt(token.encode()).decode()
    return decrypted_data


def create_auth_token():
    path = Path(f'./project_data/')
    path.mkdir(parents=True, exist_ok=True)
    init_file = os.path.join(path, "_secret.withpano")
    token = token_urlsafe(16)
    with open(init_file, 'w') as fp:
        fp.write(token)
    fp.close()
    print(colored("#############################################################", 'green', attrs=['reverse', 'blink']))
    log.info(colored(f"TOKEN_FOR_ACCESS: {token}", "green"))
    print(colored("#############################################################", 'green', attrs=['reverse', 'blink']))
    return "Success"
