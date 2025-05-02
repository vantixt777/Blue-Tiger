from colorama import Fore, Style, init
from termcolor import colored
import os
import sys
import subprocess
import webbrowser

# Init colorama
init(autoreset=True)

blue = Fore.BLUE
white = Fore.WHITE
red = Fore.RED

# Display banner with blue color using termcolor
def print_banner():
    banner_text = """
▀█████████▄   ▄█       ███    █▄     ▄████████          ███      ▄█     ▄██████▄     ▄████████    ▄████████ 
  ███    ███ ███       ███    ███   ███    ███      ▀█████████▄ ███    ███    ███   ███    ███   ███    ███ 
  ███    ███ ███       ███    ███   ███    █▀          ▀███▀▀██ ███▌   ███    █▀    ███    █▀    ███    ███ 
 ▄███▄▄▄██▀  ███       ███    ███  ▄███▄▄▄              ███   ▀ ███▌  ▄███         ▄███▄▄▄      ▄███▄▄▄▄██▀ 
▀▀███▀▀▀██▄  ███       ███    ███ ▀▀███▀▀▀              ███     ███▌ ▀▀███ ████▄  ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   
  ███    ██▄ ███       ███    ███   ███    █▄           ███     ███    ███    ███   ███    █▄  ▀███████████ 
  ███    ███ ███▌    ▄ ███    ███   ███    ███          ███     ███    ███    ███   ███    ███   ███    ███ 
▄█████████▀  █████▄▄██ ████████▀    ██████████         ▄████▀   █▀     ████████▀    ██████████   ███    ███ 
             ▀                                                                                   ███    ███ 
                                by vantixt
"""
    colored_banner = colored(banner_text, 'blue')
    print(colored_banner + Style.RESET_ALL)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Kategorien (unverändert)
network_tools = [
    "Website-Vulnerability-Scanner",
    "Website-Info-Scanner",
    "Website-Url-Scanner",
    "Ip-Scanner",
    "Ip-Port-Scanner",
    "Ip-Pinger",
    "Network-Traffic-Analyzer",
    "DNS-Lookup",
    "WHOIS-Query",
    "Subnet-Calculator"
]

osint_tools = [
    "Get-Image-Exif",
    "Google-Dorking",
    "Username-Tracker",
    "Email-Tracker",
    "Email-Lookup",
    "Phone-Number-Lookup",
    "Ip-Lookup",
    "Social-Media-Scanner"
]

security_tools = [
    "Phishing-Simulator",
    "Password-Cracker",
    "Hash-Analyzer",
    "SQL-Injection-Tester",
    "XSS-Scanner",
    "File-Integrity-Checker",
    "VPN-Checker",
    "Proxy-Verifier",
    "MAC-Spoofer",
    "DNS-Spoof-Detector"
]

game_tools = [
    "Roblox-Cookie-Info",
    "Roblox-Id-Info",
    "Roblox-User-Info",
    "Game-Server-Scanner",
    "Player-Profile-Analyzer",
    "Item-Value-Checker",
    "Trade-History-Tracker",
    "Gun-LoL-Checker",
    "Aniworld-Scanner",
    "TikTok-OSINT",
    "Steam-Osint",
    "Valorant-Osint"
]

# Funktion zur Darstellung eines Optionsblocks (unverändert)
def format_option(number, name):
    return f"{blue}[{white}{str(number).zfill(2)}{blue}]{white} {name.ljust(30)[:30].replace('-', ' ')}"

