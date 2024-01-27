import os
import subprocess

def reload_pc():
    # Use the appropriate system command to reload the PC based on the platform
    if os.name == 'nt':  # For Windows
        os.system('shutdown /r /f /t 0')
        print("System reload succesfully")
    else:
        print("Reloading the PC is not supported on this platform.")

def shutdown_pc():
    # Use the appropriate system command to reload the PC based on the platform
    if os.name == 'nt':  # For Windows
        os.system('shutdown /s /f /t 0')
        print("System shutdown succesfully")
    else:
        print("Shutdown the PC is not supported on this platform.")

def gpupdate_pc():
    # Use the appropriate system command to reload the PC based on the platform
    if os.name == 'nt':  # For Windows
        try:
            # Use subprocess.PIPE to handle standard input
            process = subprocess.Popen(['gpupdate', '/force'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Send the response you want (e.g., 'y\n' for 'yes')
            process.communicate(input='y\n')

            # Wait for the process to finish
            process.wait()

            print("Gpupdate started successfully")
        except Exception as e:
            print(f"Error starting gpupdate: {e}")
    else:
        print("Gpupdate on the PC is not supported on this platform.")

def cmd_pc(exec):
    # Use the appropriate system command to reload the PC based on the platform
    if os.name == 'nt':  # For Windows
        os.system(exec)
        print("Command exec succesfully")
    else:
        print("Reloading the PC is not supported on this platform.")

