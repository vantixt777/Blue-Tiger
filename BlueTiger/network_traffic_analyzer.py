import os
import psutil
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

blue = Fore.BLUE
white = Fore.WHITE
red = Fore.RED
green = Fore.GREEN

def banner():
    return f"""{blue}
⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀
⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀
⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀
⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀
⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠐
⠀⣀⣠⣿⣷⣴⣶⣶⣶⣶⣿⣿⣿⣿⣶⣶⣶⣶⣶⣿⣧⣀⣀⠀
⢰⣿⡿⠛⠛⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠛⠛⢿⣿⡆
⣸⣿⠁⠀⣀⡀⠀⢀⡀⠀⢀⡀⠀⠀⠀⠀⠀⠀⢀⣀⠀⠈⣿⣇
⢿⣿⠀⠀⠻⠏⠀⠻⠟⠀⠻⠟⠀⠀⠀⠀⠀⠀⠻⠟⠀⢀⣿⡟
⢸⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠅⣰⣿⡇
⠈⠻⠿⣿⣿⣶⣶⣶⣶⣦⣤⣤⣤⣤⣴⣶⣶⣶⣶⣿⣿⠿⠟⠁
⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠀⠀⠐⠂⠠⠄
{Style.RESET_ALL}
"""

def get_network_interfaces():
    print(f"{blue}Network Interfaces:{Style.RESET_ALL}")
    interfaces = psutil.net_if_stats()
    for interface, stats in interfaces.items():
        print(f"{green}{interface}:{Style.RESET_ALL}")
        print(f"  isup: {stats.isup}")
        print(f"  duplex: {stats.duplex}")
        print(f"  speed: {stats.speed}")
        print(f"  mtu: {stats.mtu}")

def get_network_io_counters():
    print(f"{blue}Network I/O Counters:{Style.RESET_ALL}")
    io_counters = psutil.net_io_counters(pernic=True)
    for interface, counters in io_counters.items():
        print(f"{green}{interface}:{Style.RESET_ALL}")
        print(f"  bytes_sent: {counters.bytes_sent}")
        print(f"  bytes_recv: {counters.bytes_recv}")
        print(f"  packets_sent: {counters.packets_sent}")
        print(f"  packets_recv: {counters.packets_recv}")
        print(f"  errin: {counters.errin}")
        print(f"  errout: {counters.errout}")
        print(f"  dropin: {counters.dropin}")
        print(f"  dropout: {counters.dropout}")

def get_network_connections():
    print(f"{blue}Network Connections:{Style.RESET_ALL}")
    connections = psutil.net_connections()
    for conn in connections:
        laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
        raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
        print(f"{green}{conn.fd}:{Style.RESET_ALL}")
        print(f"  family: {conn.family}")
        print(f"  type: {conn.type}")
        print(f"  laddr: {laddr}")
        print(f"  raddr: {raddr}")
        print(f"  status: {conn.status}")

def main():
    print(banner())
    get_network_interfaces()
    get_network_io_counters()
    get_network_connections()

if __name__ == "__main__":
    main()
