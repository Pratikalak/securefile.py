import datetime
import base64
import os

def ceaser_cipher(plaintext, term, total_chars):
    print("Total characters in the file:", total_chars)
    ciphertext = ""
    for i, char in enumerate(plaintext):
        shift = term[i % len(term)]
        if char.isalpha():
            if char.isupper():
                shift_char = chr((ord(char) + shift - 65) % 26 + 65)
                ciphertext += shift_char
            else:
                shift_char = chr((ord(char) + shift - 97) % 26 + 97)
                ciphertext += shift_char
        elif char.isdigit():
            shift_char = chr((ord(char) + shift - 48) % 10 + 48)
            ciphertext += shift_char
        else:
            ciphertext += char
    return base64.b64encode(ciphertext.encode()).decode()

def get_pin():
    pin = input("Enter the pin number (at least 4 digits, not more than 8 digits): ")
    while len(pin) < 4 or len(pin) > 8:
        if len(pin) < 4:
            print("Pin number should be at least 4 digits.")
        else:
            print("Pin number should not be more than 8 digits.")
        pin = input("Enter the pin number (at least 4 digits, not more than 8 digits): ")
    return int(pin)

def read_file(filename):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, filename)
        with open(file_path, "r") as f:
            plaintext = f.read()
        return plaintext
    except FileNotFoundError:
        print(f"File {filename} not found.")
        log_event(f"File {filename} was not found.")
        return None

def write_file(filename, content):
    with open(filename, "w") as f:
        f.write(content)

def log_event(event):
    with open("log.txt", "a") as f:
        f.write(f"{datetime.datetime.now()}: {event}\n")

def encrypt_file():
    filename = input("Enter the file name: ")
    plaintext = read_file(filename)
    if plaintext is None:
        return
    
    total_chars = len(plaintext)
    backup_filename = f"{filename}.{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.backup"
    write_file(backup_filename, plaintext)
    log_event(f"Backed up file {filename} to {backup_filename}")

    a = get_pin()
    term = []
    for n in range(0, total_chars):
        if plaintext[n].isalpha():
            t = ((((n**5 + n**3 + a*n**2 + a*n) * (n**7 + n**5 + a*n**3 + a*n**2 + 2*a*n + a)) % 100000 - 50000) // 1000 + 25) % 26 - 13
        else:
            t = ((((n**5 + n**3 + a*n**2 + a*n) * (n**7 + n**5 + a*n**3 + n**2 + 2*a*n + a)) % 100000 - 50000) // 1000 + 10) % 10 - 5
        term.append(t)

    ciphertext = ceaser_cipher(plaintext, term, total_chars)
    write_file(filename, ciphertext)
    log_event(f"Encrypted file {filename}")
    print("File encrypted successfully.")

if __name__ == "__main__":
    encrypt_file()
