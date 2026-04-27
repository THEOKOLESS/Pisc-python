import sys
import requests
from bs4 import BeautifulSoup

def main():


    if len(sys.argv) != 2:
        print("Usage: python roads_to_philosophy.py <Wikipedia resource>")
        sys.exit(1)

    search = sys.argv[1]
    visited = set()
    steps = 0
    base_url = "https://en.wikipedia.org/wiki/"
    url = base_url + search.replace(" ", "_")
    while url not in visited:
        visited.add(url)
        steps += 1

        if url == "https://en.wikipedia.org/wiki/Philosophy":
            print(f"Reached Philosophy in {steps} steps!")
            break

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the first link in the main content
        content = soup.find(id="mw-content-text")
        first_link = content.find('a', href=True)

        if not first_link:
            print("No more links to follow. Stuck at:", url)
            break

        url = "https://en.wikipedia.org" + first_link['href']


if __name__ == "__main__":
    main()
