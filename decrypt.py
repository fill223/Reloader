key=''
with open('MyKey.key', 'rb') as file:
    key=file.read()


#Read data from file
decrypted_data=''
with open('crypted_password.ini', 'rb') as file:
    decrypted_data=file.read()

#Decrypt data
from cryptography.fernet import Fernet
f=Fernet(key)
decrypted=f.decrypt(decrypted_data)


password=decrypted.decode()

print(password)