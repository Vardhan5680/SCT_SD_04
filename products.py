import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

BASE_URL = "http://books.toscrape.com/"
CATALOGUE_URL = urljoin(BASE_URL, "catalogue/page-{}.html")
CSV_HEADERS = ['Title', 'Price', 'Availability', 'Rating', 'Product URL', 'Image URL']

def extract_product_data(soup):
    products = soup.find_all('article', class_='product_pod')
    product_list = []

    for product in products:
        title = product.h3.a['title']
        price = product.find('p', class_='price_color').text.strip()
        availability = product.find('p', class_='instock availability').text.strip()
        rating = product.p.get('class')[1] if len(product.p.get('class')) > 1 else 'Not Rated'
        product_url = urljoin(BASE_URL + 'catalogue/', product.h3.a['href'])
        image_url = urljoin(BASE_URL, product.find('img')['src'])

        product_list.append([title, price, availability, rating, product_url, image_url])
    
    return product_list

def scrape_site():
    all_products = []
    for page in range(1, 6):
        print(f"🔄 Scraping page {page}...")
        url = CATALOGUE_URL.format(page)
        try:
            response = requests.get(url)
            response.raise_for_status()
        except Exception as e:
            print(f"❌ Error fetching page {page}: {e}")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        all_products.extend(extract_product_data(soup))

    return all_products

def save_to_csv(data, filename='products.csv'):
    print("📁 Writing to CSV...")
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADERS)
            writer.writerows(data)
        print(f"✅ Data saved to '{filename}'")
    except Exception as e:
        print(f"❌ CSV write error: {e}")

if __name__ == '__main__':
    data = scrape_site()
    save_to_csv(data)
