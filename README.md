# DeduVault: A Decentralized Visual Deduplication Framework using Perceptual Hashing and Blockchain-based IPFS Storage

## 📌 Abstract

DeduVault is a decentralized system designed to detect and eliminate duplicate or near-duplicate image files across cloud platforms. It leverages IPFS for distributed storage, Ethereum smart contracts for integrity and metadata management, and **Perceptual Hashing (pHash)** and **SHA-256** for robust deduplication. The project targets applications in e-commerce where multiple platforms may host visually similar product images.

---

## 🧠 Technologies Used

| Layer         | Tech Stack                           |
| ------------- | ------------------------------------ |
| Frontend      | Streamlit (Python)                   |  
| Backend       | Python, Web3.py, SQLite3             |
| Blockchain    | Solidity, Ethereum (Sepolia testnet) |
| Storage       | IPFS (via Pinata)                    |
| Deduplication | SHA-256, pHash (Perceptual Hashing)  |

---

## ⚙️ System Architecture

```
+--------------+        +--------------------+        +----------------+
|  Streamlit   | <----> |   Flask + Web3.py   | <----> | Ethereum SC    |
|  Frontend UI |        | Backend Logic      |        | (Sepolia)      |
+--------------+        +--------------------+        +----------------+
       |                         |                               |
       |                         V                               |
       |               +------------------+                     |
       +-------------> | IPFS (via Pinata) | <------------------+
                       +------------------+
                               |
                               V
                     +----------------------+
                     | dedup_db.sqlite      |
                     | (local dedup DB)     |
                     +----------------------+
```

---

## 🔍 Deduplication Algorithm

### 1. SHA-256 Hashing

- Generates a hash based on raw file bytes.
- If an exact match is found, it's a duplicate.

### 2. Perceptual Hashing (pHash)

- Used to detect **visually similar images** even if resized, reformatted, or renamed.
- Computes a perceptual hash and compares it against existing entries.
- If the Hamming Distance ≤ threshold (e.g., 5), it's treated as a near-duplicate.

```python
from imagehash import phash
from PIL import Image

# Compute pHash from file
def compute_phash(file_path):
    image = Image.open(file_path)
    return str(phash(image))
```

---

## 🧾 Smart Contract: `DedupStorage.sol`

### 📁 Functions

```solidity
function storeFile(bytes32 sha256Hash, string memory cid) public {}
function fileExists(bytes32 sha256Hash) public view returns (bool) {}
function getFile(bytes32 sha256Hash) public view returns (string memory) {}
```

- Ensures no duplicate SHA-256 entries get re-uploaded.
- IPFS CID is retrieved based on the hash.

### 🔐 Deployment

- Deployed on Sepolia Testnet using Infura and Web3.py
- Verified and interactable via Remix or Etherscan

---

## 🗂️ Database: `dedup_db.sqlite`

### 📐 Schema

```sql
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sha256 TEXT UNIQUE,
    phash TEXT,
    cid TEXT,
    upload_time TEXT
);
```

### 🔍 Sample Queries

- Check SHA duplicate:

```sql
SELECT * FROM files WHERE sha256 = ?;
```

- Find near-duplicates using pHash:

```python
from imagehash import phash
import sqlite3

# Compare pHash distances
cur.execute("SELECT phash, cid FROM files")
for db_phash, cid in cur.fetchall():
    if hamming_distance(input_phash, db_phash) <= 5:
        print("Near duplicate found:", cid)
```

---

## 💻 Streamlit Frontend UI

### 🎨 Features

- Upload image → Check duplicates → View CID/IPFS URL
- Three-column layout (Flipkart, Amazon, Myntra simulation)
- Preview uploaded image if it's new
- Displays status: New file / Duplicate / Near-Duplicate

---

## 🌐 IPFS Upload via Pinata

```python
import requests
headers = {"Authorization": f"Bearer {PINATA_JWT}"}
files = {"file": open(file_path, "rb")}
requests.post(PINATA_URL, headers=headers, files=files)
```

- CID is extracted and stored
- Preview link is shown via IPFS Gateway

---

## ✅ Flow Summary

1. User uploads file via Streamlit
2. Backend computes SHA-256 + pHash
3. Check SQLite DB for SHA and pHash matches
4. If not found → Upload to IPFS via Pinata
5. Store metadata (hashes + CID + time) in `dedup_db.sqlite`
6. Write SHA & CID to Ethereum smart contract
7. Display image + status on UI

---

## 📄 Use Case: E-Commerce Platforms

- Flipkart, Amazon, and Myntra simulation
- Detect if similar images of the same product are being reused
- Prevent redundant uploads and save cloud storage

---



## 🚀 Future Enhancements

- Integrate MongoDB or PostgreSQL for larger scale
- Add image classification (product category prediction)
- Enable user authentication with MetaMask



