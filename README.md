# 🗃️ Blockchain-Based File Deduplication using IPFS + Ethereum Smart Contracts

## 📌 Problem Statement

With the explosive growth of cloud storage and e-commerce platforms, duplicate file uploads (especially images and product data) consume unnecessary bandwidth and storage. Traditional deduplication techniques rely on centralized systems, making them vulnerable to manipulation and data loss.

---

## 🎯 Project Goal

To create a **decentralized, transparent, and verifiable** system to detect and prevent duplicate file uploads using:
- ✅ IPFS for decentralized file storage
- ✅ SHA-256 hashing for content-based deduplication
- ✅ Ethereum smart contracts for on-chain metadata logging and validation
- ✅ Web3.py and Python backend integration
- ✅ A sample UI mimicking e-commerce platforms showing deduplication in action

---

## ✅ What We’ve Achieved So Far

### 1. 📦 IPFS File Upload
- Used [Pinata](https://pinata.cloud) for IPFS hosting.
- Uploaded a product image (`shirt.jpeg`) to IPFS.
- Captured:
  - ✅ CID (Content Identifier)
  - ✅ Gateway URL
  - ✅ SHA-256 hash of the file and description

### 2. 🧠 SHA-256 Deduplication Logic
- Custom Python hasher script created.
- Generated `hash = SHA256(file_content + description)`.
- Used this hash as a unique key to detect duplicates.

### 3. 🧾 Smart Contract Design: `DedupStorage.sol`
- Built and tested a Solidity smart contract with:
  - `storeFile(string sha256Hash, string ipfsCID)`
  - `fileExists(string sha256Hash) → bool`
  - `getFile(string sha256Hash) → (CID, uploader, timestamp)`
- Emitted `FileStored` event for every unique file entry.

### 4. 🧪 Smart Contract Deployment
- Compiled and deployed to **Ethereum Sepolia Testnet** using [Remix IDE](https://remix.ethereum.org).
- Contract address: `0x3c5535F2d83049e816586b89D4585cAD31bB6f87`
- ABI was generated and stored as `DedupStorage_abi.json`.

### 5. 🔌 Web3.py Integration
- Python script (`interact.py`) created to:
  - Connect to Sepolia via Infura
  - Load ABI and contract
  - Prepare and sign transactions (using private key)
  - Call `storeFile()` with hash and CID

### 6. 🖥️ Streamlit-based UI
- Simulated 3-column view for e-commerce platforms.
- Retrieved IPFS image using CID and SHA hash.
- Displayed uploaded product image and metadata.

---

## ⚠️ Where We're Stuck (And Why)

| ❌ Issue | 😤 Cause |
|---------|----------|
| `insufficient funds for gas` | Wallet has 0 Sepolia ETH, so transactions (like `storeFile()`) fail |
| Chainlink Faucet refusing | Requires 1 real LINK token on Ethereum Mainnet |
| Alchemy / QuickNode faucet blocked | Needs Twitter or mainnet ETH |
| Can't complete dedup check from frontend | Because hash can't be stored without sending a transaction |

---

## 🧠 Why We're Doing This

- ✅ Make storage and uploads **decentralized**.
- ✅ Prevent storage of duplicate files **without needing a central server**.
- ✅ Enable users to **verify ownership and upload time**.
- ✅ Simulate a **real-world e-commerce scenario** with cross-platform validation.

---

## 🛠️ Local Deduplication Tracking

- We use a simple local file: `dedup_db.json`
- Every time a new file is uploaded:
  - SHA-256 hash is checked
  - If unique → it's recorded
  - If duplicate → fetch existing CID and metadata

---

## 🔄 What’s Next

### 🚀 Immediate Next Steps
1. **Get Sepolia ETH** using a friend’s wallet or working faucet
2. Call `storeFile()` from Python
3. Validate on-chain file storage
4. Connect frontend to `fileExists()` and `getFile()`
5. Build success/fail messages into UI

### 🧱 Future Scope
- Implement role-based access
- Upload non-image files (PDFs, docs, etc.)
- Deploy frontend using Flask or React + Tailwind
- Move from testnet to real Layer-2 network like Polygon PoS

---

## 📂 Folder Structure

dedup-ipfs-ui/
│
├── assets/
│ └── shirt.jpeg
│
├── contracts/
│ └── DedupStorage.sol
│
├── deploy/
│ ├── deploy_contract.py
│ └── wallet.env
│
├── utils/
│ └── hasher.py
│
├── backend/
│ └── interact.py
│
├── dedup_db.json
├── DedupStorage_abi.json
└── README.md ← you’re reading it



---

## 🙌 Acknowledgements

- [Pinata](https://pinata.cloud) for IPFS support  
- [Remix IDE](https://remix.ethereum.org) for contract compilation and deployment  
- [Infura](https://infura.io) for testnet RPC access  
- [Web3.py](https://web3py.readthedocs.io) for Ethereum integration  
- [Chainlink Docs](https://docs.chain.link) for event examples

---

## 💡 Created by:
**Captain Harish** — for decentralized data warriors everywhere.  
Stay deduplicated, stay unstoppable. 🌐🔥
