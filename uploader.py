import requests
import json
import os
from utils.hasher import generate_sha256

PINATA_API_KEY = '27d4d8e05c46c9665df2'
PINATA_SECRET_API_KEY = '437a81c9fa70e01672ab63cd80e823620968e7908777a632ea658886c544d3e1'
DEDUP_DB_PATH = r'C:\Users\jhari\Desktop\data\Decentralized-Deduplication\dedup_db.json'

def load_db():
    if not os.path.exists(DEDUP_DB_PATH):
        return {}
    with open(DEDUP_DB_PATH, 'r') as f:
        return json.load(f)

def save_db(db):
    try:
        os.makedirs(os.path.dirname(DEDUP_DB_PATH), exist_ok=True)  # 🔧 ensure the path exists
        with open(DEDUP_DB_PATH, 'w') as f:
            json.dump(db, f, indent=4)
        print("✅ DB saved successfully.")
    except Exception as e:
        print("❌ Failed to save DB:", e)



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
    print(f"\n🔍 Processing: {file_path}")

    # Generate the hash
    hash_val = generate_sha256(file_path, description)
    print(f"🔑 Hash generated: {hash_val}")

    # Load the DB
    db = load_db()
    print(f"📖 DB Loaded: {len(db)} entries")
    print("🧠 DB Snapshot:", json.dumps(db, indent=2))

    # Check for hash in DB
    if hash_val in db:
        cid = db[hash_val]
        print("🧪 Found in DB. CID:", cid)

       
    else:
        print("📤 Uploading to Pinata...")
        try:
            with open(file_path, 'rb') as f:
                file_bytes = f.read()

            cid = upload_to_pinata(file_bytes, os.path.basename(file_path))
            print("✅ Uploaded to Pinata. CID:", cid)

            # Save to DB
            db[hash_val] = cid
            print("💾 Saving new entry to DB...")
            try:
                save_db(db)
                print("✅ DB saved successfully.")
            except Exception as e:
                print("❌ DB save failed:", e)
                return None, None

        except Exception as e:
            print("❌ Upload failed:", e)
            return None, None

    return hash_val, cid


