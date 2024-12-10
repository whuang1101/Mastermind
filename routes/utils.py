import bcrypt
def hash_password(password):
    encrypted_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')
    return encrypted_password

