import bcrypt
import _cffi_backend
import os
from Cryptodome.Cipher import AES
import base64



def get_iv():
    return(os.urandom(16))

#Funcations for encrypting and decrypting the user passwords with a Key Password and then using Base64, to give it a better "hashed look"
def encrypt_password(key, string, IV):
    key = key.encode()
    string = string.encode()
    obj = AES.new(key, AES.MODE_CFB, IV)
    password = obj.encrypt(string)
    return(base64.urlsafe_b64encode(password))

def decrypt_password(key, string, IV):
    key = key.encode()
    string = base64.urlsafe_b64decode(string)

    IV = base64.urlsafe_b64decode(IV)

    obj2 = AES.new(key, AES.MODE_CFB, IV)
    decrtypted_password = obj2.decrypt(string)
    return(decrtypted_password)
