import hashlib

def main():
    """
    This script prompts the user for an input string, calculates the SHA256 hash
    of the input, and prints the resulting hash.
    """
    user_input = input("Enter the data to hash: ")
    
    # Encode the input string to bytes, as hashlib works with bytes
    encoded_input = user_input.encode('utf-8')
    
    # Create a sha256 hash object
    hasher = hashlib.sha256()
    
    # Update the hash object with the bytes-like object
    hasher.update(encoded_input)
    
    # Get the hexadecimal representation of the hash
    hex_digest = hasher.hexdigest()
    
    print(f"SHA256 Hash: {hex_digest}")

if __name__ == "__main__":
    main() 