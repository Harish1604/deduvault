# 🔒 DeduVault
Decentralized Image Deduplication Platform using IPFS & Blockchain

Secure your digital assets, detect duplicates instantly, and visualize content across platforms — all powered by Web3.

## 🚀 Overview
DeduVault is a next-generation image deduplication and verification system. Built with IPFS, Ethereum Blockchain, and Streamlit, it allows users to:
- Upload image files.
- Generate SHA-256 and perceptual (phash) hashes.
- Store on IPFS via Pinata.
- Check for duplicates (exact and visual) using on-chain verification.
- Register new files on-chain with smart contracts.
- Simulate e-commerce listings across Flipkart, Amazon, and Myntra.
- Verify trusted uploaders for authenticity.

## 🌐 Tech Stack
| Layer         | Tech Used                                     |
|---------------|-----------------------------------------------|
| 💻 Frontend   | Streamlit + HTML/CSS                         |
| 🧠 Hashing    | SHA-256 (hashlib), Perceptual Hash (imagehash) |
| 📦 Storage    | IPFS via Pinata                              |
| 🔗 Blockchain | Ethereum Sepolia Testnet + web3.py           |
| 📜 Smart Contract | Solidity (Deployed via Remix IDE)        |
| 🧠 Logic      | Python: interact.py, uploader.py, hasher.py   |
| 📊 Database   | SQLite (dedup_db.sqlite)                     |

## 📸 Features
- 🔐 **Cryptographic Security**: SHA-256 for exact matches, perceptual hashing for visual similarity.
- 🌐 **IPFS Integration**: Decentralized content-addressed storage.
- ⛓️ **Blockchain Verification**: Immutable registry with smart contracts.
- ⚡ **Real-time Deduplication**: Detects exact and visually similar duplicates.
- 🛍️ **E-commerce Simulation**: Flipkart, Amazon, Myntra-styled previews with trusted/untrusted status.
- 📊 **Live Stats Dashboard**: Uptime, metrics, and storage saved.

## 📂 Project Structure
deduvault/
├── contracts/
│   ├── DedupStorage.sol          # Solidity smart contract with phash support
│   └── DedupStorage_abi.json     # Compiled ABI
├── utils/
│   └── hasher.py                 # SHA-256 and phash generation
├── .streamlit/
│   └── secrets.toml              # Secure secrets (DO NOT COMMIT)
├── data/
│   └── dedup_db.sqlite           # SQLite database for deduplication
├── interact.py                   # Blockchain interaction logic
├── uploader.py                   # IPFS upload and deduplication logic
├── streamlit_app.py              # Streamlit frontend UI
├── .env                          # Local secrets (DO NOT COMMIT)
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore file
└── README.md                     # Project documentation



## 🧠 How It Works
1. User uploads an image file.
2. App generates SHA-256 and perceptual (phash) hashes.
3. Checks for duplicates in SQLite DB and smart contract.
4. If no duplicate, uploads to IPFS via Pinata and stores metadata on-chain.
5. Displays IPFS CID, transaction hash, and e-commerce previews with trusted/untrusted status.

## 🧪 Smart Contract Details
- **Name**: DedupStorage.sol
- **Functions**:
  - `storeFile(sha256Hash, phash, ipfsCID)`
  - `fileExists(sha256Hash, phash)`
  - `getFile(sha256Hash)`
- **Deployed On**: Ethereum Sepolia Testnet
- **Contract Address**: (Update with your deployed address)

## 🔐 Secrets Setup
For local development, create `.env`:
```bash
PINATA_API_KEY=your-pinata-api-key
PINATA_SECRET_API_KEY=your-pinata-secret-key
WALLET_ADDRESS=your-ethereum-wallet-address
PRIVATE_KEY=your-private-key
INFURA_RPC_URL=https://sepolia.infura.io/v3/your-infura-project-id
CONTRACT_ADDRESS=your-deployed-contract-address

For Streamlit Cloud, add to Secrets Management:

Go to your app → Settings → Secrets tab → Paste the above content (without .env).

🚫 Sensitive Files & Security
Ensure these are in .gitignore:

.streamlit/secrets.toml
data/dedup_db.sqlite
.env
*.key
*.pem
__pycache__/
*.pyc
venv/

🌍 Live Deployment
Deployed on Streamlit Cloud (add link after deployment).
Run locally: streamlit run streamlit_app.py
👨‍💻 Author
Harish J. (aka Captain)

Top 15 Finalist – Sony AITRIOS Hackathon | Full-Stack + Blockchain Developer

GitHub | LinkedIn

📜 License
MIT License © 2025 Harish J.



---

### Implementation Steps
1. **Set Up File Structure**:
   - Create `data/` directory.
   - Create `.env` with your credentials.
   - Update `.gitignore`.

2. **Recompile and Deploy Smart Contract**:
   - Open Remix IDE<a href="https://remix.ethereum.org" target="_blank" rel="noopener noreferrer nofollow"></a>.
   - Copy the updated `DedupStorage.sol`.
   - Compile with Solidity `0.8.0` or higher.
   - Deploy to Sepolia Testnet via MetaMask (ensure Sepolia ETH).
   - Save ABI to `contracts/DedupStorage_abi.json`.
   - Update `.env` with new `CONTRACT_ADDRESS`.

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt


Initialize SQLite Database:

from uploader import init_db
init_db()

Test Locally:
streamlit run streamlit_app.py