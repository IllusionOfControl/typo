from passlib.hash import bcrypt_sha256


def hash_password(plaintext):
    return bcrypt_sha256.hash(str(plaintext))


def verify_password(password_hash, plaintext):
    return bcrypt_sha256.verify(password_hash, plaintext)
