from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import serialization
import base64
from cryptography.hazmat.primitives.serialization import load_der_private_key

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.setUserKeys()

    def setUserKeys(self):
        # Generate a new RSA key pair
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        # Create a new self-signed certificate
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, self.name),
            x509.NameAttribute(NameOID.EMAIL_ADDRESS, self.email),
        ])
        now = datetime.utcnow()
        self.certificate = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            now
        ).not_valid_after(
            now + timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([x509.DNSName('example.com')]),
            critical=False,
        ).sign(key, hashes.SHA256())

        # Extract the private key and public key as variables
        private_key_bytes = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        # private_key = serialization.load_pem_private_key(
        #     private_key_bytes,
        #     password=None
        # )

        # Write the email and private key to a local text file as a tuple
        #with open('keys.txt', 'a') as f:
        with open(f'{self.email}_key', 'a') as f:

            # Might have to fix as will probably add multiple private keys
            # file_contents = f.read()
            # if len(file_contents) > 0:
            #     f.truncate(0)
            
            #f.write(f'({self.email}\n{private_key_bytes.decode("utf-8")})\n')
            # f.write(f'({self.email}\n{private_key_bytes})\n')
            f.write(private_key_bytes.decode())

    
def getPrivateKey(userEmail):
    with open(f'{userEmail}_key', "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )

    return private_key
