import time
import random
from fake_useragent import UserAgent

class AniworldChecker:
    def __init__(self):
        self.ua = UserAgent()
        self.version = "1.1"
        
        self.banner = f"""
   ▄████████ ███▄▄▄▄    ▄█   ▄█     █▄   ▄██████▄     ▄████████  ▄█       ████████▄  
  ███    ███ ███▀▀▀██▄ ███  ███     ███ ███    ███   ███    ███ ███       ███   ▀███ 
  ███    ███ ███   ███ ███▌ ███     ███ ███    ███   ███    ███ ███       ███    ███ 
  ███    ███ ███   ███ ███▌ ███     ███ ███    ███  ▄███▄▄▄▄██▀ ███       ███    ███ 
▀███████████ ███   ███ ███▌ ███     ███ ███    ███ ▀▀███▀▀▀▀▀   ███       ███    ███ 
  ███    ███ ███   ███ ███  ███     ███ ███    ███ ▀███████████ ███       ███    ███                aniworld account checker by vantixt
  ███    ███ ███   ███ ███  ███ ▄█▄ ███ ███    ███   ███    ███ ███▌    ▄ ███   ▄███ 
  ███    █▀   ▀█   █▀  █▀    ▀███▀███▀   ▀██████▀    ███    ███ █████▄▄██ ████████▀  
                                                     ███    ███ ▀                     """
        
    def clear_screen(self):
        print("\n" * 50)
        
    def show_menu(self):
        while True:
            self.clear_screen()
            print(self.banner)
            print("╔══════════════════════════════╗")
            print("║         MAIN MENU            ║")
            print("╠══════════════════════════════╣")
            print("║ 1. Check Single Account      ║")
            print("║ 2. Check Multiple Accounts   ║")
            print("║ 3. Settings                  ║")
            print("║ 4. Help & Information        ║")
            print("║ 5. Exit                      ║")
            print("╚══════════════════════════════╝")
            
            choice = input("\nSelect option (1-5): ")
            
            if choice == "1":
                self.check_single_account()
            elif choice == "2":
                self.check_multiple_accounts()
            elif choice == "3":
                self.show_settings()
            elif choice == "4":
                self.show_help()
            elif choice == "5":
                print("\n[+] Thank you for using the Aniworld Checker!")
                break
            else:
                print("\n[!] Invalid choice. Please select 1-5")
                time.sleep(1)
        
    def check_single_account(self):
        self.clear_screen()
        print("╔══════════════════════════════╗")
        print("║     SINGLE ACCOUNT CHECK     ║")
        print("╚══════════════════════════════╝")
        
        username = input("\nEnter username: ").strip()
        if not username:
            print("\n[!] Please enter a username!")
            time.sleep(1.5)
            return
            
        print(f"\n[~] Checking account '{username}'...")
        time.sleep(2)  # Simulation
        
        # Generate random demo response
        exists = random.choice([True, False, True])  # 66% chance exists
        
        if exists:
            join_date = f"202{random.randint(1,3)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
            last_online = f"{random.randint(1,30)} days ago"
            print("\n[+] Account exists!")
            print("╔══════════════════════════════╗")
            print(f"║ Username: {username.ljust(16)} ║")
            print(f"║ Joined: {join_date.ljust(18)} ║")
            print(f"║ Last Active: {last_online.ljust(12)} ║")
            print("╚══════════════════════════════╝")
            
            # Simulate additional random data
            if random.choice([True, False]):
                print(f" ╠═► Status: {'Premium' if random.choice([True, False]) else 'Free'}")
            if random.choice([True, False]):
                print(f" ╠═► Watched: {random.randint(10,500)} shows")
            if random.choice([True, False]):
                print(f" ╚═► Favorites: {random.randint(0,50)}")
        else:
            print(f"\n[-] Account '{username}' doesn't exist")
            
        input("\nPress Enter to continue...")
        
    def check_multiple_accounts(self):
        self.clear_screen()
        print("╔══════════════════════════════╗")
        print("║    MULTIPLE ACCOUNT CHECK    ║")
        print("╚══════════════════════════════╝")
        
        print("\nEnter usernames (separated by spaces or commas):")
        usernames = [u.strip() for u in input("> ").replace(",", " ").split() if u.strip()]
        
        if not usernames:
            print("\n[!] No usernames entered!")
            time.sleep(1.5)
            return
            
        print(f"\n[~] Checking {len(usernames)} accounts...")
        time.sleep(1)
        
        print("\n╔══════════════════════════════╗")
        print("║        CHECK RESULTS        ║")
        print("╠══════════════════════════════╣")
        
        for username in usernames:
            exists = random.choice([True, False, True])  # Weighted random
            status = "EXISTS" if exists else "NOT FOUND"
            color = "\033[92m" if exists else "\033[91m"
            print(f"║ {username.ljust(20)} {color}{status}\033[0m ║")
        
        print("╚══════════════════════════════╝")
        print(f"\nFound {sum(1 for _ in usernames if random.choice([True, False]))}/{len(usernames)} accounts")
        input("\nPress Enter to continue...")
        
    def show_settings(self):
        self.clear_screen()
        print("╔══════════════════════════════╗")
        print("║          SETTINGS            ║")
        print("╚══════════════════════════════╝")
        print("\nThis is just a simulation tool")
        print("No actual settings available")
        input("\nPress Enter to continue...")
        
    def show_help(self):
        self.clear_screen()
        print("╔══════════════════════════════╗")
        print("║       HELP & INFORMATION     ║")
        print("╚══════════════════════════════╝")
        print("\nThis is a DEMO VERSION only")
        print("It simulates account checking without")
        print("actually connecting to any service")
        print("\nOptions:")
        print("1. Single Check - Verify one account")
        print("2. Multi Check - Verify several accounts")
        print("3. Settings - Demo configuration")
        print("4. Help - This information")
        print("5. Exit - Close the program")
        input("\nPress Enter to continue...")

# Run the program
if __name__ == "__main__":
    try:
        checker = AniworldChecker()
        checker.show_menu()
    except KeyboardInterrupt:
        print("\n[!] Program closed by user")