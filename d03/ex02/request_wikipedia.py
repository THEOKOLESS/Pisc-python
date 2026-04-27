
import sys
import requests

def sanitize_filename(query):
    name = query.replace(" ", "_")
    return name

def get_best_title(query, base_url, headers):
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": 1,
        "format": "json",
        "utf8": 1,
    }
    r = requests.get(base_url, params=params, headers=headers, timeout=10)
    r.raise_for_status()
    data = r.json()

    results = data.get("query", {}).get("search", [])
    if not results:
        return None
    return results[0].get("title")



def get_plain_extract(title, base_url, headers):
    params = {
        "action": "query",
        "prop": "extracts",
        "titles": title,
        "explaintext": 1,   # texte brut, sans wiki markup
        "redirects": 1,
        "format": "json",
        "utf8": 1,
    }
    r = requests.get(base_url, params=params, headers=headers, timeout=10)
    r.raise_for_status()
    data = r.json()

    pages = data.get("query", {}).get("pages", {})
    page = next(iter(pages.values()), {})
    extract = page.get("extract", "")
    return extract.strip()

def main():
    if len(sys.argv) != 2:
        print("Usage: python request_wikipedia.py <search_query>")
        return
    query = sys.argv[1].strip()
    if not query:
        print("Error: search_query cannot be empty.")
        return
    name = sanitize_filename(query)
    base_url = "https://fr.wikipedia.org/w/api.php"
    headers = {
        "User-Agent": "request_wikipedia/1.0 (student script)",
        "Accept": "application/json",
    }
    try:
        title = get_best_title(query, base_url, headers)
        if not title:
            print("No results found for the query.")
            return
        
        text = get_plain_extract(title, base_url, headers)
        if not text:
            print("No extract found for the title.")
            return

        
        filename = f"{name}.wiki"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
    except requests.exceptions.RequestException as e:
        print(f"HTTP request failed: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"JSON parsing failed: {e}")
        sys.exit(1)
    except OSError as e:
        print(f"File operation failed: {e}")
        sys.exit(1)



        

if __name__ == "__main__":
    main()