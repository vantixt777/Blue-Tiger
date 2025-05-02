import requests
import json
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
⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣴⣶⣿⣿⣷⣤⡶⠿⡶⢦⡤⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⣿⣿⣩⣭⣽⣿⣿⣤⡿⣦⡈⢶⣝⣆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⡟⢻⣿⣿⣿⠟⡍⣿⢤⣿⣿⣦⢹⣼⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠘⣿⢸⣿⠟⠁⠀⣷⢼⣾⣿⠘⣿⣧⢸⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢰⣿⣿⣿⠀⠀⠀⠉⠘⠋⠁⠀⣾⣦⡾⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⢿⡿⠀⠀⣦⠀⠀⢠⡆⠀⢻⣿⠛⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣴⣶⣶⣤⣷⡀⠶⠈⠳⠶⠋⠀⢀⣾⣿⣶⣦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣷⣿⣆⠀⠀⠀⠀
⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀
⠀⠀⢰⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀                roblox + blue tiger = harmful
⠀⢠⠏⠀⠀⠽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⠀⠀
⢀⣻⣴⠦⣄⣀⣹⣿⣿⣿⣿⠉⣿⣿⣿⣿⣿⣿⣿⣿⠉⠉⠁⠀⠀⢸⠀⠀
⣿⡤⠌⡟⠆⢀⣿⣿⣿⣿⣿⡀⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⢸⡇⠀
⠳⣍⣠⣿⡷⠿⣿⣿⣿⣿⣿⠛⣿⣿⣿⣿⣿⣿⣿⣿⣤⣧⣤⣤⣤⣌⡇⠀
⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡆⣩⣑⣦⠈⢧⠀
⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⠯⢴⣿⡗⣿⢀⣼⠇
⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠻⠦⠝⠋⠁⠀
⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣴⡋⠀⠈⢻⡿⣋⣼⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠷⣜⣦⡄⢀⣷⣿⣿⠏⠁⠉⢻⣿⡽⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠈⠉⣏⢦⣀⡀⠀⣽⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠓⠾⠣⠖⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"""
    print(banner)

def get_user_id(username):
    url = "https://users.roblox.com/v1/usernames/users"
    payload = {"usernames": [username], "excludeBannedUsers": False}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json().get("data", [])
            if data:
                return data[0].get("id"), None
            return None, "User not found"
        return None, f"API error (HTTP {response.status_code})"
    except Exception as e:
        return None, str(e)

def get_user_info(user_id):
    endpoints = {
        "basic": f"https://users.roblox.com/v1/users/{user_id}",
        "presence": "https://presence.roblox.com/v1/presence/users",
        "badges": f"https://accountinformation.roblox.com/v1/users/{user_id}/roblox-badges",
        "friends": f"https://friends.roblox.com/v1/users/{user_id}/friends/count",
        "groups": f"https://groups.roblox.com/v1/users/{user_id}/groups/roles",
        "inventory": f"https://inventory.roblox.com/v1/users/{user_id}/items/collectibles?limit=10"
    }
    
    results = {}
    errors = []
    
    # Basic info
    try:
        response = requests.get(endpoints["basic"])
        if response.status_code == 200:
            results["basic"] = response.json()
        else:
            errors.append(f"Basic info: HTTP {response.status_code}")
    except Exception as e:
        errors.append(f"Basic info: {str(e)}")
    
    # Presence info
    try:
        response = requests.post(endpoints["presence"], json={"userIds": [user_id]})
        if response.status_code == 200:
            results["presence"] = response.json().get("userPresences", [{}])[0]
        else:
            errors.append(f"Presence: HTTP {response.status_code}")
    except Exception as e:
        errors.append(f"Presence: {str(e)}")
    
    # Badges
    try:
        response = requests.get(endpoints["badges"])
        if response.status_code == 200:
            results["badges"] = response.json()
        else:
            errors.append(f"Badges: HTTP {response.status_code}")
    except Exception as e:
        errors.append(f"Badges: {str(e)}")
    
    # Friends count
    try:
        response = requests.get(endpoints["friends"])
        if response.status_code == 200:
            results["friends"] = response.json()
        else:
            errors.append(f"Friends: HTTP {response.status_code}")
    except Exception as e:
        errors.append(f"Friends: {str(e)}")
    
    # Groups
    try:
        response = requests.get(endpoints["groups"])
        if response.status_code == 200:
            results["groups"] = response.json()
        else:
            errors.append(f"Groups: HTTP {response.status_code}")
    except Exception as e:
        errors.append(f"Groups: {str(e)}")
    
    # Inventory (limited to 10 collectibles)
    try:
        response = requests.get(endpoints["inventory"])
        if response.status_code == 200:
            results["inventory"] = response.json()
        else:
            errors.append(f"Inventory: HTTP {response.status_code}")
    except Exception as e:
        errors.append(f"Inventory: {str(e)}")
    
    return results, errors if errors else None

def format_user_info(data):
    if not data.get("basic"):
        return "No user data available"
    
    basic = data["basic"]
    presence = data.get("presence", {})
    badges = data.get("badges", [])
    friends = data.get("friends", {})
    groups = data.get("groups", {}).get("data", [])
    inventory = data.get("inventory", {}).get("data", [])
    
    info = f"""
{INFO_ADD} {colors.YELLOW}Basic Information:{colors.RESET}
    Username: {colors.WHITE}{basic.get('name', 'N/A')}{colors.RESET}
    Display Name: {colors.WHITE}{basic.get('displayName', 'N/A')}{colors.RESET}
    User ID: {colors.WHITE}{basic.get('id', 'N/A')}{colors.RESET}
    Description: {colors.WHITE}{basic.get('description', 'N/A')}{colors.RESET}
    Created: {colors.WHITE}{basic.get('created', 'N/A')}{colors.RESET}
    Is Banned: {colors.WHITE}{basic.get('isBanned', 'N/A')}{colors.RESET}
    Verified: {colors.WHITE}{basic.get('hasVerifiedBadge', False)}{colors.RESET}

