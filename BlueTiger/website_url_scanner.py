import requests
from colorama import Fore, Style, init
from urllib.parse import urlparse, urlunparse
import socket

# Initialize colorama
init(autoreset=True)

blue = Fore.BLUE
white = Fore.WHITE
red = Fore.RED
green = Fore.GREEN

def banner():
    return f"""{blue}
⢀⣴⣶⠛⠋⠉⠉⠉⠉⠉⠙⠛⠒⠒⠒⠒⠒⠒⠒⠀⠠⠤⠤⠤⠤⠤⠤⠤⠤⠤⢤⣤⣄⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣼⢻⡇⠀⠀⢀⣠⡤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⣄⣀⣀⣀⣀⣀⣀⣀⣀⣈⠉⠉⠳⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣇⢸⡇⠀⠀⣾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠻⣆⠀⢸⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⠸⣧⠀⠀⢹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠐⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⠀⣿⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡇⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠸⡄⢸⡄⠀⠀⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣷⠀⢻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⡇⠀⡇⠀⠀⢿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣷⠀⢷⠀⠀⠸⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡄⠘⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢻⠀⢸⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡇⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢸⡇⠸⡄⠀⠀⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⡇⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠈⣿⠀⣇⠀⠀⢹⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣿⡀⢹⠀⠀⠘⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢷⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠉⡇⠸⡄⠀⠀⢹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠆⢸⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢧⠀⣷⠀⠀⢸⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡤⠴⠞⠋⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢸⠀⢹⡀⠀⠈⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⠤⠴⠒⠛⠉⠁⢀⣀⣠⣤⣶⣾⣿⣶⠶⠤⣤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠘⡆⠈⣇⠀⠀⢧⡀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⠤⠴⠒⠚⠋⠉⠉⢀⣀⣠⣤⣴⣺⣿⣿⣿⣿⣿⣿⣟⣿⣽⢷⡲⢦⣬⣉⡙⠒⠶⠦⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢧⠀⢹⡀⠀⠘⢷⣤⠤⠤⠤⠖⠒⠚⠋⠉⠁⠀⠀⣀⣀⡤⠴⠖⢚⣯⡫⠼⣿⣿⣽⢿⣿⣿⣭⠼⣿⡛⢛⣦⣬⣟⠛⣿⣭⡽⠓⣶⣤⡀⠈⠉⠓⠲⠤⣤⣀⡀⠀⠀⠀
⠀⠀⠀⠀⢸⡀⠈⣇⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⡤⠤⠖⠻⢋⣁⣈⣤⣶⣾⣯⡿⠟⢿⣉⣠⣿⠛⠋⠹⣧⡠⣾⣿⣻⣷⠴⠟⢿⣅⣠⣿⣾⡿⠟⠁⠀⠀⠀⠀⠀⠀⠈⠉⠓⠲⣤
⠀⠀⠀⠀⠈⣧⠀⢹⡆⣀⣀⡤⠤⠖⠛⠋⠁⠁⣀⣠⣤⢖⢻⣿⣥⣴⡛⢉⣹⡷⠶⠿⣍⣀⣨⠷⠞⢻⣅⡠⠼⠟⠉⣹⣦⣴⣿⡿⠟⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠚
⠀⠀⠀⠀⠀⠸⠷⢾⢿⡍⠀⠀⠀⣀⡤⠴⢾⣏⣁⣤⢿⠛⣿⣥⠤⢾⡛⠉⣙⣦⠤⢶⣏⢉⣨⡷⠖⠛⢁⣠⡤⢾⣿⣿⣿⣿⡿⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡴⠟⠁⠀⣠
⠀⠀⠀⠀⠀⠀⢠⣟⡀⠙⢦⡀⠀⠙⢶⡞⢻⣍⣠⡽⠟⠛⠛⢦⣄⣤⠟⠛⠻⣄⣠⠴⠛⠉⢀⣀⣤⣞⣏⡥⣞⣻⡿⠛⠋⠀⠀⠀⠙⠦⡄⠀⠀⠀⠀⢀⣠⠴⠛⠁⠀⣀⡴⠚⠁
⠀⠀⠀⠀⠀⠀⠀⠻⣧⡀⠀⠙⢦⡀⠈⠙⢿⡇⠈⣳⣦⠴⠾⣝⢁⣨⠷⠖⠋⢧⣀⣠⠴⢺⣭⡼⠟⣫⡥⠞⠋⠁⠀⠀⠀⠀⠀⠀⢀⡴⠇⠀⢀⡠⠖⠉⠀⠀⣠⠴⠚⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⣄⠀⠀⠙⢦⡀⠀⠙⢯⡁⣀⡠⣶⠋⠉⠈⣳⡤⣶⣫⣭⡴⠖⠉⢱⡶⠊⠉⠀⠀⠀⠀⠀⠀⠀⢀⡤⠞⠋⣀⡤⠞⠉⠀⢀⣠⠶⠋⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⣄⠀⠀⠙⢦⡀⠀⠙⢧⣀⣹⣷⣶⣿⡿⠿⠟⠉⠁⠀⠀⠀⠈⠻⣄⠀⠀⠀⠀⠀⣀⡴⠚⠁⣠⠴⠛⠁⠀⣀⡴⠞⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⣄⠀⠀⠙⠦⣀⠀⠉⠙⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⢤⣤⠖⠋⢁⡤⠞⠋⠁⢀⣠⠴⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢦⡀⠀⠈⠲⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠴⠚⠉⠀⢀⣤⠖⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⣀⠀⠈⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡴⠚⠋⠀⢀⣠⡴⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⣄⡀⠈⠛⢦⡀⠀⠀⠀⢀⣠⠴⠚⠉⠁⠀⣠⡤⠖⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠦⣀⠀⠙⠓⠒⠛⠉⠀⠀⣀⡤⠖⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⢤⣄⣀⣤⠤⠖⠚⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Style.RESET_ALL}
"""

def ensure_scheme(url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = f"http://{url}"
    return url

def is_valid_domain(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except socket.error:
        return False

def scan_urls(base_url, paths):
    print(f"{blue}Scanning URLs on {base_url}...{Style.RESET_ALL}")
    for path in paths:
        full_url = f"{base_url}{path}"
        try:
            response = requests.get(full_url)
            if response.status_code == 200:
                print(f"{green}[+] {full_url} - {response.status_code}{Style.RESET_ALL}")
            else:
                print(f"{red}[-] {full_url} - {response.status_code}{Style.RESET_ALL}")
        except requests.exceptions.RequestException as e:
            print(f"{red}[!] Error scanning {full_url}: {e}{Style.RESET_ALL}")

def main():
    print(banner())
    base_url = input(f"{white}Enter base URL (e.g., example.com): ")
    base_url = ensure_scheme(base_url)

    # Extract domain to check if it's valid
    parsed_url = urlparse(base_url)
    domain = parsed_url.netloc

    if not is_valid_domain(domain):
        print(f"{red}Error: The domain '{domain}' could not be resolved. Please check the URL and try again.{Style.RESET_ALL}")
        return

    if not base_url.endswith('/'):
        base_url += '/'

    paths = [
        "/admin",
        "/login",
        "/dashboard",
        "/panel",
        "/config",
        "/backup",
        "/test",
        "/debug",
        "/.git",
        "/robots.txt"
    ]

    scan_urls(base_url, paths)

if __name__ == "__main__":
    main()
