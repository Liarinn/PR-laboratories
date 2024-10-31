import re

def deserialize(serialized):
    # Regex patterns for different data types
    dict_pattern = r'D\{(.*)\}'
    list_pattern = r'L\[(.*)\]'
    int_pattern = r'I\((\d+)\)'
    str_pattern = r'S\(([^)]+)\)'
    bool_pattern = r'B\((true|false)\)'

    # Deserialize dictionary
    if re.match(dict_pattern, serialized):
        inner_content = re.match(dict_pattern, serialized).group(1)
        items = split_items(inner_content)
        result = {}
        for item in items:
            key, value = item.split(':', 1)  # Split only on the first colon
            result[key] = deserialize(value)
        return result

    # Deserialize list
    elif re.match(list_pattern, serialized):
        inner_content = re.match(list_pattern, serialized).group(1)
        items = split_items(inner_content)
        return [deserialize(item) for item in items]

    # Deserialize integer
    elif re.match(int_pattern, serialized):
        return int(re.match(int_pattern, serialized).group(1))

    # Deserialize string
    elif re.match(str_pattern, serialized):
        return re.match(str_pattern, serialized).group(1)

    # Deserialize boolean
    elif re.match(bool_pattern, serialized):
        return re.match(bool_pattern, serialized).group(1) == 'true'

    else:
        raise ValueError(f"Unsupported serialized format: {serialized}")

def split_items(content):
    """Helper function to split dictionary or list items correctly."""
    items = []
    depth = 0
    item = []
    for char in content:
        if char in '{[':
            depth += 1
        elif char in '}]':
            depth -= 1
        if char == ';' and depth == 0:
            items.append(''.join(item).strip())
            item = []
        else:
            item.append(char)
    if item:
        items.append(''.join(item).strip())
    return items

def serialize(data):
    if isinstance(data, dict):
        # Dictionary
        serialized_items = [f"{key}:{serialize(value)}" for key, value in data.items()]
        return f"D{{{'; '.join(serialized_items)}}}"
    elif isinstance(data, list):
        # List
        serialized_items = [serialize(item) for item in data]
        return f"L[{'; '.join(serialized_items)}]"
    elif isinstance(data, int):
        # Integer
        return f"I({data})"
    elif isinstance(data, float):
        # Float
        return f"F({data})"
    elif isinstance(data, str):
        # String
        return f"S({data})"
    elif isinstance(data, bool):
        # Boolean
        return f"B({str(data).lower()})"
    else:
        raise TypeError(f"Unsupported data type: {type(data)}")


# Test data to serialize
test_data = {
    "user": {
        "name": "Riri",
        "age": 16,
        "email": "riri@example.com"
    },
    "numbers": [1, 2, 3, 44],
    "description": {
        "gender": [True],
        "preferences": ["music", "reading"]
    },
    "constcomplexData" : {
    "name": "1984 (Wordsworth Classics)",
    "price": [6.46, 7.56],
    "details": {
        "currency": "USD",
        "availability": [True]
    }
    }
}


serialized = serialize(test_data)
print("Serialized Data:", serialized)


serialized = "D{user:D{name:S(Riri); age:I(16); email:S(riri@example.com);}; numbers:L[I(1); I(2); I(3); I(4);]; description:D{gender:L[B(true)]; preferences:L[S(music); S(reading);];};}"
deserialized = deserialize(serialized)
print("Deserialized Data:", deserialized)
