#!/usr/bin/env python3

"""
google_dorking.py - A command-line tool for performing Google Dorking queries.

This tool takes a list of dorks and a search term (optional) and performs
Google searches for each dork, displaying the results. Be aware of ethical
implications and legal boundaries when using this tool.
"""

import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import sys
import time

# ASCII Banner
BANNER = """
  _     _       _       _
 | |   (_)     | |     | |
 | |__  _   ___| | __  | |__   ___  _ __
 | '_ \| | / __| |/ /  | '_ \ / _ \| '_ \\
 | |_) | | \__ \   <   | | | | (_) | | | |
 |_.__/|_| |___/_|\_\  |_| |_|\___/|_| |_|
"""

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
GOOGLE_SEARCH_URL = "https://www.google.com/search?q={query}&start={start}"
RESULTS_PER_PAGE = 10
SEARCH_DELAY = 1  # Delay in seconds between searches

def search_google(query, start=0):
    """Performs a Google search for the given query and returns the results.

    Args:
        query (str): The search query.
        start (int): The starting result number (for pagination).

    Returns:
        list: A list of dictionaries, where each dictionary contains the
              'title' and 'url' of a search result, or None if an error occurs.
    """
    encoded_query = quote_plus(query)
    url = GOOGLE_SEARCH_URL.format(query=encoded_query, start=start)
    headers = {'User-Agent': USER_AGENT}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for result_set in soup.find_all('div', class_='Gx5Zad'):
            link = result_set.find('a')
            title_element = result_set.find('h3')
            if link and title_element:
                href = link.get('href')
                title = title_element.get_text(strip=True)
                if href.startswith('/url?q='):
                    actual_url = href.split('/url?q=')[1].split('&')[0]
                    results.append({'title': title, 'url': actual_url})
        return results
    except requests.exceptions.RequestException as e:
        print(f"Error during Google search for '{query}': {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"An unexpected error occurred during search for '{query}': {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description="Perform Google Dorking queries.")
    parser.add_argument("dorks", nargs='+', help="One or more Google dorks (e.g., inurl:admin filetype:log).")
    parser.add_argument("-t", "--term", help="Optional search term to combine with dorks (e.g., 'sensitive data').")
    parser.add_argument("-p", "--pages", type=int, default=1, help="Number of result pages to fetch per dork.")
    args = parser.parse_args()

    print(BANNER)

    for dork in args.dorks:
        query = dork
        if args.term:
            query = f"{dork} {args.term}"

        print(f"\nPerforming dork: '{query}'")

        all_results = []
        for page in range(args.pages):
            start = page * RESULTS_PER_PAGE
            results = search_google(query, start)

            if results:
                all_results.extend(results)
                print(f"  Page {page + 1} results:")
                for result in results:
                    print(f"    Title: {result['title']}")
                    print(f"    URL: {result['url']}")
                if page < args.pages - 1:
                    print(f"  Waiting {SEARCH_DELAY} seconds before the next page...")
                    time.sleep(SEARCH_DELAY)
            else:
                print(f"  No results found or an error occurred on page {page + 1}.")
                break

        if all_results:
            print(f"\nTotal results for dork '{query}': {len(all_results)}")
        else:
            print(f"\nNo results found for dork '{query}'.")

if __name__ == "__main__":
    main()