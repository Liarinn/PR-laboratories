import requests
from bs4 import BeautifulSoup

url = "https://999.md/ro/list/transport/cars"

"""

<li class="ads-list-photo-item " data-index="28">
<div class="ads-list-photo-item-title ">
<a class="js-item-ad " href="/ro/87937151">Renault Kadjar, 2020 an</a>
</div>
<div class="ads-list-photo-item-price">
<span class="ads-list-photo-item-price-wrapper">16 950 €</span>
</div>
</li>
"""

try:
    response = requests.get(url)

    if response. status_code == 200:
        print ("GET request successful!")

        soup = BeautifulSoup(response.text, 'html.parser' )

        products = []

        # All products are stored in lists 'ads-list-photo-item'
        for item in soup.find_all('li', class_='ads-list-photo-item'):
            title_div = item.find('div', class_='ads-list-photo-item-title')
            price_div = item.find('div', class_='ads-list-photo-item-price')

            if title_div and price_div:
                # Extract link
                link = title_div.find('a', class_='js-item-ad')['href']
                
                # Extract name
                name = title_div.find('a', class_='js-item-ad').text.strip()
                
                # Extract price
                price_str = price_div.find('span', class_='ads-list-photo-item-price-wrapper').text.strip()
                
                # Check if the price is "negociabil"
                if "negociabil" in price_str.lower():
                    price = None  # Set price to None for negotiable prices
                else:
                    # Convert price to float
                    price = float(price_str.replace('€', '').replace(' ', '').replace(',', '.')) 

                products.append({
                    'name': name,
                    'price': price,
                    'link': link
            })
        for product in products:
            print(f"Name: {product['name']}, Price: {product['price']} EUR, Link: {product['link']}")

    
    else:
        print(f"GET request failed with status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
