import psutil
import socket

def get_specific_ip(interface_name):
    specific_ip = None
    addrs = psutil.net_if_addrs().get(interface_name, [])
    for addr in addrs:
        if addr.family == socket.AF_INET:
            specific_ip = addr.address
            break
    return specific_ip

specific_interface = "Ethernet"  # Укажите имя интерфейса, который вы хотите считать основным
specific_ip = get_specific_ip(specific_interface)

if specific_ip:
    print(f"The specific IP address for {specific_interface} is: {specific_ip}")
else:
    print(f"No active network interfaces found for {specific_interface}.")
