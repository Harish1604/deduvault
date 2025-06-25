from web3 import Web3
import json

# Connect to Sepolia
w3 = Web3(Web3.HTTPProvider("https://sepolia.infura.io/v3/03729448df4641ab9d35be871215138c"))
print("Connected:", w3.is_connected())

# Wallet info
wallet_address = '0x66c720EaDEEc55048fFCb86A0300123D5fe0b1a7'
private_key = '0x5828012726adadce4b084885f549f2d1844e3e0fa0f1ab6296cf1f8b9bb507f9'
print(w3.eth.get_balance(wallet_address))


# Load ABI
with open(r'C:\Users\jhari\Desktop\data\cloud\DedupStorage_abi.json') as f:
    abi = json.load(f)

# Contract
contract_address = '0x3c5535F2d83049e816586b89D4585cAD31bB6f87'
contract = w3.eth.contract(address=contract_address, abi=abi)

# File hash & CID
file_hash = "02bb8abf24e64832b47a00cb006cbc90b2b08f406ae4357aeb85cd6a97a6476c"
ipfs_cid = "QmV5tZTPpkT75ESNMuM8nzx5qcKd1AjRAQ5RziMF2JwHrq"

# Build transaction
tx = contract.functions.storeFile(file_hash, ipfs_cid).build_transaction({
    'from': wallet_address,
    'nonce': w3.eth.get_transaction_count(wallet_address),
    'gas': 200000,
    'gasPrice': w3.to_wei('20', 'gwei')
})

# Sign & send
signed_tx = w3.eth.account.sign_transaction(tx, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
print("Transaction sent! TX hash:", tx_hash.hex())
