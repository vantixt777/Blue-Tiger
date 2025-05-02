import json
import requests
from bs4 import BeautifulSoup as BSoup
from datetime import datetime

# Color codes
ESC = '\x1b'
RED = ESC + '[31m'
GREEN = ESC + '[32m'
YELLOW = ESC + '[33m'
BLUE = ESC + '[34m'
MAGENTA = ESC + '[35m'
CYAN = ESC + '[36m'
RESET = ESC + '[0m'

def display_banner():
    print(f"""{CYAN}
 ▀█████████▄   ▄█       ███    █▄     ▄████████          ███      ▄█     ▄█   ▄█▄     ███      ▄██████▄     ▄█   ▄█▄ 
  ███    ███ ███       ███    ███   ███    ███      ▀█████████▄ ███    ███ ▄███▀ ▀█████████▄ ███    ███   ███ ▄███▀ 
  ███    ███ ███       ███    ███   ███    █▀          ▀███▀▀██ ███▌   ███▐██▀      ▀███▀▀██ ███    ███   ███▐██▀                 vantixt mwa
 ▄███▄▄▄██▀  ███       ███    ███  ▄███▄▄▄              ███   ▀ ███▌  ▄█████▀        ███   ▀ ███    ███  ▄█████▀    
▀▀███▀▀▀██▄  ███       ███    ███ ▀▀███▀▀▀              ███     ███▌ ▀▀█████▄        ███     ███    ███ ▀▀█████▄    
  ███    ██▄ ███       ███    ███   ███    █▄           ███     ███    ███▐██▄       ███     ███    ███   ███▐██▄   
  ███    ███ ███▌    ▄ ███    ███   ███    ███          ███     ███    ███ ▀███▄     ███     ███    ███   ███ ▀███▄ 
▄█████████▀  █████▄▄██ ████████▀    ██████████         ▄████▀   █▀     ███   ▀█▀    ▄████▀    ▀██████▀    ███   ▀█▀ 
             ▀                                                         ▀                                  ▀         
  {YELLOW}Type username when prompted{RESET}
  {MAGENTA}baka baka baka{RESET}
""")

def get_tiktok_data(username: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    url = f'https://www.tiktok.com/@{username}'

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BSoup(response.text, 'html.parser')
        script_tag = soup.find('script', id='__UNIVERSAL_DATA_FOR_REHYDRATION__')
        
        if script_tag:
            return json.loads(script_tag.string)
        return None
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
        return None

def display_account_info(data):
    if not data:
        return False

    user_info = data.get('__DEFAULT_SCOPE__', {}).get('webapp.user-detail', {})
    user = user_info.get('userInfo', {}).get('user', {})
    stats = user_info.get('userInfo', {}).get('stats', {})
    
    print(f"\n{CYAN}=== Account Information ==={RESET}")
    print(f"{YELLOW}Username:{RESET} @{user.get('uniqueId', 'N/A')}")
    print(f"{YELLOW}Nickname:{RESET} {user.get('nickname', 'N/A')}")
    print(f"{YELLOW}Followers:{RESET} {stats.get('followerCount', 'N/A')}")
    print(f"{YELLOW}Following:{RESET} {stats.get('followingCount', 'N/A')}")
    print(f"{YELLOW}Total Likes:{RESET} {stats.get('heartCount', 'N/A')}")
    print(f"{YELLOW}Country:{RESET} {user.get('region', 'N/A')}")
    
    return True

def main():
    display_banner()
    
    while True:
        print("\n" + "="*40)
        username = input("Enter TikTok username (@ optional) or 'exit': ").strip().lstrip('@')
        
        if username.lower() == 'exit':
            print(f"\n{GREEN}Goodbye!{RESET}")
            break
            
        if not username:
            print(f"{RED}Please enter a username{RESET}")
            continue
            
        print(f"\n{YELLOW}Checking @{username}...{RESET}")
        data = get_tiktok_data(username)
        
        if not display_account_info(data):
            print(f"{RED}No data found for @{username}{RESET}")

if __name__ == '__main__':
    main()