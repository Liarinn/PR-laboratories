import requests
from bs4 import BeautifulSoup

# Replace with the URL you want to GET
url = "https://999.md/"

try:
    # Send a GET request
    response = requests.get(url)

    # Check the status code
    if response. status_code == 200:
        print ("GET request successful!")

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser' )

        # Example: Extract and print the page title
        page_title = soup.title.string
        print (f"Page Title: {page_title}")
        # You can further parse and extract data from the HTML as needed
    
    else:
        print(f"GET request failed with status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
