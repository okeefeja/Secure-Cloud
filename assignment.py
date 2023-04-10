from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from user import User
from file import uploadFile

newUser = User("James O'Keefe", "jcokeefe02@gmail.com")

public_key = newUser.certificate.public_key()
public_key_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

public_key = serialization.load_pem_public_key(
    public_key_pem
)

# Open the file to be encrypted
with open('file.txt', 'rb') as f:
    plaintext = f.read()

# Encrypt the file using the RSA public key
ciphertext = public_key.encrypt(
    plaintext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Save the encrypted file to disk
with open('cipherFile.txt', 'wb') as f:
    f.write(ciphertext)

uploadFile('cipherFile.txt')

print("Successfully uploaded the encryption of 'file.txt' to Box")