def show_menu(menu_num=1):
    clear()
    print_banner()

    if menu_num == 1:
        # Menü 1: Network, OSINT, Security (mit blauem Muster)
        print(f" ┌─ {blue}[{white}I{blue}]{white} Info{white} ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── {blue}[{white}N{blue}]{white} Next ─┐")
        print(f" ├─ ┌─────────────────┐{white} ────────────────────────────── ┌───────┐{white} ────────────────────────────── ┌────────────┐{white} ────────────────────────────── │")
        print(f" └─┬─┤ {blue}Network Tools{white} ├─────────┬──────────────┤ {blue}OSINT{white} ├──────────────┬────────────┤ {blue}Security{white} ├────────────┴─")
        print(f"   │ └─────────────────┘{white} ────────────────────────────── │       │{white} ────────────────────────────── │            │{white} ──────────────────────────────")

        for i in range(10):
            net = format_option(i+1, network_tools[i])
            osi = format_option(i+11, osint_tools[i]) if i < len(osint_tools) else "".ljust(40)
            sec = format_option(i+21, security_tools[i]) if i < len(security_tools) else ""
            print(f"   ├─ {net}├─ {osi}├─ {sec}")

    elif menu_num == 2:
        # Menü 2: Game Tools (mit blauem Muster)
        print(f" ┌─ {blue}[{white}I{blue}]{white} Info{white} ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── {blue}[{white}B{blue}]{white} Back ─┐")
        print(f"─┴─┬─┤ {blue}Game Tools{white} ├───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴─")
        print(f"   │ └─────────────────┘")

        for i in range(0, 12, 2):
            left = format_option(i+31, game_tools[i]) if i < len(game_tools) else ""
            right = format_option(i+32, game_tools[i+1]) if i+1 < len(game_tools) else ""
            print(f"   ├─ {left.ljust(40)}{right}")

def handle_selection(option):
    file_mapping = {
        # Network Tools
        1: "website_vulnerability_scanner.py",
        2: "website_info_scanner.py",
        3: "website_url_scanner.py",
        4: "ip_scanner.py",
        5: "ip_port_scanner.py",
        6: "ip_pinger.py",
        7: "network_traffic_analyzer.py",
        8: "dns_lookup.py",
        9: "whois_query.py",
        10: "subnet_calculator.py",

        # OSINT Tools
        11: "get_image_exif.py",
        12: "google_dorking.py",
        13: "username_tracker.py",
        14: "email_tracker.py",
        15: "email_lookup.py",
        16: "phone_number_lookup.py",
        17: "ip_lookup.py",
        18: "social_media_scanner.py",


        # Security Tools
        21: "phishing_simulator.py",
        22: "password_cracker.py",
        23: "hash_analyzer.py",
        24: "sql_injection_tester.py",
        25: "xss_scanner.py",
        26: "file_integrity_checker.py",
        27: "vpn_checker.py",
        28: "proxy_verifier.py",
        29: "mac_spoofer.py",
        30: "dns_spoof_detector.py",

        # Game Tools
        31: "roblox_cookie_info.py",
        32: "roblox_id_info.py",
        33: "roblox_user_info.py",
        34: "game_server_scanner.py",
        35: "player_profile_analyzer.py",
        36: "item_value_checker.py",
        37: "trade_history_tracker.py",
        38: "gun_lol_checker.py",
        39: "aniworld_scanner.py",
        40: "tiktok_osint.py",
        41: "steam_osint.py",
        42: "valorant_osint.py"
    }

    if option == 0:
        sys.exit(0)
    elif option == 99:
        webbrowser.open("https://crylux.org")
    elif option in file_mapping:
        file_name = file_mapping[option]
        if os.path.exists(file_name):
            subprocess.run([sys.executable, file_name])
        else:
            print(f"{red}Tool {file_name} not found.")
    else:
        print(f"{red}Invalid option. Please try again.")

def main():
    current_menu = 1
    while True:
        show_menu(current_menu)
        try:
            choice = input(f"┌──({white}{os.getlogin()}@crylux)─{blue}[{white}~/{current_menu}\n└─{white}$ ")

            if choice.upper() in ['N', 'NEXT']:
                current_menu = 2
            elif choice.upper() in ['B', 'BACK']:
                current_menu = 1
            elif choice.upper() in ['I', 'INFO']:
                print(f"\n{blue}Crylux v1.0 - Advanced Cybersecurity Toolkit")
                print("GitHub: https://github.com/vantixt777")
                input(f"{white}Press Enter to continue...")
            elif choice.upper() in ['S', 'SITE']:
                webbrowser.open("https://crylux.org")
            elif choice.isdigit():
                handle_selection(int(choice))
                input(f"{white}Press Enter to continue...")
            else:
                print(f"{red}Invalid input. Use numbers or commands [N/B/I/S]")

        except ValueError:
            print(f"{red}Please enter a valid number or command")
        except KeyboardInterrupt:
            print(f"\n{blue}Exiting Crylux...")
            sys.exit(0)

if __name__ == "__main__":
    main()
