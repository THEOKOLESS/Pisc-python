import sys
import requests
from bs4 import BeautifulSoup

def get_page_title(soup):
    """Extract page title from Wikipedia page"""
    title_elem = soup.find('h1', class_='firstHeading')
    return title_elem.text if title_elem else "Unknown"


def normalize_href(href):
    if not href:
        return None
    if href.startswith('#'):
        return None
    if href.startswith('/wiki/'):
        return "https://en.wikipedia.org" + href
    if href.startswith('//en.wikipedia.org/wiki/'):
        return "https:" + href
    if href.startswith('https://en.wikipedia.org/wiki/'):
        return href
    if href.startswith('http://en.wikipedia.org/wiki/'):
        return "https://" + href[len("http://"):]
    return None


def is_valid_article_href(href):
    if not href:
        return False
    if href.startswith('/wiki/'):
        path = href
    elif href.startswith('//en.wikipedia.org/wiki/'):
        path = href[len('//en.wikipedia.org'):]
    elif href.startswith('https://en.wikipedia.org/wiki/'):
        path = href[len('https://en.wikipedia.org'):]
    elif href.startswith('http://en.wikipedia.org/wiki/'):
        path = href[len('http://en.wikipedia.org'):]
    else:
        return False
    if ':' in path:
        return False
    if path == '/wiki/Main_Page':
        return False
    return True


def find_first_valid_link(main):
    # Prefer direct intro paragraphs first.
    direct_paragraphs = [child for child in main.find_all(recursive=False) if child.name == 'p']

    for paragraph in direct_paragraphs:
        for link in paragraph.find_all('a', href=True):
            href = link.get('href', '')
            if is_valid_article_href(href):
                return link

    # Fallback for pages where intro paragraphs are nested in extra wrappers.
    for paragraph in main.find_all('p'):
        if paragraph.find_parent('table'):
            continue
        for link in paragraph.find_all('a', href=True):
            href = link.get('href', '')
            if is_valid_article_href(href):
                return link

    return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python roads_to_philosophy.py <Wikipedia resource>")
        sys.exit(1)

    search = sys.argv[1]
    visited_pages = []  # Store (url, title) tuples
    visited_urls = set()
    base_url = "https://en.wikipedia.org/wiki/"
    url = base_url + search.replace(" ", "_")
    headers = {
        "User-Agent": "request_wikipedia/1.0 (42 student script)",
        "Accept": "application/json",
    }
    
    try:
        while url not in visited_urls:
            visited_urls.add(url)

            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Error: Failed to fetch {url}: {e}")
                sys.exit(1)

            soup = BeautifulSoup(response.text, "lxml")
            title = get_page_title(soup)
            visited_pages.append(title)

       

            if title == "Philosophy" or url == "https://en.wikipedia.org/wiki/Philosophy":
                for page_title in visited_pages:
                    print(page_title)
                print(f"{len(visited_pages)} roads from {search} to philosophy")
                return

            # Find the first valid link in the content
            content = soup.find(id="mw-content-text")
            if not content:
                print("It leads to a dead end !")
                return

            main = content.find("div", class_="mw-parser-output")
            if not main:
                print("It leads to a dead end !")
                return

            first_valid_link = find_first_valid_link(main)

            if not first_valid_link:
                print("It leads to a dead end !")
                return
        
            next_url = normalize_href(first_valid_link['href'])
            if not next_url:
                print("It leads to a dead end !")
                return
            url = next_url

        # If we exit the while loop, we've revisited a URL
        print("It leads to an infinite loop !")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)



if __name__ == "__main__":
    main()
