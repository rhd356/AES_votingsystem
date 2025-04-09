from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import cv2
import numpy as np

key = get_random_bytes(32)

def pad(data):
    pad_len = AES.block_size - (len(data) % AES.block_size)
    return data + bytes([pad_len] * pad_len)

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

def encrypt_image_aes(image_path, key):
    with open(image_path, 'rb') as f:
        image_data = f.read()
    padded_data = pad(image_data)
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(padded_data)
    return iv + ciphertext

def decrypt_image_aes(encrypted_data, key):
    iv = encrypted_data[:AES.block_size]
    ciphertext = encrypted_data[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = cipher.decrypt(ciphertext)
    data = unpad(padded_data)
    nparr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def encrypt_text_aes(plaintext, key):
    data = plaintext.encode('utf-8')
    padded_data = pad(data)
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(padded_data)
    return iv + ciphertext

def decrypt_text_aes(encrypted_data, key):
    iv = encrypted_data[:AES.block_size]
    ciphertext = encrypted_data[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = cipher.decrypt(ciphertext)
    plaintext = unpad(padded_data).decode('utf-8')
    return plaintext