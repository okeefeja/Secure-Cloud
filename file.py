from boxsdk import OAuth2
from boxsdk import Client
from urllib.parse import urlparse, parse_qs
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def uploadFile(fileName):
    oauth = OAuth2(
        client_id='pu0jbhsntz9p4s4uimbppue1tw4pengw',
        client_secret='fSwjHzheuKqV5qU2kap4Z70Fu5qCnhXX',
    )

    auth_url, csrf_token = oauth.get_authorization_url('https://app.box.com/box/callback')

    # Redirect the user to the auth_url
    print(f'Please visit the following URL to authorize your application: {auth_url}')

    # Get the redirect URL that the user was redirected to after authorizing your application
    redirect_url = input('Paste the redirect URL here: ')

    # Parse the redirect URL to extract the authorization code
    url_parts = urlparse(redirect_url)
    query_params = parse_qs(url_parts.query)
    auth_code = query_params['code'][0] 

    access_token, refresh_token = oauth.authenticate(auth_code)

    client = Client(oauth)

    shared_folder = client.folder('202433136302')

    uploaded_file = shared_folder.upload(fileName)

def encryptFile(fileName, public_key):
    # Open the file to be encrypted
    with open(fileName, 'rb') as f:
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
    with open(f'cipher_{fileName}', 'wb') as f:
        f.write(ciphertext)

    uploadFile(f'cipher_{fileName}')

    print(f"Successfully uploaded the encryption of {fileName} to Box")
