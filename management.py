from boxsdk import OAuth2
from boxsdk import Client
from urllib.parse import urlparse, parse_qs
from boxsdk.object.collaboration import CollaborationRole
from cryptography.hazmat.primitives import serialization
from user import User

def addUser(userEmail, sharedFolder):
    collaboration = sharedFolder.add_collaborator(
        userEmail,
        CollaborationRole.EDITOR,
    )

    collaboration.update_info(role=CollaborationRole.EDITOR)
    print(f"\nAdded the user {userEmail} to the shared Box folder 202433136302")


def removeUser(userEmail, sharedFolder):
    collaborations = sharedFolder.get_collaborations()
    for collab in collaborations:
        if collab.accessible_by['login'] == userEmail:
            collab.delete()
            print(f"\nCollaborator {collab.accessible_by['login']} has been removed from the shared folder.")
            break


def getPrivateKey(userEmail):
    with open(f'{userEmail}_key', "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )

    return private_key

def getPublicKey(user):
    public_key = user.certificate.public_key()
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    public_key = serialization.load_pem_public_key(
        public_key_pem
    )
    return public_key


def getClient():
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

    oauth.authenticate(auth_code)

    client = Client(oauth)

    #shared_folder = client.folder('202433136302')

    return client


def isMember(userEmail, folder):
    collaborators = folder.get_collaborations()
    # Check if the user owns the folder
    owner_email = folder.owned_by['login']
    if(userEmail == owner_email):
        return True
    # Check if the user is a collaborator if they are not the owner
    for collaborator in collaborators:
        if collaborator.accessible_by['login'] == userEmail:
            return True
    return False


def getUsers(folder):
    users = []
    collaborators = folder.get_collaborations()
    # Append owner to list of users
    user = User(folder.owned_by['login'])
    users.append(user)
    # Append collaborators to the list of users
    for collaborator in collaborators:
        user = User(collaborator.accessible_by['login'])
        users.append(user)
    return users

def getUser(userEmail, users):
    for user in users:
        if user.email == userEmail:
            return user
    return None
