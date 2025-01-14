import requests
from bs4 import BeautifulSoup
import csv

# List of news URLs
urls = [
    "https://top-channel.tv/2025/01/14/kater-angleze-fajtore-per-vrasjen-e-shqiptarit-nga-kopliku-mesazhet-ne-telefonin-e-viktimes-zbuluan-perfshirjen-ne-trafikun-e-droges/",
    "https://top-channel.tv/2025/01/14/lekundje-termeti-ne-vend-ja-sa-ishte-magnitudaw/",
    "https://top-channel.tv/2025/01/14/cilin-politikan-besojne-shqiptaret-me-shume-sondazhi-i-institutit-republikan-amerikan-rama-kryeson-me-35-berisha-14wsy/",
    "https://top-channel.tv/2025/01/14/pak-dite-para-lenies-se-mandatit-biden-pritet-te-heqe-kuben-nga-lista-e-shteteve-sponsorizuese-te-terrorizmit/",
    "https://top-channel.tv/2025/01/14/vucic-do-te-mase-mbeshtetjen-e-popullit-ndaj-tij-i-kerkon-opozites-referendum/",
    "https://top-channel.tv/2025/01/14/fiks-fare-e-gjeten-hajdutin-e-naftes-gabimet-e-albpetrolit-dhe-tatimeve-lene-pa-pension-70-vjecarins/"
]

def extract_news_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            title_element = soup.find('h1')
            title = title_element.text.strip() if title_element else "Not Found"

            categories_element = soup.find('div', class_='categories')
            if categories_element:
                categories = ", ".join([cat.text.strip() for cat in categories_element.find_all('a')])
            else:
                categories = "Not Found"

            first_paragraph_element = soup.find('div', class_='firstP')
            first_paragraph = first_paragraph_element.text.strip() if first_paragraph_element else "Not Found"

            return [title, categories, first_paragraph]
        else:
            print(f"Error fetching {url}. Status code: {response.status_code}")
            return ["Error", "Error", "Error"]
    except Exception as e:
        print(f"An error occurred while processing {url}: {e}")
        return ["Error", "Error", "Error"]

csv_filename = "latest_news.csv"
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Title', 'Categories', 'First Paragraph'])

    for url in urls:
        print(f"Processing {url}...")
        news_data = extract_news_data(url)
        writer.writerow(news_data)

print(f"All data extracted and saved to {csv_filename}!")
