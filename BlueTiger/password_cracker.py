import hashlib
import itertools
import time
import zipfile
from threading import Thread
import queue

BANNER = """
██████╗  █████╗ ███████╗███████╗██╗    ██╗ ██████╗ ██████╗ ██████╗ 
██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔═══██╗██╔══██╗██╔══██╗
██████╔╝███████║███████╗███████╗██║ █╗ ██║██║   ██║██████╔╝██║  ██║
██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║   ██║██╔══██╗██║  ██║
██║     ██║  ██║███████║███████║╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ 
                                                                    
 ██████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗                       by vantixt meow
██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗           
██║     ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝           
██║     ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗           
╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║           
 ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝           
"""

print(BANNER)
print("Password Cracker Tool - For educational purposes only\n")
print("DISCLAIMER: Use only on systems you own or have permission to test.\n")

class PasswordCracker:
    def __init__(self):
        self.found = False
        self.start_time = time.time()
        self.attempts = 0
        self.hash_type = ""
        self.hash_func = None

    def detect_hash(self, hash_str):
        """Try to detect hash type based on length and character set"""
        hash_length = len(hash_str)
        
        if hash_length == 32 and all(c in "0123456789abcdef" for c in hash_str):
            return "md5", hashlib.md5
        elif hash_length == 40 and all(c in "0123456789abcdef" for c in hash_str):
            return "sha1", hashlib.sha1
        elif hash_length == 64 and all(c in "0123456789abcdef" for c in hash_str):
            return "sha256", hashlib.sha256
        elif hash_length == 128 and all(c in "0123456789abcdef" for c in hash_str):
            return "sha512", hashlib.sha512
        else:
            return "unknown", None

    def crack_hash(self, hash_str, wordlist=None, max_length=6):
        """Crack a hash using brute force or wordlist"""
        self.hash_type, self.hash_func = self.detect_hash(hash_str.lower())
        
        if self.hash_type == "unknown":
            print("[-] Could not determine hash type")
            return None
            
        print(f"[*] Detected hash type: {self.hash_type.upper()}")
        print(f"[*] Starting cracking process...\n")
        
        if wordlist:
            self._crack_with_wordlist(hash_str, wordlist)
        else:
            self._brute_force(hash_str, max_length)
            
        if not self.found:
            print("\n[-] Password not found")
            
        elapsed = time.time() - self.start_time
        print(f"\n[+] Attempted {self.attempts} passwords in {elapsed:.2f} seconds")
        print(f"[+] Speed: {self.attempts/elapsed:.2f} attempts per second")

    def _crack_with_wordlist(self, hash_str, wordlist):
        """Try passwords from a wordlist file"""
        try:
            with open(wordlist, 'r', errors='ignore') as f:
                for line in f:
                    password = line.strip()
                    self.attempts += 1
                    
                    if self.attempts % 1000 == 0:
                        print(f"\r[*] Attempts: {self.attempts}", end="")
                    
                    hashed = self.hash_func(password.encode()).hexdigest()
                    if hashed == hash_str.lower():
                        self.found = True
                        print(f"\n\n[+] Password found: {password}")
                        return
        except FileNotFoundError:
            print(f"[-] Wordlist file '{wordlist}' not found")
            return

    def _brute_force(self, hash_str, max_length):
        """Brute force with given max length"""
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
        
        for length in range(1, max_length + 1):
            print(f"[*] Trying length {length}...")
            for attempt in itertools.product(chars, repeat=length):
                password = ''.join(attempt)
                self.attempts += 1
                
                if self.attempts % 10000 == 0:
                    print(f"\r[*] Attempts: {self.attempts}", end="")
                
                hashed = self.hash_func(password.encode()).hexdigest()
                if hashed == hash_str.lower():
                    self.found = True
                    print(f"\n\n[+] Password found: {password}")
                    return

    def crack_zip(self, zip_file, wordlist=None, max_length=6):
        """Attempt to crack a password-protected ZIP file"""
        print(f"[*] Attempting to crack ZIP file: {zip_file}")
        
        if not wordlist:
            print("[*] Using brute force method (slower)")
            self._brute_force_zip(zip_file, max_length)
        else:
            print("[*] Using wordlist method")
            self._wordlist_zip(zip_file, wordlist)
            
        if not self.found:
            print("\n[-] Password not found")
            
        elapsed = time.time() - self.start_time
        print(f"\n[+] Attempted {self.attempts} passwords in {elapsed:.2f} seconds")

    def _wordlist_zip(self, zip_file, wordlist):
        """Try passwords from wordlist against ZIP"""
        try:
            with zipfile.ZipFile(zip_file) as zf, open(wordlist, 'r', errors='ignore') as f:
                for line in f:
                    password = line.strip()
                    self.attempts += 1
                    
                    if self.attempts % 100 == 0:
                        print(f"\r[*] Attempts: {self.attempts}", end="")
                    
                    try:
                        zf.extractall(pwd=password.encode())
                        self.found = True
                        print(f"\n\n[+] Password found: {password}")
                        return
                    except (RuntimeError, zipfile.BadZipFile):
                        continue
        except FileNotFoundError:
            print(f"[-] Wordlist file '{wordlist}' not found")
            return

    def _brute_force_zip(self, zip_file, max_length):
        """Brute force ZIP password"""
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        
        try:
            zf = zipfile.ZipFile(zip_file)
        except FileNotFoundError:
            print(f"[-] ZIP file '{zip_file}' not found")
            return
            
        for length in range(1, max_length + 1):
            print(f"[*] Trying length {length}...")
            for attempt in itertools.product(chars, repeat=length):
                password = ''.join(attempt)
                self.attempts += 1
                
                if self.attempts % 1000 == 0:
                    print(f"\r[*] Attempts: {self.attempts}", end="")
                
                try:
                    zf.extractall(pwd=password.encode())
                    self.found = True
                    print(f"\n\n[+] Password found: {password}")
                    return
                except (RuntimeError, zipfile.BadZipFile):
                    continue

def main():
    cracker = PasswordCracker()
    
    print("1. Crack a hash")
    print("2. Crack a ZIP file")
    choice = input("\nSelect an option (1-2): ")
    
    if choice == "1":
        hash_str = input("Enter the hash: ").strip()
        wordlist = input("Enter path to wordlist (leave blank for brute force): ").strip()
        
        if wordlist:
            cracker.crack_hash(hash_str, wordlist)
        else:
            max_len = int(input("Enter maximum password length for brute force (default 6): ") or "6")
            cracker.crack_hash(hash_str, max_length=max_len)
            
    elif choice == "2":
        zip_file = input("Enter path to ZIP file: ").strip()
        wordlist = input("Enter path to wordlist (leave blank for brute force): ").strip()
        
        if wordlist:
            cracker.crack_zip(zip_file, wordlist)
        else:
            max_len = int(input("Enter maximum password length for brute force (default 6): ") or "6")
            cracker.crack_zip(zip_file, max_length=max_len)
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()