import requests
from bs4 import BeautifulSoup
import re 
import functools
from datetime import datetime
import pytz  # For UTC timestamp

url = "https://999.md/ro/list/transport/cars"

eur_exchange_rate = 19.34
dolar_exchange_rate = 17.69

try:
    response = requests.get(url)

    if response. status_code == 200:
        print ("GET request successful!")

        soup = BeautifulSoup(response.text, 'html.parser' )

        products = []

        currency_conversion = {
            '€': eur_exchange_rate, 
            '$': dolar_exchange_rate,  
            'MDL': 1.0  
        }

        # Function to clean and convert the price
        def clean_and_convert_price(price_str):
            # Clean non-breaking space, not to get errors
            price_str = price_str.replace('\xa0', '').replace(' ', '').strip()  
            
            # Check if the price is "negociabil" or "1" 
            if "negociabil" in price_str.lower() or price_str == '1':
                return None
            
            # Handle price with currency symbol
            currency_match = re.search(r'[€$]', price_str)
            if currency_match:
                symbol = currency_match.group(0)
                amount = price_str.replace(symbol, '')
                
                try:
                    price = float(amount.replace(',', '.')) * currency_conversion.get(symbol, 1.0)
                except ValueError:
                    return None  
            else:
                # For MDL
                try:
                    price = float(price_str.replace(',', '.'))
                except ValueError:
                    return None

            return price
        


        # All products are stored in lists 'ads-list-photo-item'
        for item in soup.find_all('li', class_='ads-list-photo-item'):
            title_div = item.find('div', class_='ads-list-photo-item-title')
            price_div = item.find('div', class_='ads-list-photo-item-price')

            if title_div and price_div:
                # Extract full link
                link = 'https://999.md' + title_div.find('a', class_='js-item-ad')['href']
                
                # Extract name
                name = title_div.find('a', class_='js-item-ad').text.strip()
                
                # Remove year from name
                name = re.sub(r',\s*\d{4}\s*an', '', name).strip()  
        
                # Extract price
                price_str = price_div.find('span', class_='ads-list-photo-item-price-wrapper').text.strip()
                
                price = clean_and_convert_price(price_str)

                # Request at product page to scrape phone numbers
                product_page = requests.get(link)
                product_soup = BeautifulSoup(product_page.text, 'html.parser')

                # Phone numbers repeat on the product page
                phone_numbers = set()

                # Find all <a> elements with phone numbers in links
                phone_elements = product_soup.select('a[href^="tel:"]')

                # Remove unecessary phone numbers
                for phone_element in phone_elements:
                    # Extract phone number
                    phone_number = phone_element['href'].replace('tel:', '').strip()  
                    # Exclude the support number "+37322888002" and add unique numbers
                    if phone_number != '+37322888002':
                        phone_numbers.add(phone_number)
            

                products.append({
                    'name': name,
                    'price': price,
                    'phone_numbers': phone_numbers,
                    'link': link
            })
        for product in products:
            price_display = product['price'] if product['price'] is not None else "Negotiable"
            phones = ", ".join(product['phone_numbers']) if product['phone_numbers'] else "No phone available"
            print(f"Name: {product['name']}, Price: {price_display} MDL, Phone(s): {phones}, Link: {product['link']}")

        # Convert prices to dollars
        def convert_price_dolar(product):
            if product['price'] is not None:
                product['price_dolar'] = product['price'] / dolar_exchange_rate
                return product
            return None

        # Convert prices and filter products
        products_with_dolar_prices = list(filter(None, map(convert_price_dolar, products)))

        # Cars for poor students
        min_price = 0
        max_price = 3500

        # Filter products within the price range
        products_filtered = list(filter(lambda product: product['price_dolar'] is not None and min_price <= product['price_dolar'] <= max_price, products_with_dolar_prices))

        # Sum the prices of filtered products
        total_price = functools.reduce(lambda acc, product: acc + product['price_dolar'], products_filtered, 0)

        # Attach sum and products to a new data structure
        final_data = {
            'cheap_products': products_filtered,
            'total_price_dolar': total_price,
            'timestamp': datetime.now(pytz.utc).strftime('%Y-%m-%d %H:%M:%S UTC')  # Attach UTC timestamp
        }

        # Output cheap car data
        print(f"Total price of filtered products: {final_data['total_price_dolar']} $")
        print(f"UTC Timestamp: {final_data['timestamp']}")
        print("Filtered Products:")
        for product in final_data['cheap_products']:
            print(f"Name: {product['name']}, Price: {product['price_dolar']} $, Link: {product['link']}")


       
            
    else:
        print(f"GET request failed with status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