{INFO_ADD} {colors.YELLOW}Presence:{colors.RESET}
    Status: {colors.WHITE}{presence.get('userPresenceType', 'N/A')}{colors.RESET}
    Last Online: {colors.WHITE}{presence.get('lastOnline', 'N/A')}{colors.RESET}
    Last Location: {colors.WHITE}{presence.get('lastLocation', 'N/A')}{colors.RESET}
    Game ID: {colors.WHITE}{presence.get('gameId', 'N/A')}{colors.RESET}
    Place ID: {colors.WHITE}{presence.get('placeId', 'N/A')}{colors.RESET}
    Universe ID: {colors.WHITE}{presence.get('universeId', 'N/A')}{colors.RESET}

{INFO_ADD} {colors.YELLOW}Social:{colors.RESET}
    Friends Count: {colors.WHITE}{friends.get('count', 'N/A')}{colors.RESET}
    Groups ({len(groups)}):"""
    
    for group in groups[:5]:  # Show first 5 groups
        info += f"\n        {colors.WHITE}• {group.get('group', {}).get('name', 'N/A')} ({group.get('role', {}).get('name', 'N/A')}){colors.RESET}"
    if len(groups) > 5:
        info += f"\n        {colors.WHITE}• ...and {len(groups)-5} more{colors.RESET}"
    
    info += f"""
    
{INFO_ADD} {colors.YELLOW}Badges ({len(badges)}):{colors.RESET}"""
    
    for badge in badges[:5]:  # Show first 5 badges
        info += f"\n        {colors.WHITE}• {badge.get('name', 'N/A')}{colors.RESET}"
    if len(badges) > 5:
        info += f"\n        {colors.WHITE}• ...and {len(badges)-5} more{colors.RESET}"
    
    info += f"""
    
{INFO_ADD} {colors.YELLOW}Recent Collectibles ({len(inventory)}):{colors.RESET}"""
    
    for item in inventory[:5]:  # Show first 5 inventory items
        info += f"\n        {colors.WHITE}• {item.get('name', 'N/A')}{colors.RESET}"
    if len(inventory) > 5:
        info += f"\n        {colors.WHITE}• ...and {len(inventory)-5} more{colors.RESET}"
    
    return info

def main():
    display_banner()
    
    while True:
        try:
            identifier = input(f"{INPUT} Enter Roblox Username or ID (or 'exit' to quit) -> {colors.WHITE}")
            
            if identifier.lower() == 'exit':
                print(f"{INFO} Exiting...{colors.RESET}")
                break
                
            if identifier.isdigit():
                user_id = identifier
            else:
                print(f"{WAIT} Looking up user ID...{colors.RESET}")
                user_id, error = get_user_id(identifier)
                if error:
                    print(f"{ERROR} Error: {error}{colors.RESET}")
                    continue
            
            print(f"{WAIT} Fetching user information...{colors.RESET}")
            
            user_data, error = get_user_info(user_id)
            
            if error:
                print(f"{ERROR} Partial data retrieved with errors:")
                for err in error:
                    print(f"    {ERROR} {err}")
                print()
            
            print(format_user_info(user_data))
            
        except KeyboardInterrupt:
            print(f"\n{INFO} Exiting...{colors.RESET}")
            break
        except Exception as e:
            print(f"{ERROR} An error occurred: {e}{colors.RESET}")

if __name__ == "__main__":
    main()