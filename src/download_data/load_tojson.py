import zipfile
import json
from datetime import datetime

def load2json(filename):
    with zipfile.ZipFile(filename, 'r') as z:
        z.extractall(f'../../data/raw')

    train_data = []
    for line in open(f'../../data/raw/train_data.jsonl', "r"):
        train_data.append(json.loads(line))
    print("Loaded {} train conversations".format(len(train_data)))

    test_data = []
    for line in open(f'../../data/raw/test_data.jsonl', "r"):
        test_data.append(json.loads(line))
    print("Loaded {} test conversations".format(len(test_data)))

if __name__ == "__main__":
    current_date = datetime.now().strftime("%Y-%m-%d")
    filename = f'../../data/raw/redial_dataset_{current_date}.zip'
    load2json(filename)