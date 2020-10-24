import requests
from bs4 import BeautifulSoup
import pandas as pd

#python credentials to access the website
mainURL = 'https://www.zoopla.co.uk'
agent = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"}

#An array to store all houses link
houselinks = []

#A loop to go through the zoopla pages looking for the houses link
for x in range(1, 3):
    url = f"https://www.zoopla.co.uk/for-sale/property/london/?identifier=london&q=London&radius=0&pn={x}"
    r = requests.get(url, headers=agent)
    soup = BeautifulSoup(r.content, "lxml")
    zooplaLink = soup.find_all('h2', class_='listing-results-attr')
    for item in zooplaLink:
        for link in item.find_all('a', href=True):
            houselinks.append(mainURL + link['href']) 

houses = []

#A loop that goes through every link found
for links in houselinks:
    try:
        r = requests.get(links, headers=agent)
        soup = BeautifulSoup(r.content, 'lxml')

        name = soup.find('h1', class_='ui-property-summary__title ui-title-subgroup').text.strip()
        price = soup.find('p', class_='ui-pricing__main-price ui-text-t4').text.strip()
        address = soup.find('h2', class_='ui-property-summary__address').text.strip()
        description = soup.find('div', class_='dp-description__text').text.strip()

        house = {
            'name': name,
            'price': price,
            'address': address,
            'description': description
        }
    except:
       pass


    houses.append(house)


# Panda frame work and .csv write
dataFrame = pd.DataFrame(houses)
print(dataFrame.head(3))
dataFrame.to_csv('/Users/leonardosaeta/Desktop/data.csv')
