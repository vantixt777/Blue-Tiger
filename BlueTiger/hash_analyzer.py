import hashlib
import re
import argparse
from datetime import datetime

BANNER = """
██╗  ██╗ █████╗ ███████╗██╗  ██╗    █████╗ ███╗   ██╗ █████╗ ██╗  ██╗███████╗██████╗ 
██║  ██║██╔══██╗██╔════╝██║  ██║   ██╔══██╗████╗  ██║██╔══██╗██║  ██║██╔════╝██╔══██╗
███████║███████║███████╗███████║   ███████║██╔██╗ ██║███████║███████║█████╗  ██████╔╝
██╔══██║██╔══██║╚════██║██╔══██║   ██╔══██║██║╚██╗██║██╔══██║██╔══██║██╔══╝  ██╔══██╗              vantixt meow
██║  ██║██║  ██║███████║██║  ██║   ██║  ██║██║ ╚████║██║  ██║██║  ██║███████╗██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
"""

print(BANNER)
print("Hash Analyzer Tool - Identify and analyze hash types")
print("="*60 + "\n")

class HashAnalyzer:
    def __init__(self):
        self.hash_patterns = {
            'MD5': r'^[a-f0-9]{32}$',
            'SHA-1': r'^[a-f0-9]{40}$',
            'SHA-256': r'^[a-f0-9]{64}$',
            'SHA-384': r'^[a-f0-9]{96}$',
            'SHA-512': r'^[a-f0-9]{128}$',
            'CRC32': r'^[a-f0-9]{8}$',
            'MySQL5': r'^\*[a-f0-9]{40}$',
            'NTLM': r'^[a-f0-9]{32}$',
            'LM': r'^[a-f0-9]{32}$',
            'bcrypt': r'^\$2[aby]\$\d+\$[./A-Za-z0-9]{53}$',
            'Unix Crypt': r'^(?:[./0-9A-Za-z]{13}|\$[156]\$.{56}|\$[156]\$[./0-9A-Za-z]{8}\$[./0-9A-Za-z]{22})$',
            'JWT': r'^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]*$'
        }
        
        self.hash_examples = {
            'MD5': '5d41402abc4b2a76b9719d911017c592',
            'SHA-1': 'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d',
            'SHA-256': '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824',
            'SHA-384': '59e1748777448c69de6b800d7a33bbfb9ff1b463e44354c3553bcdb9c666fa90125a3c79f90397bdf5f6a13de828684f',
            'SHA-512': '9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca72323c3d99ba5c11d7c7acc6e14b8c5da0c4663475c2e5c3adef46f73bcdec043',
            'CRC32': 'd87f7e0c',
            'MySQL5': '*2470C0C06DEE42FD1618BB99005ADCA2EC9D1E19',
            'NTLM': 'AAD3B435B51404EEAAD3B435B51404EE',
            'LM': '299BD128C1101FD6',
            'bcrypt': '$2a$12$R9h/cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jWMUW',
            'Unix Crypt': '$1$salt$UCIYJOYLyN8wdNh3gXQMN0',
            'JWT': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
        }

    def identify_hash(self, hash_str):
        """Identify the type of hash"""
        hash_str = hash_str.strip()
        results = []
        
        for hash_type, pattern in self.hash_patterns.items():
            if re.match(pattern, hash_str, re.IGNORECASE):
                results.append(hash_type)
        
        return results if results else ["Unknown hash type"]

    def get_hash_info(self, hash_type):
        """Get information about a specific hash type"""
        info = {
            'MD5': {
                'description': 'Message Digest Algorithm 5',
                'bits': 128,
                'collisions': 'Vulnerable to collisions',
                'security': 'Considered cryptographically broken',
                'common_uses': 'File integrity checks, checksums'
            },
            'SHA-1': {
                'description': 'Secure Hash Algorithm 1',
                'bits': 160,
                'collisions': 'Vulnerable to collisions',
                'security': 'Considered cryptographically broken',
                'common_uses': 'Git commit hashes, some TLS certificates'
            },
            'SHA-256': {
                'description': 'Secure Hash Algorithm 256-bit',
                'bits': 256,
                'collisions': 'No practical collisions found',
                'security': 'Considered secure',
                'common_uses': 'Blockchain, password hashing, digital signatures'
            },
            'SHA-384': {
                'description': 'Secure Hash Algorithm 384-bit',
                'bits': 384,
                'collisions': 'No practical collisions found',
                'security': 'Considered secure',
                'common_uses': 'High-security applications'
            },
            'SHA-512': {
                'description': 'Secure Hash Algorithm 512-bit',
                'bits': 512,
                'collisions': 'No practical collisions found',
                'security': 'Considered secure',
                'common_uses': 'High-security applications, password hashing'
            },
            'CRC32': {
                'description': 'Cyclic Redundancy Check 32-bit',
                'bits': 32,
                'collisions': 'Very vulnerable to collisions',
                'security': 'Not cryptographic - for error detection only',
                'common_uses': 'Network protocols, file integrity checks'
            },
            'MySQL5': {
                'description': 'MySQL 5.x password hash',
                'bits': 160,
                'collisions': 'Vulnerable to rainbow tables',
                'security': 'Weak - uses SHA-1 with salt',
                'common_uses': 'MySQL user authentication'
            },
            'NTLM': {
                'description': 'NT LAN Manager hash',
                'bits': 128,
                'collisions': 'Vulnerable to rainbow tables',
                'security': 'Weak - no salt, single iteration',
                'common_uses': 'Windows authentication'
            },
            'LM': {
                'description': 'LAN Manager hash',
                'bits': 128,
                'collisions': 'Extremely vulnerable',
                'security': 'Very weak - disabled in modern Windows',
                'common_uses': 'Legacy Windows authentication'
            },
            'bcrypt': {
                'description': 'Blowfish-based password hashing',
                'bits': 'Variable',
                'collisions': 'Resistant',
                'security': 'Strong - designed for password hashing',
                'common_uses': 'Password storage'
            },
            'Unix Crypt': {
                'description': 'Traditional Unix password hashing',
                'bits': 'Variable',
                'collisions': 'Vulnerable to modern attacks',
                'security': 'Weak for modern standards',
                'common_uses': 'Legacy Unix systems'
            },
            'JWT': {
                'description': 'JSON Web Token',
                'bits': 'Depends on algorithm',
                'collisions': 'Depends on algorithm used',
                'security': 'Depends on implementation',
                'common_uses': 'Web authentication, API authorization'
            }
        }
        
        return info.get(hash_type, {'description': 'No information available'})

    def generate_hash(self, text, algorithm='sha256'):
        """Generate a hash of the given text using specified algorithm"""
        algorithm = algorithm.lower()
        if algorithm not in hashlib.algorithms_available:
            return f"Error: Algorithm '{algorithm}' not available"
        
        hash_func = hashlib.new(algorithm)
        hash_func.update(text.encode('utf-8'))
        return hash_func.hexdigest()

