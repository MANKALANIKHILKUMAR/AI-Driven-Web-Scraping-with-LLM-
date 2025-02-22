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
    
    # Initialize driver as None to ensure it's always defined
    driver = None
    
    try:
        # Set up Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")  # Avoid memory issues

        # Get the root directory path
        root_dir = os.path.dirname(os.path.abspath(__file__))

        # Specify the path to the ChromeDriver binary
        chrome_driver_path = os.path.join(root_dir, "bin", "chromedriver")

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
        # Close the browser if driver was initialized
        if driver:
            driver.quit()
