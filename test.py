import pymysql.cursors
import configparser
import datetime
import time
import base64
import psutil
import ctypes



#____________________________________________________________________________________
#Connect to SQL
def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def encrypt_password(password):
    encrypted_password = base64.b64encode(password.encode()).decode()
    return encrypted_password



#Testing log-on log-off
def login_test():
    users_logged_in = psutil.users()
    status_log_in = "yes" if users_logged_in else "no"

    print(psutil.users())

# def is_screen_locked():
#     # Check if the screen is locked
#     result = ctypes.windll.user32.GetForegroundWindow() == 0
#
#     # Return True if the screen is locked, False otherwise
#     return result == 1
#
# # Example usage
# if is_screen_locked():
#     print("The screen is locked")
# else:
#     print("The screen is not locked")
# time.sleep(10)
# print(ctypes.windll.user32.GetForegroundWindow())

import ctypes
import time
user32 = ctypes.windll.User32
time.sleep(5)
#
#print(user32.GetForegroundWindow())
#
if (user32.GetForegroundWindow() % 10 == 0): print('Locked')
# 10553666 - return code for unlocked workstation1
# 0 - return code for locked workstation1
#
# 132782 - return code for unlocked workstation2
# 67370 -  return code for locked workstation2
#
# 3216806 - return code for unlocked workstation3
# 1901390 - return code for locked workstation3
#
# 197944 - return code for unlocked workstation4
# 0 -  return code for locked workstation4
#
else: print('Unlocked')