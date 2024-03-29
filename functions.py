import hashlib

def hash_password(password):
    password_bytes = password.encode('utf-8')
    hash_object = hashlib.sha256()
    hash_object.update(password_bytes)
    hashed_password = hash_object.hexdigest()
    return hashed_password

def hashFunction(password):
    password = password
    hashed_password = hash_password(password)
    return hashed_password