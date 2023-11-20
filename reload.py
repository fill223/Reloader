import os

def reload_pc():
    # Use the appropriate system command to reload the PC based on the platform
    if os.name == 'nt':  # For Windows
        os.system('shutdown /r /f /t 0')
        print("System reload succesfully")
    else:
        print("Reloading the PC is not supported on this platform.")

def cmd_pc(exec):
    # Use the appropriate system command to reload the PC based on the platform
    if os.name == 'nt':  # For Windows
        os.system(exec)
        print("Command exec succesfully")
    else:
        print("Reloading the PC is not supported on this platform.")

