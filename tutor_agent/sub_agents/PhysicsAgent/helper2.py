import json

import os
def find_constant(query: str) -> dict:
    print(query)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    role_path = os.path.join(current_dir, "constants.json", )
    with open(role_path, "r") as f:
        constants= json.load(f)
    query = query.lower().strip()
    
    for name, details in constants.items():
        if query == name.lower() or query == details["symbol"].lower():
            return {
                "name": name.replace("_", " ").capitalize(),
                "symbol": details["symbol"],
                "value": details["value"],
                "unit": details["unit"],
                "description": details["description"]
            }
    return None
