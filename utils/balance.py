from web3 import Web3

# ✅ Connect to an Ethereum provider (replace with your actual RPC URL)
rpc_url = "https://sepolia.infura.io/v3/03729448df4641ab9d35be871215138c"
w3 = Web3(Web3.HTTPProvider(rpc_url))

# ✅ Your wallet address
wallet_address = "0x66c720EaDEEc55048fFCb86A0300123D5fe0b1a7"

# ✅ Check if connection is successful
if not w3.is_connected():
    print("⚠️ Not connected to the network!")
else:
    # ✅ Get balance in wei
    balance_wei = w3.eth.get_balance(wallet_address)

    # ✅ Convert to Ether
    balance_eth = w3.from_wei(balance_wei, 'ether')

    print(f"Wallet Balance: {balance_eth} ETH")
