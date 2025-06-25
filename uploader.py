import requests
import json
import os
from utils.hasher import generate_sha256

PINATA_API_KEY = '7d3ff616e7e5bcb971ff'
PINATA_SECRET_API_KEY = 'f93c663255ad4707db00a365807690b721f40b23537a62362895d7178e4ed225'
DEDUP_DB_PATH = r'C:\Users\jhari\Desktop\data\dedup-ipfs-ui\dedup_db.json'


def load_db():
    if not os.path.exists(DEDUP_DB_PATH):
        return {}
    with open(DEDUP_DB_PATH, 'r') as f:
        return json.load(f)

def save_db(db):
    with open(DEDUP_DB_PATH, 'w') as f:
        json.dump(db, f, indent=4)

def upload_to_pinata(file_path):
    file_name = os.path.basename(file_path)
    with open(file_path, 'rb') as f:
        files = {'file': (file_name, f)}
        headers = {
            'pinata_api_key': PINATA_API_KEY,
            'pinata_secret_api_key': PINATA_SECRET_API_KEY
        }
        res = requests.post("https://api.pinata.cloud/pinning/pinFileToIPFS", files=files, headers=headers)
        if res.status_code == 200:
            return res.json()['IpfsHash']
        else:
            raise Exception(f"Upload failed: {res.text}")

def process_file(file_path, description=""):
    hash_val = generate_sha256(file_path, description)
    db = load_db()

    if hash_val in db:
        cid = db[hash_val]
        print("Duplicate detected. Using existing CID.")
    else:
        cid = upload_to_pinata(file_path)
        db[hash_val] = cid
        save_db(db)
        print("File uploaded. CID stored.")

    return hash_val, cid
