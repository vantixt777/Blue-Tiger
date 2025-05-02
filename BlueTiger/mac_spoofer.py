import subprocess
import re
import optparse

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac, use --help for more info.")
    return options

def change_mac(interface, new_mac):
    print(f"[+] Changing MAC address for {interface} to {new_mac}")
    subprocess.call(["netsh", "interface", "set", "interface", interface, "admin=disable"])
    subprocess.call(["netsh", "interface", "set", "interface", interface, "admin=enable"])
    subprocess.call(["reg", "add", f"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Class\\{{4d36e972-e325-11ce-bfc1-08002be10318}}\\000X", "/v", "NetworkAddress", "/d", new_mac, "/f"])
    subprocess.call(["netsh", "interface", "set", "interface", interface, "admin=disable"])
    subprocess.call(["netsh", "interface", "set", "interface", interface, "admin=enable"])

def get_current_mac(interface):
    result = subprocess.check_output(["getmac", "/v", "/fo", "LIST"])
    mac_address_search_result = re.search(rf"{interface}.*\n\s*Physical Address:\s*(\S+)", result.decode())
    if mac_address_search_result:
        return mac_address_search_result.group(1)
    else:
        print("[-] Could not read MAC address.")

options = get_arguments()

current_mac = get_current_mac(options.interface)
print(f"Current MAC = {str(current_mac)}")

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print(f"[+] MAC address was successfully changed to {current_mac}")
else:
    print("[-] MAC address did not get changed.")
