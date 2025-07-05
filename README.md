# 🔒 DeduVault

**Decentralized Image Deduplication Platform using IPFS & Blockchain**

> Secure your digital assets, detect duplicates instantly, and visualize content across platforms — all powered by Web3.

---

## 🚀 Overview

**DeduVault** is a next-generation image deduplication and verification system. Built with **IPFS**, **Ethereum Blockchain**, and **Streamlit**, it allows users to:

- Upload image files.
- Generate a **SHA-256 hash**.
- Store on **IPFS via Pinata**.
- Check for duplicates using **on-chain verification**.
- **Register new files** on-chain with smart contracts.
- Simulate e-commerce listings across **Flipkart, Amazon, and Myntra**.

---

## 🌐 Tech Stack

| Layer            | Tech Used                          |
|------------------|------------------------------------|
| 💻 Frontend      | Streamlit + HTML/CSS               |
| 🧠 Hashing       | SHA-256 (`hashlib`)                |
| 📦 Storage       | IPFS via [Pinata](https://pinata.cloud) |
| 🔗 Blockchain    | Ethereum (Testnet) + `web3.py`     |
| 📜 Smart Contract| Solidity (Deployed via Remix IDE) |
| 🧠 Logic         | Python: `interact.py`, `uploader.py` |

---

## 📸 Features

- 🔐 **Cryptographic Security** – Unique SHA-256 hashing per image
- 🌐 **IPFS Integration** – Decentralized content-addressed storage
- ⛓️ **Blockchain Verification** – Immutable registry with smart contracts
- ⚡ **Real-time Deduplication** – Alerts on existing file hashes
- 🛍️ **E-commerce Simulation** – Flipkart, Amazon & Myntra styled preview cards
- 📊 **Live Stats Dashboard** – Uptime, metrics, and storage saved

---

## 📂 Project Structure

```
📁 deduvault/
├── contracts/
│   └── DedupStorage_abi.json      # ABI from Remix (Solidity contract compiled)
├── utils/
│   └── hasher.py                  # SHA-256 hash generator
├── interact.py                    # Blockchain interaction logic
├── uploader.py                    # IPFS upload + hash check
├── streamlit_app.py               # Frontend UI with Streamlit
├── .streamlit/
│   └── secrets.toml               # 🔒 Secure secrets (DO NOT COMMIT)
├── requirements.txt               # Python dependencies
└── README.md                      # You’re reading it now
```

---

## 🧠 How It Works

### 🔁 Workflow

1. User uploads an image file.
2. App generates a **SHA-256 hash** from the file.
3. File is uploaded to **IPFS** via the Pinata API.
4. The hash is checked on-chain for duplicates.
5. If no duplicate is found, **CID + hash** are stored in a smart contract.
6. Users receive the IPFS URL + transaction confirmation.
7. Optional: Preview your image across e-commerce platforms.

---

## 🧪 Smart Contract Details

- **Name**: `DedupStorage.sol`
- **Functions**:
  - `storeFile(fileHash, cid)`
  - `fileExists(fileHash)`
  - `getFile(fileHash)`
- **Deployed On**: Ethereum Sepolia Testnet (via Remix IDE)
- **Contract Address**: `0x3c5535F2d83049e816586b89D4585cAD31bB6f87`

---

## 🔐 Streamlit Secrets Setup (Required for Deployment)

### 📁 Path: `.streamlit/secrets.toml`

To securely manage your API keys and wallet credentials, create a `.streamlit/secrets.toml` file **(not pushed to GitHub)** with the following:

```toml
PINATA_API_KEY = "your-pinata-api-key"
PINATA_SECRET_KEY = "your-pinata-secret-key"
WALLET_ADDRESS = "your-ethereum-wallet-address"
PRIVATE_KEY = "your-private-key"
INFURA_RPC_URL = "https://sepolia.infura.io/v3/your-infura-project-id"
```

### 📌 For Streamlit Cloud Deployment:
- Go to your app → `Settings` → `Secrets` tab → Paste the above content there.

---

## 🚫 Sensitive Files & Security

The following files should **never** be committed or exposed:

```
# .gitignore entries
.streamlit/secrets.toml
config.py
*.key
*.pem
__pycache__/
*.pyc
.env/
venv/
```

You can check the full `.gitignore` file inside the repo.

---

## 🌍 Live Deployment

> 🎯 This app is deployed on **Streamlit Cloud**  
> 🔗 Add your live link here (once deployed):  
> 👉 [Open DeduVault Live](https://deduvault.streamlit.app)

---

## 👨‍💻 Author

**Harish J. (aka Captain)**  
Top 15 Finalist – Sony AITRIOS Hackathon | Full-Stack + Blockchain Developer  
[GitHub](https://github.com/Harish1604) | [LinkedIn](https://linkedin.com/in/harish16042005)

---

## 📜 License

MIT License © 2025 Harish J.

---

## ✨ Extras

- Built with ❤️ using Web3 and Open Source tools.
- Feel free to fork, star, and contribute.

---