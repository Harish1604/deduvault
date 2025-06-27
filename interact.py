from web3 import Web3
import json
import os

# Web3 Setup
w3 = Web3(Web3.HTTPProvider("https://sepolia.infura.io/v3/YOUR_INFURA_KEY"))

# Wallet Info
wallet_address = '<#WALLET ADDRESS>'
private_key = '<WALLET PRIVATE KEY>'

# Dynamically build the path to the ABI file
abi_path = os.path.join(os.getcwd(), "contracts", "DedupStorage_abi.json")

with open(abi_path) as f:
    abi = json.load(f)

contract_address = "<YOUR Contract address>"
contract = w3.eth.contract(address=contract_address, abi=abi)


def check_file_exists(file_hash):
    try:
        return contract.functions.fileExists(file_hash).call()
    except Exception as e:
        print("Error checking file:", e)
        return False


def get_file_data(file_hash):
    try:
        data = contract.functions.getFile(file_hash).call()
        return {
            "cid": data[0],
            "uploader": data[1],
            "timestamp": str(data[2])  # no datetime, raw timestamp
        }
    except Exception as e:
        print("Error fetching file data:", e)
        return None


def store_file_on_chain(file_hash, ipfs_cid):
    try:
        nonce = w3.eth.get_transaction_count(wallet_address)
        tx = contract.functions.storeFile(file_hash, ipfs_cid).build_transaction({
            'from': wallet_address,
            'nonce': nonce,
            'gas': 200000,
            'gasPrice': w3.to_wei('20', 'gwei')
        })
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        return tx_hash.hex()
    except Exception as e:
        print("Error storing file:", e)
        return None