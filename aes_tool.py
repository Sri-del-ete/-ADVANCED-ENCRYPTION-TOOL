from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os

def encrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        data = f.read()

    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))

    with open(file_path + ".enc", 'wb') as f:
        f.write(cipher.iv + ct_bytes)

    print(f"[+] Encrypted and saved as {file_path}.enc")

def decrypt_file(enc_path, key):
    with open(enc_path, 'rb') as f:
        iv = f.read(16)
        ct = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)

    dec_path = enc_path.replace(".enc", ".dec")
    with open(dec_path, 'wb') as f:
        f.write(pt)

    print(f"[+] Decrypted and saved as {dec_path}")

def main():
    print("""
[1] Encrypt File
[2] Decrypt File
[3] Exit
""")
    choice = input("Choose an option : ")

    if choice == "1":
        path = input("Enter file path to encrypt: ")
        key = input("Enter 32-byte key (or leave empty to auto-generate): ").encode()
        if not key:
            key = get_random_bytes(32)
            print(f"Generated key (save this!): {key.hex()}")
        encrypt_file(path, key)

    elif choice == "2":
        path = input("Enter encrypted file path: ")
        key = input("Enter your 32-byte key in hex: ")
        decrypt_file(path, bytes.fromhex(key))

    elif choice == "3":
        print("Exiting. Stay encrypted.")
        exit()

    else:
        print("Invalid choice . Try again.")

if __name__ == "__main__":
    main()
