import datetime
import base64
import os

def ceaser_cipher(ciphertext, term, total_chars):
    print("Total characters in the file:", total_chars)
    plaintext = ""
    for i, char in enumerate(ciphertext):
        shift = term[i % len(term)]
        if char.isalpha():
            if char.isupper():
                shift_char = chr((ord(char) - shift - 65 + 26) % 26 + 65)
                plaintext += shift_char
            else:
                shift_char = chr((ord(char) - shift - 97 + 26) % 26 + 97)
                plaintext += shift_char
        elif char.isdigit():
            shift_char = chr((ord(char) - shift - 48 + 10) % 10 + 48)
            plaintext += shift_char
        else:
            plaintext += char
    return plaintext

def read_file(filename):
    try:
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct full file path
        file_path = os.path.join(current_dir, filename)
        
        print(f"Attempting to read file from: {file_path}")  # Debug print
        
        with open(file_path, "r") as f:
            ciphertext = f.read()
        return ciphertext
    except FileNotFoundError:
        print(f"File {filename} not found at {file_path}")
        log_event(f"File {filename} was not found at {file_path}")
        return None

def write_file(filename, content):
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct full file path
    file_path = os.path.join(current_dir, filename)
    
    with open(file_path, "w") as f:
        f.write(content)

def log_event(event):
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct log file path
    log_path = os.path.join(current_dir, "log.txt")
    
    with open(log_path, "a") as f:
        f.write(f"{datetime.datetime.now()}: {event}\n")

def decrypt_file():
    filename = input("Enter the file name: ")
    ciphertext = read_file(filename)
    if ciphertext is None:
        return
    
    try:
        ciphertext = base64.b64decode(ciphertext.encode()).decode()
    except Exception as e:
        print(f"Error: Invalid base64 encoding in file: {str(e)}")
        log_event(f"Failed to decode base64 in file {filename}: {str(e)}")
        return

    total_chars = len(ciphertext)
    
    try:
        print("Enter the same PIN used for encryption")
        a = int(input("Enter the pin number: "))
    except ValueError:
        print("Error: Please enter a valid number for pin")
        log_event("Invalid pin number entered")
        return

    term = []
    for n in range(0, total_chars):
        if ciphertext[n].isalpha():
            t = ((((n**5 + n**3 + a*n**2 + a*n) * (n**7 + n**5 + a*n**3 + a*n**2 + 2*a*n + a)) % 100000 - 50000) // 1000 + 25) % 26 - 13
        else:
            t = ((((n**5 + n**3 + a*n**2 + a*n) * (n**7 + n**5 + a*n**3 + n**2 + 2*a*n + a)) % 100000 - 50000) // 1000 + 10) % 10 - 5
        term.append(t)

    try:
        plaintext = ceaser_cipher(ciphertext, term, total_chars)
        write_file(filename, plaintext)
        log_event(f"Decrypted file {filename}")
        print("File decrypted successfully.")
    except Exception as e:
        print(f"Error during decryption: {str(e)}")
        log_event(f"Decryption failed for file {filename}: {str(e)}")

if __name__ == "__main__":
    decrypt_file()
