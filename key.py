from cryptography.fernet import Fernet

# Generate a proper key
key = Fernet.generate_key()
print(key)
