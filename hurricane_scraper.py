import requests
from bs4 import BeautifulSoup
import re
import json

# Fetch the content of a webpage
def fetch_page_content(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

# Clean unwanted elements from text
def clean_text(text):
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'[\xa0]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

# Extract headings and related paragraphs
def extract_hurricane_data(soup):
    content_div = soup.find('div', {'class': 'mw-body-content'})
    headings = content_div.find_all('div', class_='mw-heading mw-heading3')
    
    results = []
    for heading in headings:
        h3_tag = heading.find('h3')
        if h3_tag:
            h3_text = clean_text(h3_tag.get_text(strip=True))
            paragraphs = []
            next_tag = heading.find_next_sibling('p')
            while next_tag and next_tag.name == 'p':
                paragraphs.append(clean_text(next_tag.get_text(strip=True)))
                next_tag = next_tag.find_next_sibling()
            if paragraphs:
                results.append({'storm_name': h3_text, 'content': paragraphs})
    return results

# Save data to a JSON file
def save_to_json(data, filename='hurricane_data.json'):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Main execution
if __name__ == '__main__':
    url = "https://en.wikipedia.org/wiki/1975_Pacific_hurricane_season"
    soup = fetch_page_content(url)
    hurricane_data = extract_hurricane_data(soup)
    save_to_json(hurricane_data)
    print("Data successfully saved to hurricane_data.json")
