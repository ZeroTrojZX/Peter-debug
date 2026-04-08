import os
import base64
import hashlib

# Function to generate a secure random key

def generate_secure_key(length=32):
    return base64.urlsafe_b64encode(os.urandom(length)).decode('utf-8')

# Function to validate a given key against a predefined pattern or length

def validate_key(key, length=32):
    # Checks if key is the expected length
    if len(key) != length:
        return False
    # Additional validation can be implemented here (e.g., regex patterns)
    return True