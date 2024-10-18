import json

# Example car data
cars = [
    {
        "name": "Toyota Camry",
        "price": 15000,
        "phone_numbers": ["+123456789"],
        "link": "https://999.md/car1"
    },
    {
        "name": "Honda Accord",
        "price": 12000,
        "phone_numbers": ["+987654321"],
        "link": "https://999.md/car2"
    },
    {
        "name": "Ford Focus",
        "price": 8000,
        "phone_numbers": ["+1122334455"],
        "link": "https://999.md/car3"
    }
]

# Function to serialize into JSON format
def serialize_to_json(cars):
    return json.dumps(cars, indent=2)

# Function to serialize into XML format
def serialize_to_xml(cars):
    xml_str = "<cars>\n"
    for car in cars:
        xml_str += "  <car>\n"
        xml_str += f'    <name>{car["name"]}</name>\n'
        xml_str += f'    <price>{car["price"]}</price>\n'
        xml_str += '    <phone_numbers>\n'
        for phone in car["phone_numbers"]:
            xml_str += f'      <phone>{phone}</phone>\n'
        xml_str += '    </phone_numbers>\n'
        xml_str += f'    <link>{car["link"]}</link>\n'
        xml_str += "  </car>\n"
    xml_str += "</cars>"
    return xml_str

# Perform serialization to JSON
json_output = serialize_to_json(cars)
print("JSON Output:")
print(json_output)

# Perform serialization to XML
xml_output = serialize_to_xml(cars)
print("\nXML Output:")
print(xml_output)
