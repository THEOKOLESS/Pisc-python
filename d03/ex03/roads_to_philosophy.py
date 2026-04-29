import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_page_title(soup):
    """Extract page title from Wikipedia page"""
    title_elem = soup.find('h1', class_='firstHeading')
    return title_elem.text if title_elem else "Unknown"

def check_redirect(soup):
    """Check if page is a redirect and return redirect URL if exists"""
    redirect = soup.find('div', class_='mw-parser-output')
    if redirect:
        link = redirect.find('a')
        if link and 'href' in link.attrs:
            href = link.get('href')
            if '/wiki/' in href and ':' not in href and not link.get('class') and 'Main_Page' not in href:
                print(f"Redirected to {href}")
                return "https://en.wikipedia.org" + href
    return None


def normalize_href(base_url, href):
    if not href:
        return None
    if href.startswith('#'):
        return None
    if href.startswith('/wiki/') or href.startswith('//') or href.startswith('http://') or href.startswith('https://'):
        return urljoin(base_url, href)
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

            soup = BeautifulSoup(response.text, 'html.parser')
            title = get_page_title(soup)
            visited_pages.append(title)

            # Check for redirect
            # redirect_url = check_redirect(soup)
            # if redirect_url and redirect_url != url:
            #     url = redirect_url
            #     continue

            if "Philosophy" in title or url == "https://en.wikipedia.org/wiki/Philosophy":
                for page_title in visited_pages:
                    print(page_title)
                print(f"{len(visited_pages)} roads from {search} to philosophy")
                return

            # Find the first valid link in the content
            content = soup.find(id="mw-content-text")
            if not content:
                print("It leads to a dead end !")
                return

            first_valid_link = None
            for paragraph in content.find_all('p'):
                all_links = paragraph.find_all('a', href=True)
                for link in all_links:
                    # Skip links in spans (citations)
                    if link.find_parent('span') or link.find_parent('i') or link.find_parent('sup'):
                        continue
                    href = link['href']
                    # Valid link conditions
                    if ('/wiki/' in href and ':' not in href and 'Main_Page' not in href):
                        first_valid_link = link
                        break
                if first_valid_link:
                    break

            if not first_valid_link:
                print("It leads to a dead end !")
                return
            # print(f"{title} -> {first_valid_link['href']}")
            next_url = normalize_href(base_url, first_valid_link['href'])
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
