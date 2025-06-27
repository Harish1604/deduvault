# 🔒 DeduVault

**Decentralized Image Deduplication Platform using IPFS & Blockchain**

> Secure your digital assets, detect duplicates instantly, and visualize content across platforms — all powered by Web3.

---

## 🚀 Overview

**DeduVault** is a next-generation image deduplication and asset verification system. Built with **IPFS**, **Blockchain**, and **Streamlit**, it allows users to:

- Upload image files.
- Generate a **SHA-256 hash**.
- Store them on **IPFS via Pinata**.
- Check for duplicates using **on-chain verification**.
- **Register new files** on the blockchain using smart contracts.
- Visualize product listings on **Flipkart, Amazon, and Myntra**-like previews.

---

## 🌐 Live Tech Stack

| Layer            | Tech Used                                    |
|------------------|----------------------------------------------|
| 💻 Frontend      | Streamlit + HTML/CSS                         |
| 🧠 Hashing       | SHA-256 (Python `hashlib`)                   |
| 📦 File Storage  | IPFS via Pinata                              |
| 🔗 Blockchain    | Ethereum (Testnet) + Web3.py                 |
| 📃 Smart Contract| Solidity (Deployed via Remix IDE)           |
| 🧠 Backend Logic | Python (`interact.py`, `uploader.py`)        |
| 🔍 Data Format   | JSON (for file metadata, local DB)           |

---

## 📸 Features

- 🔐 **Cryptographic Security** – Unique SHA-256 hashing per image
- 🌐 **IPFS Integration** – Decentralized, content-addressed storage
- ⛓️ **Blockchain Verification** – Smart contract-based deduplication check
- ⚡ **Real-time Detection** – Alerts on existing duplicates
- 🛍️ **Cross-platform Visualization** – See how your product looks on Flipkart, Amazon & Myntra
- 📊 **Live Metrics Dashboard** – Uptime, response time, encryption stats

---

## 📂 File Structure
<pre>```bash
📁 Decentralized-Deduplication/
├── contracts/
│   ├── DedupStorage.sol         # Solidity Smart Contract
│   └── DedupStorage_abi.json    # Compiled ABI for contract interaction
│
├── utils/
│   ├── hasher.py                # SHA-256 hash generation
│   └── dedup_db.json            # Local deduplication DB (hash → CID)
│
├── hash.py                      # Alternative hashing logic (if needed)
├── interact.py                  # Web3 interaction with smart contract
├── main.py                      # Optional main entry (legacy/dev)
├── streamlit_app.py             # Streamlit frontend app
├── uploader.py                  # Upload file to Pinata & manage dedup
├── wallet.env                   # Environment vars (wallet keys, etc.)
├── requirements.txt             # Python dependencies
└── README.md                    # Documentation

</pre>
---

## 🧪 Smart Contract Overview

- **Name**: `DedupStorage.sol`
- **Functions**:
  - `storeFile(string memory fileHash, string memory cid)`
  - `fileExists(string memory fileHash) public view returns (bool)`
  - `getFile(string memory fileHash) public view returns (FileData)`
- **Chain**: Ethereum (e.g., Sepolia / Polygon Mumbai / Amoy)
- **Deployed Using**: Remix IDE

---

## 🧠 How It Works

### 🔁 Workflow

1. **Upload** your image via the Streamlit UI
2. A **SHA-256 hash** is generated locally
3. File is uploaded to **IPFS using Pinata API**
4. The app checks if the file hash **already exists** on the blockchain
5. If not found, the hash and CID are **stored on-chain** using a smart contract
6. You get a **confirmation + IPFS link** and deduplication feedback

---

## 🛠️ Installation Guide

### 🐍 Requirements

- Python 3.8+
- `pip` for dependency management

### 🔧 Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/deduvault.git
   cd deduvault
   
2. **Install dependencies**
   ```bash
    pip install -r requirements.txt

3. **Configure your API keys**
    In uploader.py, replace your Pinata APIs:
   
      PINATA_API_KEY = '<YOUR PINATA_API_KEY>'
   
      PINATA_SECRET_API_KEY = '<YOUR PINATA_SECRET_API_KEY>'
      
   
      In interact.py, set up your Infura / Ankr RPC endpoint and contract info:
   
      w3 = Web3(Web3.HTTPProvider("https://sepolia.infura.io/v3/YOUR_INFURA_KEY"))

   
5. **Run the Streamlit app**
   ```bash
    streamlit run streamlit_app.py
