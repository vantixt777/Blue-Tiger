import requests
import json

# Banner
BANNER = """
  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⡀⠀⡀⠀⠂⡀⢀⢰⠀⢂⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣐⣬⣄⣷⡀⢸⡃⡘⡸⡄⢸⠀⠀⡇⠀⢠⠀⠀⠀
⠀⠀⠀⠀⠀⣠⡴⠚⢉⢍⢂⣼⣴⣿⣿⣿⣷⣷⣷⣣⣏⣆⣼⠀⠀⠄⠀⠀⠀
⠀⠀⠀⢠⡞⠋⠀⡑⣮⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣷⣼⣆⣌⡠⢁⡤
⠀⠀⣰⠋⠀⣀⣺⣾⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠁
⠀⡼⠁⢀⣿⣿⣿⡿⣿⡛⣿⣿⣿⡷⢸⣿⠀⠀⠀⠀⣹⣿⣿⣿⣟⠣⠀⠀⠀
⡰⠁⢀⣼⣿⠟⢿⡇⠹⣿⣿⣿⠟⠀⢠⡿⠀⠀⣠⣾⡿⣿⡥⠊⠁⠀⠀⠀⠀
⠁⢠⣾⠟⠁⠀⠈⠳⢿⣦⣠⣤⣦⣼⠟⠁⣠⣾⣿⣿⣟⠍⠒⠀⠠⠀⠀⠀⠀
⢠⡟⠁⢀⣀⣀⣀⣀⡀⠈⣉⣉⣡⣤⣶⣿⡿⡿⡿⡻⠥⠑⡀⠀⠀⠀⠀⠀⠀
⠏⡠⠚⠉⠋⢍⠋⢫⠋⠛⢹⢻⡟⠻⣟⢏⠌⢊⡌⠌⠄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠘⠂⠘⠂⠿⠈⠀⠀⠀⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀
       ~ by blue tiger ~
"""

print(BANNER)

def ip_lookup_extreme(ip_address):
    """
    Führt ein extremes IP-Lookup durch und ruft Daten von verschiedenen APIs ab.
    """
    print(f"\nLookup für IP-Adresse: {ip_address}")

    apis = [
        ("ip-api.com", f"http://ip-api.com/json/{ip_address}"),
        ("ipinfo.io", f"https://ipinfo.io/{ip_address}/json"), # Benötigt keinen Key für einfache Abfragen
        ("ipapi.co", f"https://ipapi.co/{ip_address}/json/"),
        # ("abstractapi.com", f"https://ipgeolocation.abstractapi.com/v1/?ip_address={ip_address}&api_key=YOUR_API_KEY"), # Kostenpflichtig mit Free Tier
        ("ipwhois.io", f"https://ipwhois.io/{ip_address}"),
        ("geoip.nekudo.com", f"https://geoip.nekudo.com/api/{ip_address}"),
    ]

    for name, url in apis:
        print(f"\n--- Abfrage von {name} ---")
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
            print(json.dumps(data, indent=4))
        except requests.exceptions.RequestException as e:
            print(f"Fehler bei der Abfrage von {name}: {e}")
        except json.JSONDecodeError:
            print(f"Fehler beim Decodieren der JSON-Antwort von {name}.")

if __name__ == "__main__":
    ip_to_lookup = input("Gib die IP-Adresse ein, die du untersuchen möchtest: ")
    ip_lookup_extreme(ip_to_lookup)