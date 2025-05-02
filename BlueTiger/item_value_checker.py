import requests
import json
from datetime import datetime
import webbrowser

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
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣴⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠉⠛⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⢰⣿⣿⠇⠀⠉⠉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠉⠉⠛⠛⠿⠿⡏⠀⠀⠀⣾⣿⡿⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀
⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠃⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀
⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀
⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⢠⣶⣦⣤⣀⡀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀
⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣷⡄⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠘⠿⠿⢿⣿⣿⡿⠟⠁⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⣴⣶⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠐⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⢿⡿⠁⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃
⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀
⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀
⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⣾⣿⣿⠀⠀⠀⢠⣤⣄⣀⣀⣀⣀⣤⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀
⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⢰⣿⣿⡇⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣦⣾⣿⣿⡀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠻⠿⠿⢿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠟⠛⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"""
    print(banner)

def get_item_id(item_name):
    url = "https://catalog.roblox.com/v1/search/items"
    params = {
        "category": "All",
        "limit": 10,
        "keyword": item_name
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            items = response.json().get("data", [])
            if items:
                return items[0].get("id"), None
        return None, "Item not found"
    except Exception as e:
        return None, str(e)

def get_item_details(item_id):
    sources = {
        "roblox": f"https://economy.roblox.com/v2/assets/{item_id}/details",
        "rolimons": f"https://www.rolimons.com/itemapi/itemdetails",
        "rblx_trade": f"https://rblx.trade/api/v2/items/{item_id}"
    }
    
    data = {}
    errors = []
    
    # Roblox Official API
    try:
        response = requests.get(sources["roblox"])
        if response.status_code == 200:
            data["roblox"] = response.json()
        else:
            errors.append(f"Roblox API: HTTP {response.status_code}")
    except Exception as e:
        errors.append(f"Roblox API: {str(e)}")
    
    # Rolimons (community pricing)
    try:
        response = requests.get(sources["rolimons"])
        if response.status_code == 200:
            all_items = response.json().get("items", {})
            if str(item_id) in all_items:
                data["rolimons"] = all_items[str(item_id)]
    except Exception as e:
        errors.append(f"Rolimons: {str(e)}")
    
    # RBX.Trade (historical sales)
    try:
        response = requests.get(sources["rblx_trade"])
        if response.status_code == 200:
            data["rblx_trade"] = response.json()
    except Exception as e:
        errors.append(f"RBX.Trade: {str(e)}")
    
    return data, errors if errors else None

def format_price(price):
    if not price:
        return "N/A"
    return f"R$ {price:,}"

def display_item_info(item_id, item_name, data, errors):
    roblox_data = data.get("roblox", {})
    rolimons_data = data.get("rolimons", [])
    rblx_trade_data = data.get("rblx_trade", {})
    
    print(f"\n{INFO_ADD} {colors.YELLOW}Basic Information:{colors.RESET}")
    print(f"    Name: {colors.WHITE}{item_name}{colors.RESET}")
    print(f"    Item ID: {colors.WHITE}{item_id}{colors.RESET}")
    print(f"    Asset Type: {colors.WHITE}{roblox_data.get('AssetType', 'N/A')}{colors.RESET}")
    print(f"    Creator: {colors.WHITE}{roblox_data.get('Creator', {}).get('Name', 'N/A')}{colors.RESET}")
    print(f"    Created: {colors.WHITE}{roblox_data.get('Created', 'N/A')}{colors.RESET}")
    
    print(f"\n{INFO_ADD} {colors.YELLOW}Current Values:{colors.RESET}")
    print(f"    Roblox Price: {colors.WHITE}{format_price(roblox_data.get('Price'))}{colors.RESET}")
    print(f"    Roblox Resale: {colors.WHITE}{format_price(roblox_data.get('Remaining', {}).get('ResalePrice'))}{colors.RESET}")
    
    if rolimons_data:
        print(f"\n{INFO_ADD} {colors.YELLOW}Community Values (Rolimons):{colors.RESET}")
        print(f"    Value: {colors.WHITE}{format_price(rolimons_data[2])}{colors.RESET}")
        print(f"    Demand: {colors.WHITE}{rolimons_data[5]}/5{colors.RESET}")
        print(f"    Trend: {colors.WHITE}{rolimons_data[6]}{colors.RESET}")
        print(f"    Projected Value: {colors.WHITE}{format_price(rolimons_data[3])}{colors.RESET}")
    
    if rblx_trade_data:
        recent_sales = rblx_trade_data.get("recentSales", [])
        if recent_sales:
            print(f"\n{INFO_ADD} {colors.YELLOW}Recent Sales (RBX.Trade):{colors.RESET}")
            for sale in recent_sales[:3]:
                date = datetime.fromtimestamp(sale["timestamp"]).strftime('%Y-%m-%d')
                print(f"    {colors.WHITE}• {date}: {format_price(sale['price'])} (Qty: {sale['quantity']}){colors.RESET}")
    
    print(f"\n{INFO_ADD} {colors.YELLOW}Quick Links:{colors.RESET}")
    print(f"    {colors.WHITE}• Roblox Catalog: https://www.roblox.com/catalog/{item_id}{colors.RESET}")
    print(f"    {colors.WHITE}• Rolimons: https://www.rolimons.com/item/{item_id}{colors.RESET}")
    print(f"    {colors.WHITE}• RBX.Trade: https://rblx.trade/items/{item_id}{colors.RESET}")
    
    if errors:
        print(f"\n{ERROR} Partial data with errors:{colors.RESET}")
        for error in errors:
            print(f"    {ERROR} {error}{colors.RESET}")

def main():
    display_banner()
    
    while True:
        try:
            item_name = input(f"{INPUT} Enter item name or ID (or 'exit' to quit) -> {colors.WHITE}")
            
            if item_name.lower() == 'exit':
                print(f"{INFO} Exiting...{colors.RESET}")
                break
                
            if item_name.isdigit():
                item_id = item_name
                item_name = "Unknown"
            else:
                print(f"{WAIT} Searching for item...{colors.RESET}")
                item_id, error = get_item_id(item_name)
                if error:
                    print(f"{ERROR} Error: {error}{colors.RESET}")
                    continue
            
            print(f"{WAIT} Fetching item values...{colors.RESET}")
            data, errors = get_item_details(item_id)
            
            display_item_info(item_id, item_name, data, errors)
            
            view_web = input(f"\n{INPUT} Open item in browser? (y/n) -> {colors.WHITE}")
            if view_web.lower() == 'y':
                webbrowser.open(f"https://www.roblox.com/catalog/{item_id}")
            
        except KeyboardInterrupt:
            print(f"\n{INFO} Exiting...{colors.RESET}")
            break
        except Exception as e:
            print(f"{ERROR} An error occurred: {e}{colors.RESET}")

if __name__ == "__main__":
    main()