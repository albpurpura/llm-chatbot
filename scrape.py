import requests
from bs4 import BeautifulSoup
import re

def download_text_from_url(url):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract text from the parsed HTML
            text = soup.get_text()
            
            return text
        else:
            print(f"Failed to fetch URL. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None

def extract_urls(text):
    # Regular expression pattern to match URLs
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')    
    # Find all matches of the URL pattern in the text
    urls = re.findall(url_pattern, text)
    return urls
