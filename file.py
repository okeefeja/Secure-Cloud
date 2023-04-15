import boxsdk
from boxsdk import OAuth2
from boxsdk import Client
from urllib.parse import urlparse, parse_qs
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def encryptFile(fileName, sharedFolder, public_key):
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

    sharedFolder.upload(f'cipher_{fileName}')

    print(f"\nSuccessfully uploaded the encryption of {fileName} to Box")


def downloadFile(fileName, sharedFolder, client):
    file_list = sharedFolder.get_items()
    file_id = None
    for item in file_list:
        if isinstance(item, boxsdk.object.file.File) and item.name == fileName:
            file_id = item.id
            break

    # Download the file
    if file_id:
        file_content = client.file(file_id).content()
        with open(f'encrypted_{fileName}', 'wb') as f:
            f.write(file_content)
            print(f"\nDownloaded {fileName}")
    else:
        print(f"\nFile {fileName} not found in the shared folder.")


def decryptFile(fileName, private_key):
    with open(fileName, "rb") as data_file:
        encrypted_data = data_file.read()

    try:
        # Decrypt data
        decrypted_data = private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except ValueError:
        print(f"\nError: User's private key does not match the public key used for the encryption of {fileName}\n")
        return
    
    # Save the decrypted file to disk
    with open(f'decrypted_{fileName}', 'wb') as f:
        f.write(decrypted_data)
    
    print(f"\nSuccessfully decrypted the file {fileName}")
