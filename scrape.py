from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

AUTH = os.getenv("AUTH")
SBR_WEBDRIVER = f"https://{AUTH}@brd.superproxy.io:9515"

def scrape_website_with_sbr(website):
    """
    Scrapes the website using Selenium and ChromeDriver.
    
    Args:
        website (str): The URL of the website to scrape.
    
    Returns:
        str: The page source of the website.
    """
    logging.info("Launching Chrome Browser...")
    
    try:
        # Set up Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")  # Avoid memory issues

        # Specify the path to the ChromeDriver binary
        chrome_driver_path = os.path.join(os.getcwd(), "bin", "chromedriver")

        # Initialize the Chrome WebDriver
        driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

        # Navigate to the URL
        logging.info(f"Navigating to URL: {website}")
        driver.get(website)
        logging.info("Page loaded...")

        # Get the page source
        html = driver.page_source

        return html
    except Exception as e:
        logging.error(f"Error during scraping: {e}")
        raise
    finally:
        # Close the browser
        if driver:
            driver.quit()

def extract_body_content(html_content):
    """
    Extracts the body content from the HTML.
    
    Args:
        html_content (str): The HTML content of the website.
    
    Returns:
        str: The body content of the website.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    else:
        return "No body content found"

def clean_body_content(body_content):
    """
    Cleans the body content by removing unnecessary tags and whitespace.
    
    Args:
        body_content (str): The body content of the website.
    
    Returns:
        str: The cleaned body content.
    """
    soup = BeautifulSoup(body_content, "html.parser")
    
    # Remove unnecessary tags
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    # Extract text and clean it
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content

def split_dom_content(dom_content, chunk_size=6000):
    """
    Splits the DOM content into chunks of a specified size.
    
    Args:
        dom_content (str): The DOM content to split.
        chunk_size (int): The size of each chunk.
    
    Returns:
        list: A list of chunks.
    """
    return [
        dom_content[x : x + chunk_size]
        for x in range(0, len(dom_content), chunk_size)
    ]
