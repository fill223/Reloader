#Creating crypted password file from default password.ini


#Creating secret key to MyKey.key
def create_key():
    from cryptography.fernet import Fernet

    key=Fernet.generate_key()

    with open('MyKey.key', 'wb') as file:
        file.write(key)

#Read key from file
key=''
with open('MyKey.key', 'rb') as file:
    key=file.read()


#Read data from file
data=''
with open('password.ini', 'rb') as file:
    data=file.read()

#Encrypt data
from cryptography.fernet import Fernet
f=Fernet(key)
encrypted=f.encrypt(data)


with open('crypted_password.ini', 'wb') as file:
    file.write(encrypted)