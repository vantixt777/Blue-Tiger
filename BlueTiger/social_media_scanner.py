import requests
import threading
import time
from queue import Queue

BANNER = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⡀⠀⠀⣰⣷⠀⠀⣮⣢⣖⣲⡦⠀⢀⣞⡻⠟⣦⠀⠀⣄⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠟⠅⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⡇⠻⡀⡔⠁⢿⠀⠀⡟⠀⠀⠀⠀⢐⡽⠉⠀⠀⢘⣇⠰⡏⠀⠀⢀⠀⠀⠀⣷⠀⠀⢘⡛⡇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⢿⡇⠀⢿⠀⠀⣿⠿⠻⠿⠀⢘⣫⠀⠀⢀⡼⠕⢘⣇⠀⣐⡿⡄⠀⠀⣭⠀⠀⢘⣗⠂⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⢸⠀⠀⣷⣀⣀⡀⠀⣴⢿⣕⣒⣫⠋⠀⠀⣗⠄⢘⣿⡓⡄⣸⡯⠀⠀⠀⠃⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠿⠀⠀⠀⠀⢈⡂⠈⠙⠋⠛⠋⡮⠋⠉⢟⣎⠀⠀⠀⠀⠈⠛⠛⠀⠉⠛⠋⠁⠀⢀⣔⡱⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠇⠀⠀⠈⢽⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠷⠋⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣞⡏⠉⠙⠷⢆⡀⠀⠀⢀⣀⣦⡧⠭⠝⠿⠵⣷⡏⠀⠀⠀⠀⠀⠿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⡜⣷⠀⠀⠀⠀⠙⣧⡞⡉⠃⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢷⣟⠀⠀⠀⠀⠀⠉⠚⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡄⠀⠀⠀⠀⠀⠈⠻⣦⡀⠀⠀⠀⠀⠀⣀⣠⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠘⣟⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠋⠀⠀⠀⠀⠀⠀⠀⠀⠑⣷⣀⣠⡤⠒⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⣸⡷⠛⠛⠛⠏⠀⠀⠀⠈⠛⢦⣿⣟⡅⠀⠀⡀⣤⡶⠆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡠⣿⡀⠀⣠⡶⠶⠴⣤⣄⠀⠠⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠚⢷⡀⠀⠀⠀⠤⢿⣷⠚⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣷⠃⠀⠘⠛⠀⠀⣀⡼⠿⠃⠀⠀⢻⡆⠀⠀⠀⠀⠀⠀⠀⠀⠈⠃⠀⠀⠀⠀⢠⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢐⡏⠀⠀⠀⠀⠀⣼⠃⠀⠀⠀⠀⠀⠀⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠨⣇⡀⠀⠦⣀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⢔⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣔⠞⣽⣟⠊⠱⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢀⣤⡶⠗⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢀⠾⠉⠀⣀⣙⣷⠤⠤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣬⠒⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠘⠉⠀⠀⣀⠞⠁⠙⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⣤⣠⡶⠞⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⡶⠊⠀⠀⠀⠘⠓⠶⠴⠴⠦⠦⠦⠶⣄⡬⠭⠓⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

