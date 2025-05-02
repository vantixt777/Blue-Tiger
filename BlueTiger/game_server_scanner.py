import requests
import json
import concurrent.futures
from datetime import datetime

class colors:
    WHITE = '\033[97m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

INFO = f"{colors.BLUE}[i]{colors.RESET}"
INPUT = f"{colors.YELLOW}[?]{colors.RESET}"
WAIT = f"{colors.MAGENTA}[~]{colors.RESET}"
INFO_ADD = f"{colors.CYAN}[+]{colors.RESET}"
ERROR = f"{colors.RED}[!]{colors.RESET}"
SUCCESS = f"{colors.GREEN}[✓]{colors.RESET}"

def display_banner():
    banner = f"""
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠛⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠈⠉⠉⠛⠻⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠙⠛⠻⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠙⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⡶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠛⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣦⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣦⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⣤⣀⣀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠛⠛⠛⠛⠻⣿⣿⡏⠛⠛⠻⠿⣿⡟⠛⠛⠛⠛⢿⡿⠛⠛⣿⣿⣿⠛⠛⠛⠛⠛⢻⡟⠛⠛⣿⠟⠛⢻⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠀⠀⠰⠀⠀⢸⡿⠀⠀⣀⠀⠀⢸⡇⠀⠀⠂⠀⢠⡇⠀⠀⣿⣿⣿⠀⠀⣀⠀⠀⢸⣿⣦⠀⠀⠀⣠⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠀⠀⢰⡀⠀⠹⡇⠀⠀⠉⠀⠀⣿⡇⠀⠀⠆⠀⠈⡇⠀⠀⠻⠿⢿⠀⠀⠉⠀⠀⢸⣿⠋⠀⢀⠀⠘⢿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣶⣶⣾⣷⣶⣶⣿⣷⣶⣦⣤⣼⣿⣷⣶⣶⣶⣶⣾⣷⣶⣶⣶⣶⣾⣶⣶⣶⣶⣶⣾⣷⣶⣶⣿⣶⣶⣶⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿"""
    print(banner)

def get_game_info(universe_id):
    url = f"https://games.roblox.com/v1/games?universeIds={universe_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json().get("data", [])
            if data:
                return data[0]
        return None
    except Exception as e:
        print(f"{ERROR} Error fetching game info: {e}{colors.RESET}")
        return None

def get_servers(universe_id, limit=100, cursor=""):
    url = f"https://games.roblox.com/v1/games/{universe_id}/servers/Public"
    params = {
        "limit": limit,
        "cursor": cursor
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"{ERROR} Error fetching servers: {e}{colors.RESET}")
        return None

def scan_server(server):
    try:
        ping_url = f"http://{server['ip']}:{server['port']}/ping"
        response = requests.get(ping_url, timeout=5)
        if response.status_code == 200:
            return True, server
        return False, server
    except:
        return False, server

def display_server_info(game_info, server_data, active_servers):
    print(f"\n{INFO_ADD} {colors.YELLOW}Game Information:{colors.RESET}")
    print(f"    Name: {colors.WHITE}{game_info.get('name', 'N/A')}{colors.RESET}")
    print(f"    Players: {colors.WHITE}{game_info.get('playing', 0)}/{game_info.get('maxPlayers', 0)}{colors.RESET}")
    print(f"    Active Servers: {colors.WHITE}{len(active_servers)}/{len(server_data)}{colors.RESET}")
    
    print(f"\n{INFO_ADD} {colors.YELLOW}Server List:{colors.RESET}")
    for idx, server in enumerate(active_servers[:10], 1):  # Show first 10 active servers
        print(f"    {idx}. {colors.WHITE}{server['id']}{colors.RESET}")
        print(f"       IP: {colors.CYAN}{server['ip']}:{server['port']}{colors.RESET}")
        print(f"       Players: {colors.GREEN}{server['playing']}/{server['maxPlayers']}{colors.RESET}")
        print(f"       FPS: {colors.MAGENTA}{server.get('fps', 'N/A')}{colors.RESET}")
        print(f"       Ping: {colors.BLUE}{server.get('ping', 'N/A')}ms{colors.RESET}")
    
    if len(active_servers) > 10:
        print(f"\n    {colors.WHITE}...and {len(active_servers)-10} more servers{colors.RESET}")

def main():
    display_banner()
    
    while True:
        try:
            universe_id = input(f"{INPUT} Enter Roblox Universe ID (or 'exit' to quit) -> {colors.WHITE}")
            
            if universe_id.lower() == 'exit':
                print(f"{INFO} Exiting...{colors.RESET}")
                break
                
            if not universe_id.isdigit():
                print(f"{ERROR} Invalid Universe ID. Please enter numbers only.{colors.RESET}")
                continue
                
            print(f"{WAIT} Fetching game information...{colors.RESET}")
            game_info = get_game_info(universe_id)
            
            if not game_info:
                print(f"{ERROR} Game not found or API error.{colors.RESET}")
                continue
                
            print(f"{WAIT} Scanning servers...{colors.RESET}")
            servers_data = get_servers(universe_id)
            
            if not servers_data or not servers_data.get("data"):
                print(f"{ERROR} No servers found for this game.{colors.RESET}")
                continue
                
            servers = servers_data["data"]
            active_servers = []
            
            # Use threading to scan servers faster
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                futures = [executor.submit(scan_server, server) for server in servers]
                for future in concurrent.futures.as_completed(futures):
                    is_active, server = future.result()
                    if is_active:
                        active_servers.append(server)
            
            display_server_info(game_info, servers, active_servers)
            
        except KeyboardInterrupt:
            print(f"\n{INFO} Exiting...{colors.RESET}")
            break
        except Exception as e:
            print(f"{ERROR} An error occurred: {e}{colors.RESET}")

if __name__ == "__main__":
    main()