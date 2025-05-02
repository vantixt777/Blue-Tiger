import dns.resolver
import requests
import re

# Banner
BANNER = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣶⣶⣦⣄⡀⠀⠀⠀⠀⢀⣀⣠⣤⣤⣴⣶⣶⣦⣤⣤⣄⣀⠀⠀⠀⠀⠀⣀⣤⣴⣶⣾⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣀⣀⣀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⣀⣀⣀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠉⠉⠙⠛⠿⢿⣶⣦⣀⠀⣿⣿⣿⣿⣿⣿⡿⠋⠁⠀⠀⠉⠻⣿⣿⣿⣿⣿⣿⠛⠁⠀⠀⠈⠙⢿⣿⣿⣿⣿⣿⣏⠀⣠⣴⣾⡿⠟⠛⠋⠉⠁⠀⠀⠀⠀
⠀⢀⣠⣤⣤⣤⣤⣤⣤⣀⣈⠙⠻⣷⣿⣿⣿⣿⣿⡟⠀⠀⠀⢀⠀⠀⠀⠘⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⡿⠟⠋⣁⣀⣤⣤⣤⣤⣤⣤⣀⡀⠀
⠈⠉⠉⠉⠉⠉⠉⠉⠛⠛⠿⢿⣶⣄⣿⣿⣿⣿⣿⡇⠀⠀⠀⣾⡆⠀⠀⠀⣿⣿⣿⣿⠀⠀⠀⢸⣧⠀⠀⠀⣸⣿⣿⣿⣿⣿⣤⣶⡿⠟⠛⠋⠉⠉⠉⠉⠉⠉⠉⠁
⠀⠀⠀⣠⣤⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⢿⠃⠀⢀⣼⣿⣿⣿⣿⣧⡀⠀⠸⡏⠀⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣤⣄⠀⠀⠀
⠀⠀⠊⠉⠁⠀⣠⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣤⣤⣶⣿⣿⣿⠿⠿⣿⣿⣿⣶⣤⣤⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣀⠀⠈⠉⠑⠀⠀
⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠛⠛⠛⠛⠛⠛⠛⠋⠀⠀⠀⠀⠙⠛⠛⠛⠛⠛⠛⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠻⢿⣿⡿⠟⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠻⣿⣿⠿⠋⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀
"""

print(BANNER)

# Farbdefinitionen (falls im ursprünglichen Code verwendet)
class color:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

# Platzhalter für Funktionen, die im ursprünglichen Code existieren könnten
def Title(title):
    print(f"\n[{color.CYAN}{title}{color.RESET}]")

def ErrorModule(e):
    print(f"{color.RED}Error in module import: {e}{color.RESET}")

def BEFORE(): # Muss angepasst werden, basierend auf dem ursprünglichen Code
    return "["

def current_time_hour(): # Muss angepasst werden, basierend auf dem ursprünglichen Code
    return "TIME"

def AFTER(): # Muss angepasst werden, basierend auf dem ursprünglichen Code
    return "]"

def INPUT(): # Muss angepasst werden, basierend auf dem ursprünglichen Code
    return "INPUT"

def reset(): # Muss angepasst werden, basierend auf dem ursprünglichen Code
    return color.RESET

def WAIT(): # Muss angepasst werden, basierend auf dem ursprünglichen Code
    return "WAIT"

def INFO_ADD(): # Muss angepasst werden, basierend auf dem ursprünglichen Code
    return "+"

def white(): # Muss angepasst werden, basierend auf dem ursprünglichen Code
    return color.WHITE

def red(): # Muss angepasst werden, basierend auf dem ursprünglichen Code
    return color.RED

def Censored(text): # Muss angepasst werden, basierend auf dem ursprünglichen Code
    print(f"Censored: {text}")

def Continue(): # Muss angepasst werden, basierend auf dem ursprünglichen Code
    input("Press Enter to continue...")

def Reset(): # Muss angepasst werden, basierend auf dem ursprünglichen Code
    pass

def Error(e): # Muss angepasst werden, basierend auf dem ursprünglichen Code
    print(f"{color.RED}An error occurred: {e}{color.RESET}")

try:
    Title("Email Lookup")

    def get_email_info(email):
        info = {}
        try: domain_all = email.split('@')[-1]
        except: domain_all = None

        try: name = email.split('@')[0]
        except: name = None

        try: domain = re.search(r"@([^@.]+)\.", email).group(1)
        except: domain = None
        try: tld = f".{email.split('.')[-1]}"
        except: tld = None

        try:
            mx_records = dns.resolver.resolve(domain_all, 'MX')
            mx_servers = [str(record.exchange) for record in mx_records]
            info["mx_servers"] = mx_servers
        except dns.resolver.NoAnswer:
            info["mx_servers"] = None
        except dns.resolver.NXDOMAIN:
            info["mx_servers"] = None


        try:
            spf_records = dns.resolver.resolve(domain_all, 'SPF')
            info["spf_records"] = [str(record) for record in spf_records]
        except dns.resolver.NoAnswer:
            info["spf_records"] = None
        except dns.resolver.NXDOMAIN:
            info["spf_records"] = None

        try:
            dmarc_records = dns.resolver.resolve(f'_dmarc.{domain_all}', 'TXT')
            info["dmarc_records"] = [str(record) for record in dmarc_records]
        except dns.resolver.NoAnswer:
            info["dmarc_records"] = None
        except dns.resolver.NXDOMAIN:
            info["dmarc_records"] = None

        if info.get("mx_servers"):
            for server in info["mx_servers"]:
                if "google.com" in server:
                    info["google_workspace"] = True
                elif "outlook.com" in server:
                    info["microsoft_365"] = True

        return info, domain_all, domain, tld, name

    email = input(f"\n{BEFORE()} {current_time_hour()} {AFTER()} {INPUT()} Email -> {reset()}")
    Censored(email)

    print(f"{BEFORE()} {current_time_hour()} {AFTER()} {WAIT()} Information Recovery..{reset()}")
    info, domain_all, domain, tld, name = get_email_info(email)

    try:
        mx_servers = info["mx_servers"]
        mx_servers = ' / '.join(mx_servers) if mx_servers else None
    except Exception as e:
        mx_servers = None

    try:
        spf_records = info.get("spf_records")
    except:
        spf_records = None

    try:
        dmarc_records = info.get("dmarc_records")
        dmarc_records = ' / '.join(dmarc_records) if dmarc_records else None
    except:
        dmarc_records = None

    try:
        google_workspace = info.get("google_workspace")
    except:
        google_workspace = None

    try:
        mailgun_validation = info.get("mailgun_validation")
        mailgun_validation = ' / '.join(mailgun_validation) if mailgun_validation else None
    except:
        mailgun_validation = None

    print(f"""
    {INFO_ADD()} Email     : {white()}{email}{red()}
    {INFO_ADD()} Name      : {white()}{name}{red()}
    {INFO_ADD()} Domain    : {white()}{domain}{red()}
    {INFO_ADD()} Tld       : {white()}{tld}{red()}
    {INFO_ADD()} Domain All: {white()}{domain_all}{red()}
    {INFO_ADD()} Servers   : {white()}{mx_servers}{red()}
    {INFO_ADD()} Spf       : {white()}{spf_records}{red()}
    {INFO_ADD()} Dmarc     : {white()}{dmarc_records}{red()}
    {INFO_ADD()} Workspace : {white()}{google_workspace}{red()}
    {INFO_ADD()} Mailgun   : {white()}{mailgun_validation}{red()}
    {color.RESET}""")

    Continue()
    Reset()
except Exception as e:
    Error(e)