from cryptography.fernet import Fernet
import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import getpass
import sys

def generate_key(password):
    # Use PBKDF2 to derive a key from the password
    salt = b'salt_123'  # In production, use a random salt and store it
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def encrypt_file(filename, password):
    # Generate key from password
    key = generate_key(password)
    f = Fernet(key)
    
    # Read the file content
    with open(filename, 'rb') as file:
        file_data = file.read()
    
    # Encrypt the data
    encrypted_data = f.encrypt(file_data)
    
    # Write the encrypted data back to file
    with open(filename, 'wb') as file:
        file.write(encrypted_data)

def decrypt_file(filename, password):
    # Generate key from password
    key = generate_key(password)
    f = Fernet(key)
    
    try:
        # Read the encrypted data
        with open(filename, 'rb') as file:
            encrypted_data = file.read()
        
        # Decrypt the data
        decrypted_data = f.decrypt(encrypted_data)
        
        # Write the decrypted data back to file
        with open(filename, 'wb') as file:
            file.write(decrypted_data)
            
    except Exception as e:
        print("Incorrect password or corrupted file!")
        return False
    
    return True

def main():
    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    filename = os.path.join(desktop, 'protected.txt')
    
    # Create new file or access existing one
    if not os.path.exists(filename):
        content = input("Enter the content for your protected file: ")
        with open(filename, 'w') as file:
            file.write(content)
        
        password = getpass.getpass("Create a password for your file: ")
        encrypt_file(filename, password)
        print(f"File created and encrypted at: {filename}")
    
    else:
        password = getpass.getpass("Enter password to decrypt the file: ")
        if decrypt_file(filename, password):
            print("File decrypted! You can now open it.")
            input("Press Enter when done reading...")
            encrypt_file(filename, password)
            print("File encrypted again!")

if __name__ == "__main__":
    main()