import requests
import json
import os
import streamlit as st
from utils.hasher import generate_sha256

PINATA_API_KEY = st.secrets["PINATA_API_KEY"]
PINATA_SECRET_API_KEY = st.secrets["PINATA_SECRET_API_KEY"]

DEDUP_DB_PATH = "dedup_db.json"

def load_db():
    if not os.path.exists(DEDUP_DB_PATH):
        return {}
    with open(DEDUP_DB_PATH, 'r') as f:
        return json.load(f)

def save_db(db):
    with open(DEDUP_DB_PATH, 'w') as f:
        json.dump(db, f, indent=4)

def upload_to_pinata(file_bytes, file_name):
    files = {'file': (file_name, file_bytes)}
    headers = {
        'pinata_api_key': PINATA_API_KEY,
        'pinata_secret_api_key': PINATA_SECRET_API_KEY
    }
    res = requests.post("https://api.pinata.cloud/pinning/pinFileToIPFS", files=files, headers=headers)
    if res.status_code == 200:
        return res.json()['IpfsHash']
    else:
        raise Exception(f"Upload failed: {res.text}")
