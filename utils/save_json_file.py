import os

def save_json_file(path: str, fileName: str, result: str):
    directory = os.path.dirname(path + '/' + fileName)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(path + '/' + fileName + '.json', 'w') as f:
        f.write(result)