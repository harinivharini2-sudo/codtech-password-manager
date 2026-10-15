
from cryptography.fernet import Fernet
import os
import json

KEY_FILE = "secret.key"
DATA_FILE = "passwords.json"

# Load or create the encryption key
if os.path.exists(KEY_FILE) and os.path.getsize(KEY_FILE) > 0:
    with open(KEY_FILE, "rb") as file:
        key = file.read()
else:
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as file:
        file.write(key)

fernet = Fernet(key)


def load_passwords():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}


def save_passwords(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


passwords = load_passwords()

print("\n🔐 PASSWORD MANAGER")
print("1. Save a password")
print("2. View a saved password")
print("3. Exit")

choice = input("Enter your choice: ")

if choice == "1":
    website = input("Enter website/app name: ")
    username = input("Enter username: ")
    password = input("Enter a test password: ")

    encrypted = fernet.encrypt(password.encode()).decode()

    passwords[website] = {
        "username": username,
        "password": encrypted
    }

    save_passwords(passwords)
    print("Password saved in encrypted form!")

elif choice == "2":
    website = input("Enter website/app name: ")

    if website in passwords:
        print("Username:", passwords[website]["username"])
        encrypted = passwords[website]["password"]
        decrypted = fernet.decrypt(encrypted.encode()).decode()
        print("Password:", decrypted)
    else:
        print("No saved entry found for that name.")

elif choice == "3":
    print("Goodbye!")

else:
    print("Invalid choice.")
