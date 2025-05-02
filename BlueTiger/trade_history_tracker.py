import requests
import json
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

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
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣄⣀⣀⣠⡴⠶⣄⠀⢀⣤⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣄⠀⠹⠤⠃⠀⡏⠉⠉⠳⢾⡿⣻⡆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⡀⠀⠀⠀⠇⠀⠀⠀⣠⠞⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣴⡀⡀⠀⣴⣆⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣷⣷⣷⣶⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢨⣿⡿⢻⣿⢻⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠏⠜⠀⠈⢉⣿⡟⢿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡞⠁⠀⠀⠀⠀⠀⠉⠁⠈⢻⠳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⡴⠋⠀⠀⠀⠀⢀⣤⣄⠀⠀⠀⠀⠣⠙⢦⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣰⠟⠀⠀⠀⠀⠀⠀⣿⣿⣿⠀⠀⠀⠀⠀⠰⠂⠙⣦⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⡾⠁⠀⠀⠀⠀⣀⣴⣾⣿⣿⣿⣿⣶⣤⡀⠀⠀⠐⣂⠈⢳⡄⠀⠀⠀⠀
⠀⠀⠀⣠⠟⠀⠀⠀⠀⠀⣴⣿⣿⡿⣿⣿⣿⠿⣿⣿⣿⣆⠀⠀⠰⢒⠵⢻⣆⠀⠀⠀
⠀⠀⣰⠏⠀⠀⠀⠀⠀⠀⣿⣿⣿⠀⣿⣿⣿⠀⠈⢿⣿⣿⠄⠀⠀⠄⢊⡡⠜⣦⠀⠀
⠀⢠⡏⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣷⣿⣿⣿⠀⠀⠈⠙⠉⠀⠀⠀⢒⡡⠔⣋⠼⡇⠀
⠀⣼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠿⣿⣿⣿⣿⣿⣷⣶⣄⠀⠀⠀⠀⠀⠐⣈⠤⠒⢻⡄
⢀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣟⠛⢿⣿⣿⣷⠀⠀⠀⠐⣉⠤⠒⣉⠬⣇
⢸⠇⢀⠀⠀⠀⠀⠀⠀⣠⣤⡀⠀⠀⣿⣿⣿⠀⠀⣹⣿⣿⡇⠀⠀⡈⠤⠒⣉⠤⠀⣿
⢸⠀⠘⣆⡀⠀⠀⠀⠀⢿⣿⣿⣄⠀⣿⣿⣿⢀⣴⣿⣿⡿⠀⠀⠀⠤⠒⣉⠤⠒⠀⡿
⢸⡆⢰⡆⠁⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠀⠀⠀⠠⢒⣉⠤⠒⠁⣸⠃
⠀⢳⡀⠙⠒⢷⣀⠀⠀⠀⠀⠈⠛⠻⣿⣿⣿⠛⠉⠀⠀⠀⠀⠐⢊⣁⠤⠒⠋⣠⠏⠀
⠀⠀⠳⣤⣧⡀⠸⡀⠀⠀⠀⠀⠀⠀⠻⣿⠟⠀⠀⠀⠀⠀⠔⣊⡡⠤⠒⢉⡴⠋⠀⠀
⠀⠀⠀⠀⠙⠳⠦⣌⣁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣁⣤⣴⡾⠟⠋⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠒⠒⠶⠦⠤⠤⠤⠴⠶⠒⠒⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀"""
    print(banner)

def get_trade_history(cookie, limit=100):
    headers = {
        "Cookie": f".ROBLOSECURITY={cookie}",
        "Content-Type": "application/json"
    }
    
    trades = []
    cursor = ""
    
    try:
        while len(trades) < limit:
            url = f"https://trades.roblox.com/v1/trades/completed?limit=100&cursor={cursor}"
            response = requests.get(url, headers=headers)
            
            if response.status_code != 200:
                return None, f"API Error: HTTP {response.status_code}"
            
            data = response.json()
            trades.extend(data.get("data", []))
            
            if not data.get("nextPageCursor"):
                break
                
            cursor = data["nextPageCursor"]
        
        return trades[:limit], None
    except Exception as e:
        return None, str(e)

def analyze_trades(trades):
    analysis = {
        "total_trades": len(trades),
        "total_profit": 0,
        "biggest_win": {"value": 0, "trade": None},
        "biggest_loss": {"value": 0, "trade": None},
        "monthly_stats": defaultdict(lambda: {"count": 0, "profit": 0}),
        "trade_partners": defaultdict(int),
        "item_types": defaultdict(int)
    }
    
    for trade in trades:
        # Calculate trade value difference
        offered_value = sum(item.get("rap", 0) for item in trade.get("offers", [{}])[0].get("userAssets", []))
        received_value = sum(item.get("rap", 0) for item in trade.get("offers", [{}])[1].get("userAssets", []))
        profit = received_value - offered_value
        
        # Update analysis
        analysis["total_profit"] += profit
        
        if profit > analysis["biggest_win"]["value"]:
            analysis["biggest_win"] = {"value": profit, "trade": trade}
        elif profit < analysis["biggest_loss"]["value"]:
            analysis["biggest_loss"] = {"value": profit, "trade": trade}
        
        # Monthly stats
        trade_date = datetime.strptime(trade.get("created"), "%Y-%m-%dT%H:%M:%S.%fZ")
        month_key = trade_date.strftime("%Y-%m")
        analysis["monthly_stats"][month_key]["count"] += 1
        analysis["monthly_stats"][month_key]["profit"] += profit
        
        # Trade partners
        partner = trade.get("offers", [{}])[1].get("user", {}).get("name", "Unknown")
        analysis["trade_partners"][partner] += 1
        
        # Item types
        for item in trade.get("offers", [{}])[0].get("userAssets", []):
            analysis["item_types"][item.get("assetType", "Unknown")] += 1
    
    return analysis

def display_analysis(analysis):
    print(f"\n{INFO_ADD} {colors.YELLOW}Trade Summary:{colors.RESET}")
    print(f"    Total Trades: {colors.WHITE}{analysis['total_trades']}{colors.RESET}")
    print(f"    Net Profit: {colors.GREEN if analysis['total_profit'] >= 0 else colors.RED}R$ {analysis['total_profit']:,}{colors.RESET}")
    
    print(f"\n{INFO_ADD} {colors.YELLOW}Best/Worst Trades:{colors.RESET}")
    print(f"    Biggest Win: {colors.GREEN}R$ {analysis['biggest_win']['value']:,}{colors.RESET}")
    print(f"    Biggest Loss: {colors.RED}R$ {analysis['biggest_loss']['value']:,}{colors.RESET}")
    
    print(f"\n{INFO_ADD} {colors.YELLOW}Monthly Stats:{colors.RESET}")
    for month, stats in sorted(analysis["monthly_stats"].items()):
        profit_color = colors.GREEN if stats["profit"] >= 0 else colors.RED
        print(f"    {colors.WHITE}{month}: {stats['count']} trades, {profit_color}R$ {stats['profit']:,}{colors.RESET}")
    
    print(f"\n{INFO_ADD} {colors.YELLOW}Top Trade Partners:{colors.RESET}")
    for partner, count in sorted(analysis["trade_partners"].items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"    {colors.WHITE}• {partner}: {count} trades{colors.RESET}")
    
    print(f"\n{INFO_ADD} {colors.YELLOW}Item Types Traded:{colors.RESET}")
    for item_type, count in sorted(analysis["item_types"].items(), key=lambda x: x[1], reverse=True):
        print(f"    {colors.WHITE}• {item_type}: {count} items{colors.RESET}")

def plot_profit_history(analysis):
    months = []
    profits = []
    
    for month, stats in sorted(analysis["monthly_stats"].items()):
        months.append(month)
        profits.append(stats["profit"])
    
    plt.figure(figsize=(10, 5))
    bars = plt.bar(months, profits, color=['green' if p >=0 else 'red' for p in profits])
    plt.title("Monthly Trade Profit/Loss")
    plt.xlabel("Month")
    plt.ylabel("Profit (R$)")
    plt.xticks(rotation=45)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'R$ {int(height):,}',
                ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.show()

def main():
    display_banner()
    
    while True:
        try:
            cookie = input(f"{INPUT} Enter your .ROBLOSECURITY cookie (or 'exit' to quit) -> {colors.WHITE}")
            
            if cookie.lower() == 'exit':
                print(f"{INFO} Exiting...{colors.RESET}")
                break
                
            print(f"{WAIT} Fetching trade history...{colors.RESET}")
            trades, error = get_trade_history(cookie.strip())
            
            if error:
                print(f"{ERROR} Error: {error}{colors.RESET}")
                continue
                
            if not trades:
                print(f"{ERROR} No trades found or cookie invalid{colors.RESET}")
                continue
                
            print(f"{SUCCESS} Found {len(trades)} trades{colors.RESET}")
            analysis = analyze_trades(trades)
            display_analysis(analysis)
            
            plot_choice = input(f"\n{INPUT} View profit history chart? (y/n) -> {colors.WHITE}")
            if plot_choice.lower() == 'y':
                plot_profit_history(analysis)
            
        except KeyboardInterrupt:
            print(f"\n{INFO} Exiting...{colors.RESET}")
            break
        except Exception as e:
            print(f"{ERROR} An error occurred: {e}{colors.RESET}")

if __name__ == "__main__":
    main()