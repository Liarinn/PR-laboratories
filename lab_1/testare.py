# Example car data
cars = [
    {
        "name": "Nissan Qashqai",
        "price": 240783,
        "phone_numbers": ["+37379700716", "+37379700393"],
        "link": "https://999.md/ro/2184846"
    },
    {
        "name": "Toyota Prius",
        "price": 134413,
        "phone_numbers": ["+37376599504"],
        "link": "https://999.md/ro/88049023"
    },
    {
        "name": "Ford Focus",
        "price": 206938,
        "phone_numbers": ["+37368100936", "+1122334455"],
        "link": "https://999.md/ro/87896622"
    }
]

# Function to serialize into JSON format (without json library)
def serialize_to_json(cars):
    json_str = "[\n"
    for car in cars:
        json_str += "  {\n"
        json_str += f'    "name": "{car["name"]}",\n'
        json_str += f'    "price": {car["price"]},\n'
        json_str += '    "phone_numbers": [\n'
        for phone in car["phone_numbers"]:
            json_str += f'      "{phone}",\n'
        json_str = json_str.rstrip(",\n") + '\n'  # Remove trailing comma from last phone number
        json_str += '    ],\n'
        json_str += f'    "link": "{car["link"]}"\n'
        json_str += "  },\n"
    json_str = json_str.rstrip(",\n") + '\n'  # Remove trailing comma from last car object
    json_str += "]"
    return json_str

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
