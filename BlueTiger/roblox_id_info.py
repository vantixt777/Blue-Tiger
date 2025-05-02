import requests
import json
from datetime import datetime

# Color codes for terminal output
class colors:
    WHITE = '\033[97m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

# Symbols for display
INFO = f"{colors.BLUE}[i]{colors.RESET}"
INPUT = f"{colors.YELLOW}[?]{colors.RESET}"
WAIT = f"{colors.MAGENTA}[~]{colors.RESET}"
INFO_ADD = f"{colors.CYAN}[+]{colors.RESET}"
ERROR = f"{colors.RED}[!]{colors.RESET}"

def display_banner():
    banner = f"""
⠀⠀⠀⠀⢀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡀⢀⡀⠀⠀⠀
⣤⣶⣶⡿⠿⠿⠿⠿⠿⣶⣶⣶⠄⠀⠀⠐⢶⣶⣶⣿⡿⠿⠿⠿⠿⢿⣷⠦⠀
⠙⠏⠁⠀⣤⣶⣶⣶⣶⣒⢳⣆⠀⠀⠀⠀⢠⡞⣒⣲⣶⣖⣶⣦⡀⠀⠉⠛⠁
⠀⠀⠴⢯⣁⣿⣿⣿⣏⣿⡀⠟⠀⠀⠀⠀⠸⠀⣼⣋⣿⣿⣿⣦⣭⠷⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀                 sigma roblox + blue tiger= häcker
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠟⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡄⠀⢰⠏⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⡴⠟⠁⢀⡟⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠸⡗⠶⠶⠶⠶⠶⠖⠚⠛⠛⠋⠉⠀⠀⠀⠀⢸⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠀⠀⠀⠀⠀"""
    print(banner)

def get_user_info(user_id):
    try:
        # First API endpoint for basic user info
        user_url = f"https://users.roblox.com/v1/users/{user_id}"
        response = requests.get(user_url)
        
        if response.status_code != 200:
            return None, f"User not found (HTTP {response.status_code})"
        
        user_data = response.json()
        
        # Second API endpoint for additional details
        presence_url = f"https://presence.roblox.com/v1/presence/users"
        response = requests.post(presence_url, json={"userIds": [user_id]})
        presence_data = response.json().get("userPresences", [{}])[0] if response.status_code == 200 else {}
        
        # Third API endpoint for badges
        badges_url = f"https://accountinformation.roblox.com/v1/users/{user_id}/roblox-badges"
        badges_response = requests.get(badges_url)
        badges_data = badges_response.json() if badges_response.status_code == 200 else []
        
        # Combine all data
        combined_data = {
            "basic_info": user_data,
            "presence": presence_data,
            "badges": badges_data
        }
        
        return combined_data, None
        
    except Exception as e:
        return None, str(e)

def format_user_info(data):
    if not data:
        return "No data available"
    
    basic = data.get("basic_info", {})
    presence = data.get("presence", {})
    badges = data.get("badges", [])
    
    # Format basic info
    info = f"""
    {INFO_ADD} Username: {colors.WHITE}{basic.get('name', 'N/A')}{colors.RESET}
    {INFO_ADD} Display Name: {colors.WHITE}{basic.get('displayName', 'N/A')}{colors.RESET}
    {INFO_ADD} User ID: {colors.WHITE}{basic.get('id', 'N/A')}{colors.RESET}
    {INFO_ADD} Description: {colors.WHITE}{basic.get('description', 'N/A')}{colors.RESET}
    {INFO_ADD} Created: {colors.WHITE}{basic.get('created', 'N/A')}{colors.RESET}
    {INFO_ADD} Is Banned: {colors.WHITE}{basic.get('isBanned', 'N/A')}{colors.RESET}
    
    {INFO_ADD} Status: {colors.WHITE}{presence.get('userPresenceType', 'N/A')}{colors.RESET}
    {INFO_ADD} Last Online: {colors.WHITE}{presence.get('lastOnline', 'N/A')}{colors.RESET}
    {INFO_ADD} Last Location: {colors.WHITE}{presence.get('lastLocation', 'N/A')}{colors.RESET}
    {INFO_ADD} Game ID: {colors.WHITE}{presence.get('gameId', 'N/A')}{colors.RESET}
    
    {INFO_ADD} Badges ({len(badges)}):"""
    
    for badge in badges:
        info += f"\n        {colors.WHITE}• {badge.get('name', 'N/A')}{colors.RESET}"
    
    return info

def main():
    display_banner()
    
    while True:
        try:
            user_id = input(f"{INPUT} Enter Roblox User ID (or 'exit' to quit) -> {colors.WHITE}")
            
            if user_id.lower() == 'exit':
                print(f"{INFO} Exiting...{colors.RESET}")
                break
                
            if not user_id.isdigit():
                print(f"{ERROR} Invalid User ID. Please enter numbers only.{colors.RESET}")
                continue
                
            print(f"{WAIT} Fetching user information...{colors.RESET}")
            
            user_data, error = get_user_info(user_id)
            
            if error:
                print(f"{ERROR} Error: {error}{colors.RESET}")
            else:
                print(format_user_info(user_data))
                
        except KeyboardInterrupt:
            print(f"\n{INFO} Exiting...{colors.RESET}")
            break
        except Exception as e:
            print(f"{ERROR} An error occurred: {e}{colors.RESET}")

if __name__ == "__main__":
    main()