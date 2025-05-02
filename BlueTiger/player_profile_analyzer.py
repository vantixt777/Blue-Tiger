import requests
import json
from datetime import datetime
import webbrowser
from collections import Counter

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
⠀⠀⠀⠀⢀⣀⠀⠀⢀⠀⠀⠀⠀⠀⠀
⠀⠀⢠⣶⣽⣿⡿⣿⣿⣷⣶⡀⠀⠀⠀
⠀⠀⠘⣿⣿⢻⣧⠸⣿⣿⣿⣆⠀⠀⠀
⠀⠀⠀⠀⢻⡌⠉⡀⠿⢻⡿⡧⠀⠀⠀
⠀⠀⢀⣄⣘⣚⠛⠁⢀⣠⣃⠀⠀⠀⠀
⠀⠀⢸⣿⣿⣿⣦⣶⣿⣿⣿⣿⣾⣆⠀
⠀⠐⣙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀
⠠⠧⡒⢸⣿⣿⣿⣿⣿⣿⣿⡍⠭⣉⠅
⠐⠎⠃⠚⣿⣿⣿⣿⣿⣿⡿⣽⠴⠁⡺
⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣟⠧⢮⡗⣨
⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⡇⠀⠈⠀⠀
⠀⠀⠀⠀⢎⠈⣿⠛⢻⣿⠃⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠒⠀⠃⠀⠀⠀⠀⠀"""
    print(banner)

def get_user_id(username):
    url = "https://users.roblox.com/v1/usernames/users"
    payload = {"usernames": [username]}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json().get("data", [])
            if data:
                return data[0].get("id"), None
        return None, "User not found"
    except Exception as e:
        return None, str(e)

def fetch_player_data(user_id):
    endpoints = {
        "profile": f"https://users.roblox.com/v1/users/{user_id}",
        "presence": f"https://presence.roblox.com/v1/presence/users",
        "friends": f"https://friends.roblox.com/v1/users/{user_id}/friends",
        "followers": f"https://friends.roblox.com/v1/users/{user_id}/followers",
        "following": f"https://friends.roblox.com/v1/users/{user_id}/followings",
        "groups": f"https://groups.roblox.com/v1/users/{user_id}/groups/roles",
        "badges": f"https://accountinformation.roblox.com/v1/users/{user_id}/roblox-badges",
        "games": f"https://games.roblox.com/v2/users/{user_id}/games?accessFilter=2&limit=10",
        "inventory": f"https://inventory.roblox.com/v1/users/{user_id}/items/collectibles?limit=10"
    }
    
    data = {}
    errors = []
    
    with requests.Session() as session:
        for name, url in endpoints.items():
            try:
                if name == "presence":
                    response = session.post(url, json={"userIds": [user_id]})
                    if response.status_code == 200:
                        data[name] = response.json().get("userPresences", [{}])[0]
                else:
                    response = session.get(url)
                    if response.status_code == 200:
                        data[name] = response.json()
                    elif response.status_code == 403:
                        errors.append(f"Access denied to {name} data (private profile)")
            except Exception as e:
                errors.append(f"Error fetching {name}: {str(e)}")
    
    return data, errors if errors else None

def analyze_friends(friends_data):
    if not friends_data or not friends_data.get("data"):
        return None
    
    friends = friends_data["data"]
    friend_ids = [friend["id"] for friend in friends]
    creation_dates = [friend.get("created") for friend in friends if friend.get("created")]
    
    if not creation_dates:
        return None
    
    oldest_friend = min(creation_dates)
    newest_friend = max(creation_dates)
    avg_friend_age = (datetime.now() - datetime.strptime(oldest_friend, "%Y-%m-%dT%H:%M:%S.%fZ")).days / len(creation_dates)
    
    return {
        "count": len(friends),
        "oldest": oldest_friend,
        "newest": newest_friend,
        "avg_age_days": round(avg_friend_age, 1)
    }

def analyze_groups(groups_data):
    if not groups_data or not groups_data.get("data"):
        return None
    
    groups = groups_data["data"]
    group_roles = [group["role"]["name"] for group in groups if group.get("role")]
    role_counter = Counter(group_roles)
    
    return {
        "count": len(groups),
        "common_roles": role_counter.most_common(3),
        "premium": any(group.get("group", {}).get("owner", {}).get("id") == user_id for group in groups)
    }

def display_analysis(user_id, data, errors):
    profile = data.get("profile", {})
    presence = data.get("presence", {})
    friends = data.get("friends", {})
    groups = data.get("groups", {})
    badges = data.get("badges", [])
    games = data.get("games", {}).get("data", [])
    
    print(f"\n{INFO_ADD} {colors.YELLOW}Basic Profile Information:{colors.RESET}")
    print(f"    Username: {colors.WHITE}{profile.get('name', 'N/A')}{colors.RESET}")
    print(f"    Display Name: {colors.WHITE}{profile.get('displayName', 'N/A')}{colors.RESET}")
    print(f"    User ID: {colors.WHITE}{profile.get('id', 'N/A')}{colors.RESET}")
    print(f"    Account Age: {colors.WHITE}{profile.get('created', 'N/A')}{colors.RESET}")
    print(f"    Verified: {colors.WHITE}{profile.get('hasVerifiedBadge', False)}{colors.RESET}")
    print(f"    Status: {colors.WHITE}{presence.get('userPresenceType', 'N/A')}{colors.RESET}")
    print(f"    Last Online: {colors.WHITE}{presence.get('lastOnline', 'N/A')}{colors.RESET}")
    
    friends_analysis = analyze_friends(friends)
    if friends_analysis:
        print(f"\n{INFO_ADD} {colors.YELLOW}Friends Analysis:{colors.RESET}")
        print(f"    Friend Count: {colors.WHITE}{friends_analysis['count']}{colors.RESET}")
        print(f"    Oldest Friend: {colors.WHITE}{friends_analysis['oldest']}{colors.RESET}")
        print(f"    Newest Friend: {colors.WHITE}{friends_analysis['newest']}{colors.RESET}")
        print(f"    Avg Friend Age: {colors.WHITE}{friends_analysis['avg_age_days']} days{colors.RESET}")
    
    groups_analysis = analyze_groups(groups)
    if groups_analysis:
        print(f"\n{INFO_ADD} {colors.YELLOW}Groups Analysis:{colors.RESET}")
        print(f"    Group Count: {colors.WHITE}{groups_analysis['count']}{colors.RESET}")
        print(f"    Common Roles: {colors.WHITE}{', '.join([f'{role} ({count})' for role, count in groups_analysis['common_roles']])}{colors.RESET}")
        print(f"    Owns Groups: {colors.WHITE}{groups_analysis['premium']}{colors.RESET}")
    
    if badges:
        print(f"\n{INFO_ADD} {colors.YELLOW}Badges:{colors.RESET}")
        for badge in badges[:5]:
            print(f"    {colors.WHITE}• {badge.get('name', 'N/A')}{colors.RESET}")
        if len(badges) > 5:
            print(f"    {colors.WHITE}• ...and {len(badges)-5} more{colors.RESET}")
    
    if games:
        print(f"\n{INFO_ADD} {colors.YELLOW}Recently Played Games:{colors.RESET}")
        for game in games[:3]:
            print(f"    {colors.WHITE}• {game.get('name', 'N/A')} (Plays: {game.get('placeVisits', 'N/A')}){colors.RESET}")
        if len(games) > 3:
            print(f"    {colors.WHITE}• ...and {len(games)-3} more{colors.RESET}")
    
    print(f"\n{INFO_ADD} {colors.YELLOW}Profile Links:{colors.RESET}")
    print(f"    {colors.WHITE}• Web Profile: https://www.roblox.com/users/{user_id}/profile{colors.RESET}")
    print(f"    {colors.WHITE}• Friends: https://www.roblox.com/users/{user_id}/friends{colors.RESET}")
    print(f"    {colors.WHITE}• Groups: https://www.roblox.com/users/{user_id}/groups{colors.RESET}")
    
    if errors:
        print(f"\n{ERROR} Partial data with errors:{colors.RESET}")
        for error in errors:
            print(f"    {ERROR} {error}{colors.RESET}")

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
            
            print(f"{WAIT} Analyzing profile...{colors.RESET}")
            data, errors = fetch_player_data(user_id)
            
            display_analysis(user_id, data, errors)
            
            view_web = input(f"\n{INPUT} Open profile in browser? (y/n) -> {colors.WHITE}")
            if view_web.lower() == 'y':
                webbrowser.open(f"https://www.roblox.com/users/{user_id}/profile")
            
        except KeyboardInterrupt:
            print(f"\n{INFO} Exiting...{colors.RESET}")
            break
        except Exception as e:
            print(f"{ERROR} An error occurred: {e}{colors.RESET}")

if __name__ == "__main__":
    main()