def print_hash_info(hash_type, info):
    """Print formatted information about a hash type"""
    print(f"\n[+] {hash_type} Hash Information:")
    print("-" * 50)
    for key, value in info.items():
        print(f"{key.capitalize():<15}: {value}")
    print("-" * 50)

def main():
    analyzer = HashAnalyzer()
    parser = argparse.ArgumentParser(description='Hash Analyzer Tool')
    parser.add_argument('hash', nargs='?', help='Hash to analyze')
    parser.add_argument('-l', '--list', action='store_true', help='List all supported hash types with examples')
    parser.add_argument('-g', '--generate', metavar='TEXT', help='Generate hashes of the given text using all algorithms')
    
    args = parser.parse_args()
    
    if args.list:
        print("\n[+] Supported Hash Types with Examples:")
        print("=" * 60)
        for hash_type, example in analyzer.hash_examples.items():
            print(f"\n{hash_type}:")
            print(f"Example: {example}")
            info = analyzer.get_hash_info(hash_type)
            print(f"Description: {info['description']}")
        return
    
    if args.generate:
        print(f"\n[+] Generated Hashes for: '{args.generate}'")
        print("=" * 60)
        for algo in sorted(hashlib.algorithms_available):
            if algo.startswith('shake_'):  # Skip variable-length hashes
                continue
            try:
                hash_val = analyzer.generate_hash(args.generate, algo)
                print(f"{algo.upper():<10}: {hash_val}")
            except:
                continue
        return
    
    if args.hash:
        hash_str = args.hash
    else:
        print("\nEnter a hash to analyze or press Ctrl+C to exit")
        print("You can also run with -h for help\n")
        hash_str = input("Hash: ")
    
    possible_types = analyzer.identify_hash(hash_str)
    
    print(f"\n[+] Analysis Results for: {hash_str}")
    print("=" * 60)
    
    if "Unknown hash type" in possible_types:
        print("[-] Could not identify hash type")
        print("\nPossible reasons:")
        print("- The hash is from a rare or custom algorithm")
        print("- The hash is malformed or truncated")
        print("- The hash uses an unsupported encoding")
    else:
        print("[+] Possible hash types:")
        for hash_type in possible_types:
            print(f"- {hash_type}")
        
        # Show detailed info for the first match
        primary_type = possible_types[0]
        info = analyzer.get_hash_info(primary_type)
        print_hash_info(primary_type, info)
        
        if len(possible_types) > 1:
            print("\nNote: Multiple hash types matched. Here's why:")
            for hash_type in possible_types[1:]:
                print(f"- {hash_type} has the same length as {primary_type}")
            print("\nYou may need additional context to determine the exact type.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Operation cancelled by user")
    except Exception as e:
        print(f"\n[!] An error occurred: {str(e)}")