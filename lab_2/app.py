from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Define the data model for requests
class CarRequest(BaseModel):
    name: str
    price: float
    link: str

# Database setup and helper functions
def get_db_connection():
    connection = sqlite3.connect('999_cars.db')
    connection.row_factory = sqlite3.Row  # Allows retrieval of results as dictionaries
    return connection

# CRUD Operations

# Create a new car entry
@app.post("/create")
def create_record(request: CarRequest):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Insert data
    cursor.execute("INSERT INTO products (name) VALUES (?)", (request.name,))
    product_id = cursor.lastrowid

    cursor.execute("INSERT INTO car_info (product_id, car_price, car_link) VALUES (?, ?, ?)",
                   (product_id, request.price, request.link))
    connection.commit()
    connection.close()
    return {"message": "Car record created successfully", "id": product_id}

# Read a car record by ID
@app.get("/read/{id}")
def read_record(id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Fetch the car details
    cursor.execute("""
        SELECT products.name, car_info.car_price, car_info.car_link 
        FROM car_info 
        JOIN products ON car_info.product_id = products.product_id 
        WHERE car_info.car_id = ?
    """, (id,))
    car = cursor.fetchone()
    connection.close()
    
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    
    return {
        "name": car["name"],
        "price": car["car_price"],
        "link": car["car_link"]
    }

# Update a car record by ID
@app.put("/update/{id}")
def update_record(id: int, request: CarRequest):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Update the car details
    cursor.execute("""
        UPDATE products 
        SET name = ? 
        WHERE product_id = (SELECT product_id FROM car_info WHERE car_id = ?)
    """, (request.name, id))
    cursor.execute("""
        UPDATE car_info 
        SET car_price = ?, car_link = ? 
        WHERE car_id = ?
    """, (request.price, request.link, id))
    connection.commit()
    connection.close()
    
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Car not found")
    
    return {"message": "Car record updated successfully"}

# Delete a car record by ID
@app.delete("/delete/{id}")
def delete_record(id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Delete the car entry
    cursor.execute("DELETE FROM car_info WHERE car_id = ?", (id,))
    connection.commit()
    
    if cursor.rowcount == 0:
        connection.close()
        raise HTTPException(status_code=404, detail="Car not found")

    # Delete from products table if no other car_info references it
    cursor.execute("""
        DELETE FROM products 
        WHERE product_id NOT IN (SELECT product_id FROM car_info)
    """)
    connection.commit()
    connection.close()
    
    return {"message": "Car record deleted successfully"}
