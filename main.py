from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from user import User
from file import uploadFile, encryptFile, downloadFile, decryptFile
from management import addUser, removeUser, getPrivateKey, getPublicKey, getClient, isMember, getUsers, getUser

client = getClient()
folderId = '202433136302'
folder = client.folder(folder_id=folderId).get()
userEmail = ''
users = getUsers(folder)

applicationRunning = True
print("\nHello\n")
while applicationRunning:
    loggedIn = False
    while not loggedIn:
        print("Please enter your username and password, or enter 'quit' to exit the application.\n")
        choice = input("Enter your email or enter 'quit': ")
        if(choice.lower() == 'quit' or choice.lower() == 'exit'):
            applicationRunning = False
            break
        else:
            userEmail = choice
            if isMember(choice, folder):
                loggedIn = True
            else:
                print(f"Error: The user {userEmail} does not have access to the folder {folderId}\n")

    while userEmail:
        print("\nPlease select one of the following options by choosing the corresponding number.")
        print(f"1. Add a user to the shared Box folder {folderId}")
        print(f"2. Remove a user from the shared Box folder {folderId}")
        print("3. Encrypt a file")
        print("4. Decrypt a file")
        print("5. Log out")
        print("6. Exit the application\n")

        choice = int(input("Enter your number here: "))
        if choice < 1 or choice > 6:
            print("Error: You must enter an integer in the range 1-6.")
        else:
            if choice == 1:
                print(f"\nPlease nter the email of the user you'd like to add to the folder {folderId}\n")
                newUserEmail = input("User's Email: ")
                if(isMember(newUserEmail, folder)):
                    print(f"Error: The user {newUserEmail} already has access to the folder {folderId}\n")
                else:
                    addUser(newUserEmail)
            elif choice == 2:
                print(f"\nPlease nter the email of the user you'd like to remove from the folder {folderId}\n")
                newUserEmail = input("User's Email: ")
                if(not isMember(newUserEmail, folder)):
                    print(f"Error: The user {newUserEmail} does not have access to the folder {folderId}\n")
                else:
                    removeUser(newUserEmail)
            elif choice == 3:
                fileName = input("Please enter the name of the file you'd like to encrypt: \n")
                recipientEmail = ''
                while(not isMember(recipientEmail, folder)):
                    recipientEmail = input("Please enter the email of the user you'd like to send the encryption to: \n")
                    if not isMember(recipientEmail, folder):
                        print(f"Error: The user {recipientEmail} does not have access to the folder {folderId}\n")
                recipient = getUser(recipientEmail, users)
                encryptFile(fileName, getPublicKey(recipient))
            elif choice == 4:
                fileName = input("Please enter the name of the file you'd like to encrypt: ")
                downloadFile(fileName)
                decryptFile(f'encrypted_{fileName}', getPrivateKey(userEmail))
            elif choice == 5:
                userEmail = False
            else:
                userEmail = False
                applicationRunning = False
