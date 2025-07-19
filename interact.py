from web3 import Web3
import json
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Load secrets from .env
INFURA_RPC_URL = os.getenv("INFURA_RPC_URL")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# Validate secrets
if not all([INFURA_RPC_URL, WALLET_ADDRESS, PRIVATE_KEY, CONTRACT_ADDRESS]):
    raise ValueError("Missing required environment variables in .env")

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(INFURA_RPC_URL))
if not w3.is_connected():
    raise ConnectionError("Failed to connect to Ethereum node")

# Load ABI
abi_path = os.path.join(os.getcwd(), "contracts", "DedupStorage_abi.json")
with open(abi_path) as f:
    abi = json.load(f)

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

def check_file_exists(sha256, phash):
    """Check if file exists by SHA-256 or phash."""
    try:
        return contract.functions.fileExists(sha256, phash).call()
    except Exception as e:
        print(f"Error checking file: {e}")
        return False, "Error checking file"

def get_file_data(sha256):
    """Get file data by SHA-256 hash."""
    try:
        data = contract.functions.getFile(sha256).call()
        return {
            "sha256": data[0],
            "phash": data[1],
            "cid": data[2],
            "uploader": data[3],
            "timestamp": str(data[4])
        }
    except Exception as e:
        print(f"Error fetching file data: {e}")
        return None

def store_file_on_chain(sha256, phash, ipfs_cid):
    """Store file metadata on blockchain."""
    try:
        nonce = w3.eth.get_transaction_count(WALLET_ADDRESS)
        tx = contract.functions.storeFile(sha256, phash, ipfs_cid).build_transaction({
            'from': WALLET_ADDRESS,
            'nonce': nonce,
            'gas': 300000,
            'gasPrice': w3.to_wei('20', 'gwei')
        })
        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Gas used for storeFile: {receipt.gasUsed}")
        return receipt.transactionHash.hex()
    except Exception as e:
        print(f"Error storing file: {e}")
        return None