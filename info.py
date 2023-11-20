import platform
import getpass
import socket
import ctypes
from win32gui import GetWindowText, GetForegroundWindow
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


def get_pc_info():
    # Get the username of the user who started the program
    username = getpass.getuser()

    # Get the hostname of the PC
    hostname = socket.gethostname()

    # Get the domain name of the PC
    domain_name = socket.getfqdn()

    #Get log in status
    time.sleep(5)

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
) = get_pc_info()


print(status_log_in)