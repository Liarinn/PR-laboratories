import sqlite3
from scrape_car_info import get_car_data 


# Define the function to insert data into the database
def insert_data(name, price, link):
    connection = sqlite3.connect('999_cars.db')
    cursor = connection.cursor()

    # Create tables if they don’t exist
    cursor.execute("""CREATE TABLE IF NOT EXISTS products(
                        product_id INTEGER PRIMARY KEY, 
                        name TEXT)""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS car_info(
                        car_id INTEGER PRIMARY KEY, 
                        product_id INTEGER,
                        car_price FLOAT, 
                        car_link TEXT,
                        FOREIGN KEY(product_id) REFERENCES products(product_id))""")

    # Check if the car name already exists in the 'products' table
    cursor.execute("SELECT product_id FROM products WHERE name = ?", (name,))
    product = cursor.fetchone()
    
    if not product:
        cursor.execute("INSERT INTO products (name) VALUES (?)", (name,))
        product_id = cursor.lastrowid
    else:
        product_id = product[0]

    cursor.execute("INSERT INTO car_info (product_id, car_price, car_link) VALUES (?, ?, ?)",
                   (product_id, price, link))
    connection.commit()
    connection.close()

# Fetch car data and insert each entry into the database
def populate_car_data():
    cars = get_car_data()  # Fetch car data from 999.md
    for car in cars:
        name = car['name']
        price = car['price']
        link = car['link']
        insert_data(name, price, link)  # Insert each car's data
        print(f" Name: {name}, Price: {price} MDL, Link: {link}") 


populate_car_data()

