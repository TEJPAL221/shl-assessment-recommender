import requests
from bs4 import BeautifulSoup
import json
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "https://www.shl.com"
CATALOG_BASE = "https://www.shl.com/products/product-catalog/"
OUTPUT_PATH = "../../../data/raw/shl_catalog_raw.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


def create_session():
    session = requests.Session()
    retry = Retry(
        total=5,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.headers.update(HEADERS)
    return session


def fetch_soup(session, url):
    resp = session.get(url, timeout=60)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "lxml")


def collect_assessment_links(session):
    """
    Crawl paginated catalog pages and collect ONLY individual test pages
    """
    links = set()
    start = 0
    page_size = 12  # SHL uses 12 items per page

    while True:
        url = f"{CATALOG_BASE}?start={start}"
        print(f"[INFO] Crawling catalog page: start={start}")
        soup = fetch_soup(session, url)

        page_links = soup.select("a[href*='/product-catalog/view/']")
        if not page_links:
            break

        for a in page_links:
            href = a.get("href")
            if href:
                full_url = BASE_URL + href if href.startswith("/") else href
                # Exclude job solutions explicitly
                if "solution" not in full_url.lower():
                    links.add(full_url)

        start += page_size
        time.sleep(1)

    return list(links)


def parse_assessment(session, url):
    soup = fetch_soup(session, url)

    name_tag = soup.find("h1")
    name = name_tag.get_text(strip=True) if name_tag else ""

    description = soup.get_text(" ", strip=True)
    description = description[:3000]

    text = description.lower()
    test_type = []
    if "knowledge" in text or "skill" in text:
        test_type.append("K")
    if "personality" in text or "behavior" in text:
        test_type.append("P")

    return {
        "assessment_name": name,
        "assessment_url": url,
        "description": description,
        "test_type": test_type,
        "duration": "",
        "remote_testing": "Yes",
        "adaptive_support": "Unknown"
    }


def scrape():
    session = create_session()
    print("[INFO] Collecting individual assessment links...")
    links = collect_assessment_links(session)
    print(f"[INFO] Found {len(links)} individual assessment pages")

    results = []

    for i, link in enumerate(links, 1):
        try:
            print(f"[{i}/{len(links)}] Scraping {link}")
            record = parse_assessment(session, link)
            if record["assessment_name"]:
                results.append(record)
            time.sleep(1)
        except Exception as e:
            print(f"[WARN] Failed {link}: {e}")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"[SUCCESS] Raw dataset saved with {len(results)} records")


if __name__ == "__main__":
    scrape()
