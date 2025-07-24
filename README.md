# DeduVault

**DeduVault: A Decentralized Visual Deduplication Framework using Perceptual Hashing and Blockchain-based IPFS Storage**

## 📌 Abstract

DeduVault is a decentralized framework designed to prevent duplicate image storage using a blend of perceptual hashing (phash), IPFS for decentralized storage, and Ethereum smart contracts. It offers an intelligent solution for deduplication by identifying visually similar images, even if altered (resized, renamed, or compressed), and verifying uniqueness before committing them to the blockchain ledger and IPFS.

## 🛠️ Tech Stack

- **Frontend/UI**: Python + Streamlit
- **Backend**: Python (web3.py, imagehash, hashlib, sqlite3)
- **Blockchain**: Solidity smart contract on Sepolia Testnet
- **Decentralized Storage**: IPFS via Pinata and Infura
- **Deduplication**: Perceptual Hashing (phash), SHA-256 for file-level integrity
- **Database**: SQLite for local metadata storage (`dedup_db.sqlite`)

## 🧠 Key Features

- ✅ Visual deduplication using **phash** (detects similar images)
- ✅ Secure storage with **IPFS** via Pinata
- ✅ Duplicate verification with **SHA-256** and SQLite
- ✅ On-chain verification via **Ethereum Smart Contracts**
- ✅ Beautiful **e-commerce style UI** to preview image listings (Flipkart, Amazon, Myntra)
- ✅ Streamlit secrets for secure key handling

## 🔍 What is Perceptual Hashing (phash)?

Unlike cryptographic hashes (like SHA-256), which change completely even if one pixel is modified, **perceptual hashing (phash)** generates a fingerprint based on an image’s *visual appearance*. It allows us to detect duplicates that are:

- Slightly resized or compressed
- Renamed or re-encoded (JPEG/PNG)
- Brightness/contrast adjusted

### 🔬 How it works (Simplified):
1. Resize the image to a small grayscale version (e.g., 32x32)
2. Apply Discrete Cosine Transform (DCT) to capture frequency components
3. Extract a fingerprint (hash) from top-left DCT values
4. Compare hashes using **Hamming Distance** — small distance = visually similar

This makes phash **perfect for visual deduplication** in DeduVault.

## 🖼️ System Workflow

1. **Upload Image**
2. Compute **SHA-256** and **Perceptual Hash**
3. Check for duplicates locally (`dedup_db.sqlite`) and on blockchain
4. If unique, upload to **IPFS** and store **CID + Hashes** in Smart Contract
5. Display result in UI with platform-styled previews

## 🔗 Smart Contract (`DedupStorage.sol`)

- `storeFile(hash, cid)` – stores hash and IPFS CID
- `fileExists(hash)` – checks if a hash is already stored
- `getFile(hash)` – retrieves CID for a hash

Deployed on Sepolia Ethereum Testnet, integrated via `web3.py` and Infura.


## 🛡️ Security

- Uses **Streamlit Secrets Manager** for API keys & Infura credentials.
- No hardcoded keys or sensitive data.

## 🧪 Sample Output

When uploading an image, the system detects duplicates visually and shows:

- ✅ *"Image already exists (visually similar)"* – if phash matches
- ✅ *"New image stored on IPFS and blockchain"* – if unique

## 📸 Demo UI

Streamlit UI displays image in 3-column layout (Amazon, Flipkart, Myntra themes).



## 🧑‍💻 Author

**Harish J** and **Venkatesh K** — Third year Computer Science students, Blockchain & Cloud Enthusiast.

---

> For more details or collaboration, visit: [Portfolio](https://harishx64.vercel.app)