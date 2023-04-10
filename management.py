from boxsdk import OAuth2
from boxsdk import Client
from urllib.parse import urlparse, parse_qs
from boxsdk.object.collaboration import CollaborationRole

def addUser(userEmail):
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

    collaboration = shared_folder.add_collaborator(
        userEmail,
        CollaborationRole.EDITOR,
    )

    collaboration.update_info(role=CollaborationRole.EDITOR)
    print(f"Added the user {userEmail} to the shared Box folder 202433136302")

def removeUser(userEmail):
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

    collaborations = shared_folder.get_collaborations()
    for collab in collaborations:
        if collab.accessible_by['login'] == 'jcokeefe02@gmail.com':
            collab.delete()
            print(f"Collaborator {collab.accessible_by['login']} has been removed from the shared folder.")
            break
