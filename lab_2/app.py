from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from pydantic import BaseModel
from typing import List
import sqlite3
import json

app = FastAPI()

# File Upload Route
@app.post("/upload-json/")
async def upload_json(file: UploadFile = File(...)):
    # Check if the uploaded file is a JSON file
    if file.content_type != "application/json":
        raise HTTPException(status_code=400, detail="Only JSON files are allowed.")
    
    # Read and decode the file contents
    content = await file.read()
    
    # Attempt to parse the JSON content
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format.")
    
    # Return the parsed data for confirmation
    return {"filename": file.filename, "content": data}

# Define a data model for API requests
class CarRequest(BaseModel):
    name: str
    price: float
    link: str

# Define a data model for API responses
class CarResponse(BaseModel):
    name: str
    price: float
    link: str

# CRUD operations
@app.post("/create")
def create_record(request: CarRequest):
    connection = sqlite3.connect('999_cars.db')
    cursor = connection.cursor()
    
    # Insert into products table
    cursor.execute("INSERT INTO products (name) VALUES (?)", (request.name,))
    product_id = cursor.lastrowid
    
    # Insert into car_info table
    cursor.execute("INSERT INTO car_info (product_id, car_price, car_link) VALUES (?, ?, ?)", 
                   (product_id, request.price, request.link))
    
    connection.commit()
    connection.close()
    return {"message": "Record created successfully", "product_id": product_id}

@app.get("/read", response_model=List[CarResponse])
def read_record(offset: int = Query(0, ge=0), limit: int = Query(5, gt=0)):
    connection = sqlite3.connect('999_cars.db')
    cursor = connection.cursor()
    
    # Query with pagination
    cursor.execute("""
        SELECT products.name, car_info.car_price, car_info.car_link
        FROM products
        JOIN car_info ON products.product_id = car_info.product_id
        LIMIT ? OFFSET ?
    """, (limit, offset))
    
    cars = cursor.fetchall()
    connection.close()
    
    # Format the result as a list of CarResponse objects
    return [{"name": car[0], "price": car[1], "link": car[2]} for car in cars]

@app.put("/update")
def update_record(id: int, request: CarRequest):
    connection = sqlite3.connect('999_cars.db')
    cursor = connection.cursor()
    
    # Update records in both tables
    cursor.execute("UPDATE products SET name = ? WHERE product_id = ?", (request.name, id))
    cursor.execute("UPDATE car_info SET car_price = ?, car_link = ? WHERE product_id = ?", 
                   (request.price, request.link, id))
    
    connection.commit()
    connection.close()
    return {"message": "Record updated successfully"}

@app.delete("/delete")
def delete_record(id: int):
    connection = sqlite3.connect('999_cars.db')
    cursor = connection.cursor()
    
    # Delete from both tables
    cursor.execute("DELETE FROM car_info WHERE product_id = ?", (id,))
    cursor.execute("DELETE FROM products WHERE product_id = ?", (id,))
    
    connection.commit()
    connection.close()
    return {"message": "Record deleted successfully"}
