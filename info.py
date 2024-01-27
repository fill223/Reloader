import platform
import getpass
import socket
import ctypes
from win32gui import GetWindowText, GetForegroundWindow
from ldap3 import Server, Connection, ALL, NTLM
import time
import psutil
import subprocess
import os

import pymysql.cursors
import configparser


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Getting pc Info
def get_uptime():
    # Get the system's platform information
    system_info = platform.uname()

    # Get system uptime based on the platform (Windows)
    if system_info.system == 'Windows':
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        uptime_ms = kernel32.GetTickCount64()
        uptime_seconds = abs(uptime_ms // 1000)
    else:
        # For other platforms, return None for now
        # You can add platform-specific implementations here
        uptime_seconds = None

    if uptime_seconds is None:
        return None

    # Convert uptime_seconds to dd:hh:mm:ss format
    minutes, seconds = divmod(int(uptime_seconds), 60)
    hours, minutes = divmod(minutes, 60)
    seconds = abs(seconds)
    minutes = abs(minutes)
    hours = abs(hours)

    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"


def get_ad_info(username):
    # Replace these values with your Active Directory server details
    ad_server = 'ldap://your_ad_server'
    ad_user = 'your_username'
    ad_password = 'your_password'

    # Construct the LDAP connection string
    server = Server(ad_server, get_info=ALL)
    connection = Connection(server, user=ad_user, password=ad_password, authentication=NTLM)

    # Try to establish the connection
    if not connection.bind():
        print(f"Failed to connect to Active Directory: {connection.last_error}")
        return None

    # Search for the user in Active Directory
    search_filter = f"(sAMAccountName={username})"
    attributes = ['cn', 'thumbnailPhoto']
    connection.search('OU=YourOrganizationalUnit,DC=your,DC=domain,DC=com', search_filter, attributes=attributes)

    # Retrieve user details including picture
    if connection.entries:
        user_cn = connection.entries[0].cn.value
        thumbnail_photo = connection.entries[0].thumbnailPhoto.value
        return user_cn, thumbnail_photo
    else:
        print(f"User {username} not found in Active Directory")
        return None

def get_data(EXTENDED_NAME_FORMAT: int):
    GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
    data = EXTENDED_NAME_FORMAT

    size = ctypes.pointer(ctypes.c_ulong(0))
    GetUserNameEx(data, None, size)

    nameBuffer = ctypes.create_unicode_buffer(size.contents.value)
    GetUserNameEx(data, nameBuffer, size)
    return nameBuffer.value


def get_pc_info():
    # Get the username of the user who started the program
    username = getpass.getuser()

    # Get the hostname of the PC
    hostname = socket.gethostname()

    # Get the domain name of the PC
    domain_name = socket.getfqdn()

    #Get log in status

    status=str(GetWindowText(GetForegroundWindow()))
    if (status.find('Windows') >=0):
        status_log_in='no'
    else:
        status_log_in = 'yes'

    # if process_name in outputstringall:
    #     status_log_in='no'
    # else:
    #     status_log_in = 'yes'

    # Get the IP address of the PC
    ip_address = socket.gethostbyname(hostname)

    # Get the system's platform information
    system_info = platform.uname()

    # Extract relevant system information
    system_name = system_info.system
    node_name = system_info.node
    release = system_info.release
    version = system_info.version
    machine = system_info.machine
    processor = system_info.processor

    # Get the system uptime
    uptime = get_uptime()


    surname=get_data(3)
    length=len(hostname)+1
    domain_name=domain_name[length:]


    return (
        username,
        hostname,
        domain_name,
        ip_address,
        system_name,
        node_name,
        release,
        version,
        machine,
        processor,
        uptime,
        status_log_in,
        surname
    )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Making variables single, possible to work with each other

(
    username,
    hostname,
    domain_name,
    ip_address,
    system_name,
    node_name,
    release,
    version,
    machine,
    processor,
    uptime,
    status_log_in,
    surname
) = get_pc_info()


#print(get_pc_info())