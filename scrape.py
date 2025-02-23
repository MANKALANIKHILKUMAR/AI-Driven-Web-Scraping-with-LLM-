import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

def scrape_website_with_crawl4ai(url):
    try:
        # Use Crawl4AI API for scraping
        CRAWL4AI_API_KEY = os.getenv("CRAWL4AI_API_KEY")
        headers = {
            "Authorization": f"Bearer {CRAWL4AI_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "url": url,
            "format": "html",
        }
        response = requests.post(
            "https://api.crawl4ai.com/scrape",
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        return response.json().get("html")
    except Exception as e:
        print(f"Error using Crawl4AI: {e}")
        # Fallback to requests-html
        from requests_html import HTMLSession
        session = HTMLSession()
        response = session.get(url)
        return response.text

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    else:
        return "No body content found"

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    return cleaned_content

def split_dom_content(dom_content, chunk_size=6000):
    return [dom_content[x : x + chunk_size] for x in range(0, len(dom_content), chunk_size)]



