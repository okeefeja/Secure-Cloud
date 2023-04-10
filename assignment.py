from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from user import User
from file import uploadFile, encryptFile

newUser = User("James O'Keefe", "jcokeefe02@gmail.com")

public_key = newUser.certificate.public_key()
public_key_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

public_key = serialization.load_pem_public_key(
    public_key_pem
)

encryptFile('file.txt', public_key)
