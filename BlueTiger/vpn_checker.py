import requests

def print_banner():
    banner = """
    ****************************************************
    *                VPN Checker Tool                  *
    *                                                  *
    * This tool checks if your connection is routed     *
    * through a VPN by comparing your public IP         *
    * address.                                         *
    ****************************************************
    """
    print(banner)

def get_public_ip():
    """Get the public IP address of the current connection."""
    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()
        ip_data = response.json()
        return ip_data['ip']
    except requests.RequestException as e:
        print(f"Error getting public IP: {e}")
        return None

def is_vpn_active(known_non_vpn_ip):
    """Check if the VPN is active by comparing the current public IP with a known non-VPN IP."""
    current_ip = get_public_ip()
    if current_ip is None:
        return False
    return current_ip != known_non_vpn_ip

def check_vpn_status(known_non_vpn_ip):
    """Check the VPN status and print the result."""
    if is_vpn_active(known_non_vpn_ip):
        print("VPN is active. Your connection is secure.")
    else:
        print("VPN is not active. Your connection is not secure.")

# Example usage
if __name__ == "__main__":
    print_banner()

    # Replace with your known non-VPN IP address
    known_non_vpn_ip = 'your.known.non.vpnip'

    # Check VPN status
    check_vpn_status(known_non_vpn_ip)
