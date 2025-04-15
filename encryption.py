import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import cv2
import numpy as np

KEY_FILE = "aes_key.bin"

def load_or_create_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    else:
        new_key = get_random_bytes(32)
        with open(KEY_FILE, "wb") as f:
            f.write(new_key)
        return new_key

key = load_or_create_key()

def pad(data):
    pad_len = AES.block_size - (len(data) % AES.block_size)     # 
    return data + bytes([pad_len] * pad_len)                    #

def unpad(data):
    pad_len = data[-1]                          #
    return data[:-pad_len]                      #

def encrypt_image_aes(image_path, key):
    with open(image_path, 'rb') as f:                     # open the image file in binary mode
        image_data = f.read()                             # read the image data
    padded_data = pad(image_data)                         # pad the image data
    iv = get_random_bytes(AES.block_size)                 # generate a random initialization vector
    cipher = AES.new(key, AES.MODE_CBC, iv)               # create a new AES cipher in CBC mode with its initialization vector
    ciphertext = cipher.encrypt(padded_data)              # encrypt the padded data
    return iv + ciphertext                                # prepend the IV to the ciphertext and return it

def decrypt_image_aes(encrypted_data, key):
    iv = encrypted_data[:AES.block_size]                  # extract the IV from the beginning of the encrypted data
    ciphertext = encrypted_data[AES.block_size:]          # extract the ciphertext
    cipher = AES.new(key, AES.MODE_CBC, iv)               # recreate full cipher object with the same key and IV
    padded_data = cipher.decrypt(ciphertext)              # decrypt the ciphertext
    data = unpad(padded_data)                             # remove padding from decrypted data
    nparr = np.frombuffer(data, np.uint8)                 # convert the decrypted data to a numpy array
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)           # decode the image from the numpy array
    return img                                            # return the image so it can be matched against provided fingerprint

def encrypt_text_aes(plaintext, key):
    data = plaintext.encode('utf-8')                      # convert the plaintext to bytes
    padded_data = pad(data)                               # pad the data
    iv = get_random_bytes(AES.block_size)                 # generate a random IV
    cipher = AES.new(key, AES.MODE_CBC, iv)               # create a new AES cipher in CBC mode with the IV
    ciphertext = cipher.encrypt(padded_data)              # encrypt the padded data
    return iv + ciphertext

def decrypt_text_aes(encrypted_data, key):
    iv = encrypted_data[:AES.block_size]                  # extracts the IV from the beginning of the encrypted data
    ciphertext = encrypted_data[AES.block_size:]          # extracts the ciphertext
    cipher = AES.new(key, AES.MODE_CBC, iv)               # creates a cipher object with the same key and IV
    padded_data = cipher.decrypt(ciphertext)              # decrypts the ciphertext
    plaintext = unpad(padded_data).decode('utf-8')        # removes padding and decodes to a string
    return plaintext