from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from user import User
from file import uploadFile, encryptFile, downloadFile, decryptFile
from management import addUser, removeUser, getPrivateKey, getClient, isMember

#userEmail = 'okeefeja@tcd.ie'
client = getClient()
folderId = '202433136302'
#folder = client.folder(folderId)
folder = client.folder(folder_id=folderId).get()
userEmail = ''
applicationRunning = True

print("\nHello")
while applicationRunning:
    loggedIn = False
    while not loggedIn:
        print("Please enter your username and password, or enter 'quit' to exit the application.\n")
        choice = input("Enter your email or enter 'quit': ")
        if(choice.lower() == 'quit' or choice.lower() == 'exit'):
            applicationRunning = False
            break
        else:
            validEmail = False
            collaborators = folder.get_collaborations()
            # Check if the user with the given email is a collaborator
            userEmail = choice
            for collaborator in collaborators:
                if collaborator.accessible_by['login'] == userEmail:
                    validEmail = True
            if not validEmail:
                # Check if the user owns the folder if they are not a collaborator
                owner_email = folder.owned_by['login']
                if(userEmail == owner_email):
                    loggedIn  = True
                else:
                    print(f"Error: The user {userEmail} does not have access to the folder {folderId}\n")
            else:
                loggedIn = True

    if applicationRunning:
        print(f"\nHello {userEmail}\n")
    while userEmail:
        print("Please select one of the following options by choosing the corresponding number.")
        print(f"1. Add a user to the shared Box folder {folderId}")
        print(f"2. Remove a user from the shared Box folder {folderId}")
        print("3. Encrypt a file")
        print("4. Decrypt a file")
        print("5. Log out")
        print("6. Exit the application\n")

        choice = int(input("Enter your number here: "))
        if choice <= 0 or choice > 6:
            print("Error: You must enter an integer in the range 1-6.")
        else:
            if choice == 1:
                print(f"\nPlease nter the email of the user you'd like to add to the folder {folderId}\n")
                newUserEmail = input("User's Email: ")
                if(isMember(newUserEmail, folder)):
                    print(f"Error: The user {newUserEmail} already has access to the folder {folderId}\n")
                else:
                    addUser(newUserEmail)
                    print(f"Successfully added {newUserEmail} to the folder {folderId}\n")
            elif choice == 5:
                userEmail = False
            else:
                userEmail = False
                applicationRunning = False
