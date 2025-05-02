import os
import platform
import subprocess
import time
from datetime import datetime
import argparse
import socket

class IPPinger:
    def __init__(self):
        self.clear_screen()
        self.display_banner()
        self.results = []

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if platform.system() == 'Windows' else 'clear')

    def display_banner(self):
        """Display tool banner"""
        banner = r"""
     ____  ____   ____    _   _       _             
    |  _ \|  _ \ / ___|  | | | |_ __ (_)_ __   __ _ 
    | |_) | |_) | |  _   | | | | '_ \| | '_ \ / _` |
    |  __/|  __/| |_| |  | |_| | | | | | | | | (_| |
    |_|   |_|    \____|   \___/|_| |_|_|_| |_|\__, |
                                              |___/ 
                   IP Connectivity Testing Tool
                         Version 1.0
        """
        print(banner)
        print("="*60)
        print(f"Tool started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        print()

    def ping_host(self, host, count=4, timeout=2):
        """
        Ping a host and return True if reachable
        :param host: IP or hostname to ping
        :param count: Number of ping packets to send
        :param timeout: Timeout in seconds for each ping
        :return: Tuple (success, avg_latency)
        """
        try:
            # Resolve hostname to IP if needed
            ip = socket.gethostbyname(host)
            
            # Ping parameters based on OS
            if platform.system().lower() == "windows":
                cmd = ['ping', '-n', str(count), '-w', str(timeout*1000), ip]
            else:
                cmd = ['ping', '-c', str(count), '-W', str(timeout), ip]

            # Execute ping command
            output = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Parse output for success and latency
            if output.returncode == 0:
                if platform.system().lower() == "windows":
                    # Windows output parsing
                    lines = output.stdout.split('\n')
                    for line in lines:
                        if 'Average' in line:
                            latency = line.split('=')[-1].strip().replace('ms', '')
                            return (True, float(latency))
                else:
                    # Linux/Mac output parsing
                    lines = output.stdout.split('\n')
                    for line in lines:
                        if 'min/avg/max' in line:
                            latency = line.split('=')[1].split('/')[1]
                            return (True, float(latency))
                return (True, 0)  # If we can't parse latency, just return success
            return (False, 0)
        except:
            return (False, 0)

    def continuous_ping(self, host, interval=1, max_pings=None):
        """
        Continuously ping a host until stopped
        :param host: IP or hostname to ping
        :param interval: Seconds between pings
        :param max_pings: Maximum number of pings (None for unlimited)
        """
        print(f"\n[*] Starting continuous ping to {host}")
        print("[*] Press Ctrl+C to stop\n")
        print("{:<20} {:<15} {:<10} {:<15}".format(
            "Timestamp", "Host", "Status", "Latency (ms)"
        ))
        print("-"*60)

        count = 0
        try:
            while True:
                if max_pings and count >= max_pings:
                    break

                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                success, latency = self.ping_host(host, count=1)
                status = "UP" if success else "DOWN"
                latency_str = f"{latency:.2f}" if success else "N/A"

                print("{:<20} {:<15} {:<10} {:<15}".format(
                    timestamp, host, status, latency_str
                ))

                self.results.append({
                    'timestamp': timestamp,
                    'host': host,
                    'status': status,
                    'latency': latency_str
                })

                count += 1
                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n[*] Ping stopped by user")
            self.display_stats()

    def display_stats(self):
        """Display ping statistics"""
        if not self.results:
            print("\n[!] No ping results to display")
            return

        total = len(self.results)
        up_count = sum(1 for r in self.results if r['status'] == 'UP')
        down_count = total - up_count
        uptime_percent = (up_count / total) * 100 if total > 0 else 0

        # Calculate average latency for successful pings
        successful_pings = [float(r['latency']) for r in self.results if r['status'] == 'UP']
        avg_latency = sum(successful_pings) / len(successful_pings) if successful_pings else 0

        print("\n[+] Ping Statistics:")
        print("="*60)
        print(f"Total pings: {total}")
        print(f"Successful: {up_count} ({uptime_percent:.2f}%)")
        print(f"Failed: {down_count}")
        print(f"Average latency: {avg_latency:.2f} ms")
        print("="*60)

    def save_results(self, filename):
        """Save ping results to a file"""
        try:
            with open(filename, 'w') as f:
                f.write("Timestamp,Host,Status,Latency(ms)\n")
                for result in self.results:
                    f.write(f"{result['timestamp']},{result['host']},{result['status']},{result['latency']}\n")
            print(f"\n[+] Results saved to {filename}")
        except Exception as e:
            print(f"\n[!] Error saving results: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="IP Pinger Tool")
    parser.add_argument("host", nargs='?', help="Host to ping (IP or hostname)")
    parser.add_argument("-c", "--continuous", action="store_true", help="Continuous ping mode")
    parser.add_argument("-i", "--interval", type=float, default=1, help="Interval between pings in seconds (default: 1)")
    parser.add_argument("-n", "--count", type=int, help="Number of pings to send (default: infinite)")
    parser.add_argument("-s", "--save", help="Save results to CSV file")
    args = parser.parse_args()

    pinger = IPPinger()

    if not args.host:
        print("\n[i] No host specified. Enter host to ping:")
        args.host = input("[?] Host/IP: ").strip()
        if not args.host:
            print("[!] Host is required")
            return

    if args.continuous or args.count:
        pinger.continuous_ping(args.host, args.interval, args.count)
    else:
        # Single ping test
        print(f"\n[*] Pinging {args.host}...")
        success, latency = pinger.ping_host(args.host)
        if success:
            print(f"[+] Host is reachable (latency: {latency:.2f} ms)")
        else:
            print("[!] Host is unreachable")

    if args.save and pinger.results:
        pinger.save_results(args.save)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Operation cancelled by user")
    except Exception as e:
        print(f"\n[!] An error occurred: {str(e)}")