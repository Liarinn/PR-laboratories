import sqlite3

connection = sqlite3.connect('999_cars.db')

cursor = connection.cursor()

command1 = """CREATE TABLE IF NOT EXISTS
products(product_id INTEGER PRIMARY KEY, name TEXT)"""

cursor. execute(command1)

command2 = """CREATE TABLE IF NOT EXISTS
car_info(car_id INTEGER PRIMARY KEY, car_price FLOAT, car_link ,
FOREIGN KEY(product_id) REFERENCES products(product_id))"""

cursor.execute(command2)

cursor.execute("SELECT * FROM car_info")

results = cursor.fetchall()
print(results)

