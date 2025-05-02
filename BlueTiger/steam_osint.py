import requests
import json
from prettytable import PrettyTable
import sys
import os
from datetime import datetime

class SteamOSINT:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.steampowered.com"
        
    def display_banner(self):
        """Display a cool ASCII art banner"""
        banner = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠔⠒⠒⠒⠦⣤⣀⣀⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⡞⠁⢀⣤⣀⠀⠀⠀⠀⠀⠀⠉⠲⣤⠀
⠀⠀⠀⠀⢠⡤⠴⠚⠁⣰⣿⣿⣿⡆⠀⠀⣴⣶⣶⠄⠀⢻
⠀⠀⠀⡼⠁⠀⠀⠀⠀⠻⣿⣿⣿⠃⠀⣼⣿⣿⣿⠀⠀⠀⢷⡀
⠀⠀⣼⠁⠀⣤⣶⡄⠀⠀⠈⠉⠁⠀⠀⠈⠛⠊⠁⠀⠀⠀⠀⠙⢦
⠀⢠⡇⠀⢸⣿⣿⡿⡆⠀⠀⣴⣶⣶⣴⣶⣄⠀⠀⢠⣶⣿⣦⠀⠀⡄
⠀⢸⡇⠀⠀⠛⠙⠉⠀⣰⣿⣿⣿⣿⣿⣿⣿⡇⠀⣿⣿⣿⣿⠀⠀⡇
⠀⠈⣇⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣷⣿⣷⡀⠀⠉⠉⠀⠀⣸⡟
⠀⠀⣿⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⡻⠁
⠀⠀⣿⠀⠀⠀⠀⠀⠈⠛⠉⠁⠉⠁⠙⠻⠿⠟⠀⠀⠀⠀⠀⣾⠁
⠀⠀⢸⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡟⠁
⠀⠀⠀⣻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠁
        """
        print(banner)
        print("="*60)
        print(f"{'Steam Account tool':^60}")
        print(f"{'by vantixt':^60}")
        print("="*60)
        print()
        
    def search_user(self, username):
        """Search for a Steam user by name"""
        url = f"{self.base_url}/ISteamUser/ResolveVanityURL/v1/"
        params = {
            'key': self.api_key,
            'vanityurl': username
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['response']['success'] == 1:
                steam_id = data['response']['steamid']
                return self.get_user_details(steam_id)
            else:
                return {"error": "User not found"}
                
        except requests.exceptions.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}
    
    def get_user_details(self, steam_id):
        """Get detailed information about a Steam user"""
        url = f"{self.base_url}/ISteamUser/GetPlayerSummaries/v2/"
        params = {
            'key': self.api_key,
            'steamids': steam_id
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['response']['players']:
                return data['response']['players'][0]
            else:
                return {"error": "No user details found"}
                
        except requests.exceptions.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}
    
    def display_results(self, user_data):
        """Display the user information in a formatted table"""
        if 'error' in user_data:
            print(f"\n[!] Error: {user_data['error']}")
            return
            
        print("\n[+] Steam Account Information Found:")
        table = PrettyTable()
        table.field_names = ["Field", "Value"]
        table.align["Field"] = "l"
        table.align["Value"] = "l"
        
        # Add basic information
        table.add_row(["SteamID", user_data.get('steamid', 'N/A')])
        table.add_row(["Username", user_data.get('personaname', 'N/A')])
        table.add_row(["Profile URL", user_data.get('profileurl', 'N/A')])
        table.add_row(["Account Created", self.format_timestamp(user_data.get('timecreated', 0))])
        table.add_row(["Last Logoff", self.format_timestamp(user_data.get('lastlogoff', 0))])
        table.add_row(["Country", user_data.get('loccountrycode', 'N/A')])
        table.add_row(["State/Province", user_data.get('locstatecode', 'N/A')])
        table.add_row(["City", user_data.get('loccityid', 'N/A')])
        table.add_row(["Profile Visibility", "Public" if user_data.get('communityvisibilitystate', 1) == 3 else "Private"])
        
        print(table)
        
        # Add avatar URLs if available
        print("\n[+] Avatar URLs:")
        print(f"Small: {user_data.get('avatar', 'N/A')}")
        print(f"Medium: {user_data.get('avatarmedium', 'N/A')}")
        print(f"Large: {user_data.get('avatarfull', 'N/A')}")
        
    def format_timestamp(self, timestamp):
        """Convert Unix timestamp to readable date"""
        if timestamp == 0:
            return "N/A"
        return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S UTC')

def get_api_key():
    """Prompt user for API key or check environment variable"""
    api_key = os.getenv('STEAM_API_KEY')
    if api_key:
        print("[*] Using Steam API key from environment variable")
        return api_key
    
    print("\n[i] You need a Steam Web API key to use this tool")
    print("[i] Get one from: https://steamcommunity.com/dev/apikey")
    api_key = input("[?] Enter your Steam API key: ").strip()
    
    if not api_key:
        print("[!] API key is required to continue")
        sys.exit(1)
        
    return api_key

def main():
    # Initialize tool and display banner
    tool = SteamOSINT("temp")  # Temporary key for banner display
    tool.display_banner()
    
    # Get API key
    api_key = get_api_key()
    tool = SteamOSINT(api_key)
    
    # Get username to search
    print("\n[i] You can search by profile name or custom URL")
    username = input("[?] Enter Steam username to search: ").strip()
    
    if not username:
        print("[!] Username is required")
        sys.exit(1)
    
    print(f"\n[*] Searching for Steam user: {username}")
    user_data = tool.search_user(username)
    tool.display_results(user_data)

if __name__ == "__main__":
    main()