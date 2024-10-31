import requests
from bs4 import BeautifulSoup
import re 

def get_car_data():
    url = "https://999.md/ro/list/transport/cars"
    eur_exchange_rate = 19.34
    dolar_exchange_rate = 17.69

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            products = []

            currency_conversion = {
                '€': eur_exchange_rate, 
                '$': dolar_exchange_rate,  
                'MDL': 1.0  
            }

            def clean_and_convert_price(price_str):
                price_str = price_str.replace('\xa0', '').replace(' ', '').strip()
                if "negociabil" in price_str.lower() or price_str == '1':
                    return None
                currency_match = re.search(r'[€$]', price_str)
                if currency_match:
                    symbol = currency_match.group(0)
                    amount = price_str.replace(symbol, '')
                    try:
                        price = float(amount.replace(',', '.')) * currency_conversion.get(symbol, 1.0)
                    except ValueError:
                        return None
                else:
                    try:
                        price = float(price_str.replace(',', '.'))
                    except ValueError:
                        return None
                return price

            for item in soup.find_all('li', class_='ads-list-photo-item'):
                title_div = item.find('div', class_='ads-list-photo-item-title')
                price_div = item.find('div', class_='ads-list-photo-item-price')

                if title_div and price_div:
                    link = 'https://999.md' + title_div.find('a', class_='js-item-ad')['href']
                    name = title_div.find('a', class_='js-item-ad').text.strip()
                    name = re.sub(r',\s*\d{4}\s*an', '', name).strip()
                    price_str = price_div.find('span', class_='ads-list-photo-item-price-wrapper').text.strip()
                    price = clean_and_convert_price(price_str)

                    products.append({
                        'name': name,
                        'price': price,
                        'link': link
                    })
            return products
        else:
            print(f"GET request failed with status code: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []