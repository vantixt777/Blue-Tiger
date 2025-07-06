import dns.resolver
import socket
import sys

def create_banner():
    banner = r"""
     __________∩___
/__\____________\
|門 |         田  田   |
|__ ⚘ ⚘__Π _⚘⚘__ |
    """
    print(f"\033[94m{banner}\033[0m")
    print(f"\033[92mBaka meow vantixt\033[0m")
    print("-" * 30)

def dns_lookup(hostname):
    try:
        resolver = dns.resolver.Resolver()
       
        a_records = resolver.resolve(hostname, 'A')
        print(f"\n\033[92mA-Records für {hostname}:\033[0m")
        for record in a_records:
            print(f"- {record.address}")

       
        try:
            aaaa_records = resolver.resolve(hostname, 'AAAA')
            print(f"\n\033[92mAAAA-Records für {hostname}:\033[0m")
            for record in aaaa_records:
                print(f"- {record.address}")
        except dns.resolver.NoAnswer:
            print(f"\n\033[93mKeine AAAA-Records für {hostname} gefunden.\033[0m")
        except dns.resolver.NXDOMAIN:
            print(f"\n\033[91mHostname {hostname} existiert nicht.\033[0m")
            return

        
        try:
            mx_records = resolver.resolve(hostname, 'MX')
            print(f"\n\033[92mMX-Records für {hostname}:\033[0m")
            for record in mx_records.order:
                print(f"- Präferenz: {record.preference}, Mailserver: {record.exchange}")
        except dns.resolver.NoAnswer:
            print(f"\n\033[93mKeine MX-Records für {hostname} gefunden.\033[0m")

        
        try:
            ns_records = resolver.resolve(hostname, 'NS')
            print(f"\n\033[92mNS-Records für {hostname}:\033[0m")
            for record in ns_records:
                print(f"- {record.host}")
        except dns.resolver.NoAnswer:
            print(f"\n\033[93mKeine NS-Records für {hostname} gefunden.\033[0m")

     
        try:
            cname_records = resolver.resolve(hostname, 'CNAME')
            print(f"\n\033[92mCNAME-Records für {hostname}:\033[0m")
            for record in cname_records:
                print(f"- Alias: {record.target}")
        except dns.resolver.NoAnswer:
            print(f"\n\033[93mKeine CNAME-Records für {hostname} gefunden.\033[0m")

        
        try:
            txt_records = resolver.resolve(hostname, 'TXT')
            print(f"\n\033[92mTXT-Records für {hostname}:\033[0m")
            for record in txt_records:
                print(f"- {' '.join(record.strings)}")
        except dns.resolver.NoAnswer:
            print(f"\n\033[93mKeine TXT-Records für {hostname} gefunden.\033[0m")

    except dns.resolver.NXDOMAIN:
        print(f"\n\033[91mHostname {hostname} existiert nicht.\033[0m")
    except dns.resolver.Timeout:
        print(f"\n\033[91mZeitüberschreitung bei der DNS-Abfrage für {hostname}.\033[0m")
    except socket.gaierror:
        print(f"\n\033[91mUngültiger Hostname: {hostname}.\033[0m")
    except Exception as e:
        print(f"\n\033[91mEin Fehler ist aufgetreten: {e}\033[0m")

if __name__ == "__main__":
    create_banner()
    if len(sys.argv) != 2:
        hostname = input("Bitte geben Sie den Hostnamen ein: ")
    else:
        hostname = sys.argv[1]

    dns_lookup(hostname)
