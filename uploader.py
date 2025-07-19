import requests
import sqlite3
from utils.hasher import generate_hashes
from interact import check_file_exists
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Load secrets from .env
PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_SECRET_API_KEY = os.getenv("PINATA_SECRET_API_KEY")
DEDUP_DB_PATH = "data/dedup_db.sqlite"

# Validate secrets
if not all([PINATA_API_KEY, PINATA_SECRET_API_KEY]):
    raise ValueError("Missing Pinata API keys in .env")

def init_db():
    """Initialize SQLite database for deduplication."""
    conn = sqlite3.connect(DEDUP_DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS files (sha256 TEXT PRIMARY KEY, phash TEXT, file_name TEXT)")
    conn.commit()
    conn.close()

def check_duplicate(file_bytes, file_name):
    """Check for duplicates using SHA-256 and phash."""
    sha256, phash = generate_hashes(file_bytes)
    conn = sqlite3.connect(DEDUP_DB_PATH)
    c = conn.cursor()

    # Check for SHA-256 match
    c.execute("SELECT * FROM files WHERE sha256 = ?", (sha256,))
    if c.fetchone():
        conn.close()
        return True, "Exact duplicate found (SHA-256)", sha256, phash

    # Check for phash match
    if phash:
        c.execute("SELECT phash FROM files")
        for row in c.fetchall():
            stored_phash = row[0]
            if stored_phash:
                hamming_distance = sum(c1 != c2 for c1, c2 in zip(phash, stored_phash))
                if hamming_distance < 10:  # Adjust threshold (5-15)
                    conn.close()
                    return True, f"Visually similar image found (phash, hamming distance: {hamming_distance})", sha256, phash

    # Check smart contract
    exists, message = check_file_exists(sha256, phash)
    if exists:
        conn.close()
        return True, message, sha256, phash

    # Store in local DB
    c.execute("INSERT INTO files (sha256, phash, file_name) VALUES (?, ?, ?)", (sha256, phash, file_name))
    conn.commit()
    conn.close()
    return False, "No duplicates found", sha256, phash

def upload_to_pinata(file_bytes, file_name):
    """Upload file to IPFS via Pinata."""
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