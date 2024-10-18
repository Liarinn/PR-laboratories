import requests
from bs4 import BeautifulSoup
import re

# URL for car listings
url = "https://999.md/ro/list/transport/cars"

# Function to serialize into JSON format (without json library)
def serialize_to_json(products):
    json_str = "[\n"
    for product in products:
        json_str += "  {\n"
        json_str += f'    "name": "{product["name"]}",\n'
        json_str += f'    "price": {product["price"] if product["price"] else "Negotiable"},\n'
        json_str += '    "phone_numbers": [\n'
        for phone in product["phone_numbers"]:
            json_str += f'      "{phone}",\n'
        json_str = json_str.rstrip(",\n") + '\n'  # Remove trailing comma from last phone number
        json_str += '    ],\n'
        json_str += f'    "link": "{product["link"]}"\n'
        json_str += "  },\n"
    json_str = json_str.rstrip(",\n") + '\n'  # Remove trailing comma from last product object
    json_str += "]"
    return json_str

# Function to serialize into XML format
def serialize_to_xml(products):
    xml_str = "<products>\n"
    for product in products:
        xml_str += "  <product>\n"
        xml_str += f'    <name>{product["name"]}</name>\n'
        xml_str += f'    <price>{product["price"] if product["price"] else "Negotiable"}</price>\n'
        xml_str += '    <phone_numbers>\n'
        for phone in product["phone_numbers"]:
            xml_str += f'      <phone>{phone}</phone>\n'
        xml_str += '    </phone_numbers>\n'
        xml_str += f'    <link>{product["link"]}</link>\n'
        xml_str += "  </product>\n"
    xml_str += "</products>"
    return xml_str

try:
    response = requests.get(url)

    if response.status_code == 200:
        print("GET request successful!")

        soup = BeautifulSoup(response.text, 'html.parser')

        products = []

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
                
                # Clean non-breaking space and check for "negociabil" or "1"
                price_str = price_str.replace('\xa0', '').replace(' ', '').strip()
                if "negociabil" in price_str.lower() or price_str == '1':
                    price = None
                else:
                    try:
                        price = float(price_str.replace(',', '.'))
                    except ValueError:
                        price = None

                # Request product page to scrape phone numbers
                product_page = requests.get(link)
                product_soup = BeautifulSoup(product_page.text, 'html.parser')

                # Phone numbers repeat on the product page
                phone_numbers = set()

                # Find all <a> elements with phone numbers in links
                phone_elements = product_soup.select('a[href^="tel:"]')

                # Remove unnecessary phone numbers
                for phone_element in phone_elements:
                    # Extract phone number
                    phone_number = phone_element['href'].replace('tel:', '').strip()  
                    # Exclude the support number "+37322888002" and add unique numbers
                    if phone_number != '+37322888002':
                        phone_numbers.add(phone_number)

                products.append({
                    'name': name,
                    'price': price,
                    'phone_numbers': list(phone_numbers),  # Convert set to list for serialization
                    'link': link
                })
        
        # Perform serialization to JSON
        json_output = serialize_to_json(products)
        print("JSON Output:")
        print(json_output)

        # Perform serialization to XML
        xml_output = serialize_to_xml(products)
        print("\nXML Output:")
        print(xml_output)

    else:
        print(f"GET request failed with status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
