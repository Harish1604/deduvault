from web3 import Web3

# Replace with your actual Infura RPC URL
rpc_url = "https://sepolia.infura.io/v3/03729448df4641ab9d35be871215138c"

# Connect to Web3
web3 = Web3(Web3.HTTPProvider(rpc_url))

# Wallet address to check (Sepolia or mainnet, depending on the RPC)
wallet_address = "0x92643AEafaf65d9cA08347A9e8e09c7A927b1362"

# Check connection
if web3.is_connected():
    # Get balance in Wei
    balance_wei = web3.eth.get_balance(wallet_address)

    # Convert Wei to Ether
    balance_eth = web3.from_wei(balance_wei, 'ether')

    print(f"Wallet balance: {balance_eth} ETH")
else:
    print("Connection failed ")
