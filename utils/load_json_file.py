import json

async def load_json_file(filePath: str):
    with open(filePath, 'r') as file:
        return json.load(file)