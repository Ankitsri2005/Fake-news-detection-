import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = soup.find_all('p')
        text = ' '.join(p.text for p in paragraphs)
        return text.strip()[:2000]  # Limit length for processing
    except:
        return "Unable to fetch content."