PLATFORMS = {
    "Facebook": "https://www.facebook.com/{}",
    "Twitter": "https://twitter.com/{}",
    "Instagram": "https://www.instagram.com/{}",
    "LinkedIn": "https://www.linkedin.com/in/{}",
    "YouTube": "https://www.youtube.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Pinterest": "https://www.pinterest.com/{}",
    "Tumblr": "https://{}.tumblr.com",
    "Flickr": "https://www.flickr.com/people/{}",
    "Vimeo": "https://vimeo.com/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Disqus": "https://disqus.com/{}",
    "Medium": "https://medium.com/@{}",
    "DeviantArt": "https://{}.deviantart.com",
    "VK": "https://vk.com/{}",
    "About.me": "https://about.me/{}",
    "Imgur": "https://imgur.com/user/{}",
    "Flipboard": "https://flipboard.com/@{}",
    "Slideshare": "https://slideshare.net/{}",
    "Spotify": "https://open.spotify.com/user/{}",
    "Scribd": "https://www.scribd.com/{}",
    "Patreon": "https://www.patreon.com/{}",
    "Bitbucket": "https://bitbucket.org/{}",
    "GitHub": "https://github.com/{}",
    "GitLab": "https://gitlab.com/{}",
    "Goodreads": "https://www.goodreads.com/{}",
    "Instructables": "https://www.instructables.com/member/{}",
    "Codecademy": "https://www.codecademy.com/{}",
    "Last.fm": "https://last.fm/user/{}",
    "Dribbble": "https://dribbble.com/{}",
    "Behance": "https://www.behance.net/{}",
    "Foursquare": "https://foursquare.com/{}",
    "Gravatar": "https://en.gravatar.com/{}",
    "Keybase": "https://keybase.io/{}",
    "Kongregate": "https://www.kongregate.com/accounts/{}",
    "LiveJournal": "https://{}.livejournal.com",
    "AngelList": "https://angel.co/{}",
    "Wikipedia": "https://en.wikipedia.org/wiki/User:{}",
    "HackerNews": "https://news.ycombinator.com/user?id={}",
    "Codepen": "https://codepen.io/{}",
    "Pastebin": "https://pastebin.com/u/{}",
    "Roblox": "https://www.roblox.com/user.aspx?username={}",
    "TradingView": "https://www.tradingview.com/u/{}/",
    "Blogger": "https://{}.blogspot.com",
    "WordPress": "https://{}.wordpress.com",
    "Etsy": "https://www.etsy.com/shop/{}",
    "Bandcamp": "https://bandcamp.com/{}",
    "Kickstarter": "https://www.kickstarter.com/profile/{}",
    "Venmo": "https://venmo.com/{}",
    "CashApp": "https://cash.app/${}",
    "PayPal": "https://www.paypal.me/{}",
    "Twitch": "https://www.twitch.tv/{}",
    "Steam": "https://steamcommunity.com/id/{}",
    "ReverbNation": "https://www.reverbnation.com/{}",
    "Basecamp": "https://{}.basecamphq.com",
    "DailyMotion": "https://www.dailymotion.com/{}",
    "HubPages": "https://hubpages.com/@{}",
    "BuzzFeed": "https://www.buzzfeed.com/{}",
    "9GAG": "https://9gag.com/u/{}",
    "Giphy": "https://giphy.com/{}",
    "IFTTT": "https://www.ifttt.com/p/{}",
    "Trakt": "https://www.trakt.tv/users/{}",
    "TripAdvisor": "https://www.tripadvisor.com/members/{}"
}

# Thread-safe Datenstrukturen
found_accounts = []
lock = threading.Lock()
queue = Queue()

def check_url(platform, url, username):
    full_url = url.format(username)
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        
        # Timeout auf 5 Sekunden reduziert (von 10)
        response = requests.get(full_url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            with lock:
                found_accounts.append((platform, full_url))
        # Einige Plattformen geben andere Statuscodes für existierende Profile zurück
        elif response.status_code in [301, 302, 403]:
            with lock:
                found_accounts.append((platform, full_url))
    
    except requests.exceptions.RequestException:
        pass

def worker():
    while True:
        item = queue.get()
        if item is None:
            break
        platform, url, username = item
        check_url(platform, url, username)
        queue.task_done()

def check_username(username, thread_count=20):
    print(f"\n[+] Checking username '{username}' across {len(PLATFORMS)} platforms...\n")
    
    # Thread-Pool erstellen
    threads = []
    for _ in range(thread_count):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)
    
    # Jobs in die Queue geben
    for platform, url in PLATFORMS.items():
        queue.put((platform, url, username))
    
    # Auf Fertigstellung warten
    queue.join()
    
    # Worker threads stoppen
    for _ in range(thread_count):
        queue.put(None)
    for t in threads:
        t.join()
    
    return found_accounts

def print_results(found_accounts):
    if found_accounts:
        print("\n[+] Found accounts:")
        for platform, url in sorted(found_accounts, key=lambda x: x[0]):
            print(f"  • {platform}: {url}")
    else:
        print("\n[-] No accounts found with this username.")

def main():
    print(BANNER)
    print(f"Social Media Account Finder blue tiger😈 (Fast) | Platforms: {len(PLATFORMS)}\n")
    
    import sys
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        username = input("Enter username to search: ").strip()
    
    start_time = time.time()
    found_accounts = check_username(username)
    elapsed_time = time.time() - start_time
    
    print_results(found_accounts)
    print(f"\n[!] Scan completed in {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()