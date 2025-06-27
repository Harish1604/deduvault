import requests
import json
import os
from utils.hasher import generate_sha256

PINATA_API_KEY = '<YOUR PINATA_API_KEY>'
PINATA_SECRET_API_KEY = '<YOUR PINATA_SECRET_API_KEY>'
DEDUP_DB_PATH = '<YOUR dedup_db.json PATH>'

def load_db():
    if not os.path.exists(DEDUP_DB_PATH):
        return {}
    with open(DEDUP_DB_PATH, 'r') as f:
        return json.load(f)

def save_db(db):
    with open(DEDUP_DB_PATH, 'w') as f:
        json.dump(db, f, indent=4)

def upload_to_pinata(file_bytes, file_name):
    files = {
        'file': (file_name, file_bytes)
    }

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
        with open(file_path, 'rb') as f:
            file_bytes = f.read()
        cid = upload_to_pinata(file_bytes, os.path.basename(file_path))
        db[hash_val] = cid
        save_db(db)
        print("File uploaded. CID stored.")

    return hash_val, cid
