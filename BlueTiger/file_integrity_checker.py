import hashlib
import os

def print_banner():
    banner = """
  ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⡿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⣿⣿
⣿⣿⠀⠀⠀⢠⣴⡄⠀⠀⠀⠈⢻⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿
⣿⣿⠀⠀⣶⣾⣿⣷⣶⡄⠀⠀⠀⠙⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣿⣿
⣿⣿⠀⠀⠉⢹⣿⡏⠉⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⣿⣿
⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣤⣤⣤⣤⣤⣤⣤⠀⠀⣿⣿
⣿⣿⠀⠀⠀⠀⠀⠀⣠⣴⣶⣷⣶⣦⡀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠉⠀⠀⣿⣿
⣿⣿⠀⠀⠀⠀⠀⣸⣿⠋⠀⠀⠈⢻⣿⡄⠀⠀⣴⣶⣶⣶⣶⣶⣶⣶⠀⠀⣿⣿
⣿⣿⠀⠀⠀⠀⠀⢿⣿⠀⠀⠀⠀⢸⣿⡇⠀⠀⠈⠉⠉⠉⠉⠉⠉⠉⠀⠀⣿⣿
⣿⣿⠀⠀⠀⠀⠀⠈⣿⣷⣦⣤⣶⣿⣟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿
⣿⣿⠀⠀⠀⢀⣴⣿⠟⠛⠉⠉⠙⠛⢿⣷⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿
⣿⣿⠀⠀⣰⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠘⢿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿
⣿⣿⠀⠀⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿
⣿⣿⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿
    """
    print(banner)

def generate_checksum(file_path, algorithm='sha256'):
    """Generate a checksum for a given file."""
    hash_func = getattr(hashlib, algorithm)()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def verify_checksum(file_path, checksum, algorithm='sha256'):
    """Verify the checksum of a given file."""
    return generate_checksum(file_path, algorithm) == checksum

def save_checksums(directory, output_file, algorithm='sha256'):
    """Generate and save checksums for all files in a directory."""
    checksums = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            checksums[file_path] = generate_checksum(file_path, algorithm)

    with open(output_file, 'w') as f:
        for file_path, checksum in checksums.items():
            f.write(f"{file_path}:{checksum}\n")

def load_checksums(checksum_file):
    """Load checksums from a file."""
    checksums = {}
    with open(checksum_file, 'r') as f:
        for line in f:
            file_path, checksum = line.strip().split(':')
            checksums[file_path] = checksum
    return checksums

def verify_directory(directory, checksum_file, algorithm='sha256'):
    """Verify the integrity of files in a directory against a checksum file."""
    checksums = load_checksums(checksum_file)
    for file_path, checksum in checksums.items():
        if not verify_checksum(file_path, checksum, algorithm):
            print(f"Integrity check failed for {file_path}")
        else:
            print(f"Integrity check passed for {file_path}")

# Example usage
if __name__ == "__main__":
    print_banner()

    directory = 'path/to/your/directory'
    checksum_file = 'checksums.txt'

    # Generate and save checksums
    save_checksums(directory, checksum_file)

    # Verify integrity
    verify_directory(directory, checksum_file)
