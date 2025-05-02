import requests
import time

def print_banner():
    banner = """
    ****************************************************
    *               Proxy Verifier Tool                *
    *                                                  *
    * This tool checks the validity and performance    *
    * of a list of proxy servers.                     *
    ****************************************************
    """
    print(banner)

def load_proxies(file_path):
    """Load proxies from a file."""
    proxies = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                proxy = line.strip()
                if proxy:
                    proxies.append(proxy)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    return proxies

def check_proxy(proxy):
    """Check if a proxy is working and measure its response time."""
    url = 'http://www.google.com'
    proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}',
    }
    try:
        start_time = time.time()
        response = requests.get(url, proxies=proxies, timeout=5)
        response_time = time.time() - start_time
        if response.status_code == 200:
            return True, response_time
    except requests.RequestException:
        pass
    return False, None

def verify_proxies(proxy_list):
    """Verify a list of proxies and print the results."""
    for proxy in proxy_list:
        is_working, response_time = check_proxy(proxy)
        if is_working:
            print(f"Proxy {proxy} is working. Response time: {response_time:.2f} seconds.")
        else:
            print(f"Proxy {proxy} is not working.")

# Example usage
if __name__ == "__main__":
    print_banner()

    # Path to the file containing the list of proxies
    proxy_file = 'proxies.txt'

    # Load proxies from the file
    proxies = load_proxies(proxy_file)

    # Verify proxies
    verify_proxies(proxies)
