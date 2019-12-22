from passlib.hash import bcrypt_sha256


def hash_password(plaintext):
    return bcrypt_sha256.hash(str(plaintext))


def verify_password(plaintext, password_hash):
    return bcrypt_sha256.verify(plaintext, password_hash)
