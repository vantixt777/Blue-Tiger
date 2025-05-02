import dns.resolver
import dns.message
import dns.query
import argparse
import socket
import time
from collections import defaultdict

BANNER = """
██████╗ ███╗   ██╗███████╗    ███████╗██████╗  ██████╗  ██████╗ ███████╗
██╔══██╗████╗  ██║██╔════╝    ██╔════╝██╔══██╗██╔═══██╗██╔═══██╗██╔════╝
██║  ██║██╔██╗ ██║███████╗    ███████╗██████╔╝██║   ██║██║   ██║█████╗  
██║  ██║██║╚██╗██║╚════██║    ╚════██║██╔═══╝ ██║   ██║██║   ██║██╔══╝  
██████╔╝██║ ╚████║███████║    ███████║██║     ╚██████╔╝╚██████╔╝██║     
╚═════╝ ╚═╝  ╚═══╝╚══════╝    ╚══════╝╚═╝      ╚═════╝  ╚═════╝ ╚═╝                    blue tiger 😈
                                                                         
██████╗ ███████╗████████╗██████╗ ███████╗ ██████╗████████╗ ██████╗ ██████╗ 
██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
██║  ██║█████╗     ██║   ██████╔╝█████╗  ██║        ██║   ██║   ██║██████╔╝
██║  ██║██╔══╝     ██║   ██╔═══╝ ██╔══╝  ██║        ██║   ██║   ██║██╔══██╗
██████╔╝███████╗   ██║   ██║     ███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║
╚═════╝ ╚══════╝   ╚═╝   ╚═╝     ╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
"""

print(BANNER)
print("DNS Spoofing Detector Tool - For detecting DNS cache poisoning and spoofing attacks")
print("="*90)
print("DISCLAIMER: Use only for legitimate network monitoring and security testing.\n")

class DNSSpoofDetector:
    def __init__(self):
        self.trusted_dns_servers = [
            '8.8.8.8',        # Google DNS
            '1.1.1.1',        # Cloudflare DNS
            '9.9.9.9',        # Quad9 DNS
            '208.67.222.222'  # OpenDNS
        ]
        self.local_dns_server = None
        self.results = defaultdict(list)
        self.test_domains = [
            'google.com',
            'facebook.com',
            'amazon.com',
            'microsoft.com',
            'youtube.com'
        ]
        self.detected_anomalies = 0

    def get_local_dns(self):
        """Get the local DNS server from system configuration"""
        try:
            with open('/etc/resolv.conf', 'r') as f:
                for line in f:
                    if line.startswith('nameserver'):
                        self.local_dns_server = line.split()[1]
                        print(f"[*] Detected local DNS server: {self.local_dns_server}")
                        return
        except:
            pass
        
        try:
            # Fallback method for Windows
            import subprocess
            output = subprocess.check_output(['ipconfig', '/all']).decode('utf-8')
            for line in output.split('\n'):
                if 'DNS Servers' in line:
                    self.local_dns_server = line.split(':')[-1].strip()
                    print(f"[*] Detected local DNS server: {self.local_dns_server}")
                    return
        except:
            pass
        
        print("[!] Could not detect local DNS server automatically")
        self.local_dns_server = input("Please enter your local DNS server IP: ").strip()

    def query_dns(self, server, domain, record_type='A'):
        """Query a DNS server for a specific record"""
        try:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [server]
            resolver.lifetime = 2  # Timeout in seconds
            answers = resolver.resolve(domain, record_type)
            return sorted([str(r) for r in answers])
        except Exception as e:
            print(f"[-] Error querying {server} for {domain}: {str(e)}")
            return None

    def check_for_spoofing(self, domain):
        """Check for DNS spoofing on a specific domain"""
        print(f"\n[*] Testing domain: {domain}")
        
        # Get responses from trusted DNS servers
        trusted_responses = []
        for server in self.trusted_dns_servers:
            response = self.query_dns(server, domain)
            if response:
                trusted_responses.append(response)
                print(f"[+] {server} response: {response}")
            time.sleep(0.5)  # Rate limiting
        
        if not trusted_responses:
            print("[-] Could not get responses from trusted servers")
            return
        
        # Get most common trusted response (consensus)
        consensus = max(set(tuple(r) for r in trusted_responses), 
                       key=lambda x: trusted_responses.count(list(x)))
        
        # Get local DNS response
        local_response = self.query_dns(self.local_dns_server, domain)
        if not local_response:
            print("[-] Could not get response from local DNS server")
            return
        
        print(f"[+] Local DNS ({self.local_dns_server}) response: {local_response}")
        
        # Compare responses
        if tuple(local_response) != consensus:
            print("[!] POTENTIAL DNS SPOOFING DETECTED!")
            print(f"    Expected: {list(consensus)}")
            print(f"    Received: {local_response}")
            self.detected_anomalies += 1
            self.results[domain].append({
                'expected': list(consensus),
                'received': local_response,
                'server': self.local_dns_server
            })
        else:
            print("[+] No spoofing detected for this domain")

    def run_tests(self):
        """Run DNS spoofing tests on all test domains"""
        self.get_local_dns()
        
        print("\n[*] Starting DNS spoofing detection tests...")
        for domain in self.test_domains:
            self.check_for_spoofing(domain)
            time.sleep(1)  # Rate limiting
        
        self.print_summary()

    def print_summary(self):
        """Print summary of test results"""
        print("\n[+] Test Summary:")
        print("="*50)
        print(f"Total domains tested: {len(self.test_domains)}")
        print(f"Potential spoofing cases detected: {self.detected_anomalies}")
        
        if self.detected_anomalies:
            print("\n[!] Details of potential spoofing cases:")
            for domain, anomalies in self.results.items():
                for anomaly in anomalies:
                    print(f"\nDomain: {domain}")
                    print(f"DNS Server: {anomaly['server']}")
                    print(f"Expected IPs: {', '.join(anomaly['expected'])}")
                    print(f"Received IPs: {', '.join(anomaly['received'])}")
        
        print("\n[+] Recommendations:")
        if self.detected_anomalies:
            print("- Your DNS responses appear to be manipulated")
            print("- Consider using a trusted DNS service like Google (8.8.8.8) or Cloudflare (1.1.1.1)")
            print("- Check your network for possible MITM attacks")
            print("- Use DNS-over-HTTPS or DNS-over-TLS for secure DNS resolution")
        else:
            print("- No DNS spoofing detected in your network")
            print("- For maximum security, consider using encrypted DNS protocols")

def main():
    parser = argparse.ArgumentParser(description='DNS Spoofing Detector Tool')
    parser.add_argument('-d', '--domain', help='Test a specific domain')
    parser.add_argument('-s', '--server', help='Specify a DNS server to test')
    
    args = parser.parse_args()
    
    detector = DNSSpoofDetector()
    
    if args.server:
        detector.local_dns_server = args.server
    
    if args.domain:
        if not detector.local_dns_server:
            detector.get_local_dns()
        detector.check_for_spoofing(args.domain)
        detector.print_summary()
    else:
        detector.run_tests()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
    except Exception as e:
        print(f"\n[!] An error occurred: {str(e)}")