import whois
import sys
import socket

def create_banner():
    """
    Displays a simple banner for the WHOIS query tool.
    """
    banner = r"""
     _   _   _   _   _
    | | | | | | | | (_)
    | | | | | | | |  _  ___
    | | | | | | | | | |/ __|
    | |_| | | |_| | | |\__ \
     \___/   \___/  |_||___/
    """
    print(banner)
    print("WHOIS Query Tool v1.0")
    print("------------------------")

def perform_whois_lookup(domain_name):
    """
    Performs a WHOIS lookup for the given domain name and prints the results.

    Args:
        domain_name (str): The domain name to query.
    """
    try:
        # Perform the WHOIS query
        whois_info = whois.whois(domain_name)

        # Print the WHOIS information in a user-friendly format
        print(f"\nWHOIS Information for {domain_name}:")
        print("----------------------------------------")

        # Iterate through the dictionary and print
        for key, value in whois_info.items():
            if value:  # Only print if the value is not empty or None
                print(f"{key.title()}:") # Capitalize
                if isinstance(value, list):
                    for item in value:
                        print(f"  - {item}")
                elif isinstance(value, dict):
                  for k, v in value.items():
                    print(f"   {k} : {v}")
                else:
                    print(f"  {value}")
        print("----------------------------------------")

    except whois.parser.PywhoisError as e:
        print(f"Error: {e}")
        print(f"Could not retrieve WHOIS information for {domain_name}.  The domain may not exist, or there may be a problem with the WHOIS server.")
    except socket.gaierror:
        print(f"Error: Invalid domain name.  Please check the domain name and try again.  Example: example.com")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    create_banner() # Display Banner

    # Get the domain name from the command line or user input
    if len(sys.argv) == 2:
        domain_name = sys.argv[1]
    else:
        domain_name = input("Enter the domain name to query (e.g., example.com): ")

    perform_whois_lookup(domain_name)
