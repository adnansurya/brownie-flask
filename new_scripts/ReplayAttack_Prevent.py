from web3 import Web3
from brownie import project
from eth_account.messages import encode_defunct

# Load Brownie project and configure
p = project.load('brownie-dir')
p.load_config()

# Obtain ABI from Brownie
res_abi = p.NewContract.abi

# Web3 instance connected to your local Ganache instance
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Addresses for UserB (replace with actual addresses and private keys)
userB_address = "0x9057116E692a2957423E24A8FE35672dd568F943"
userB_private_key = "0xd0c4c9f9d4b60b1eaeca51212eee251b01fcbcd7b7750054c957105722930389"  # Replace with UserB's private key

# Contract address (replace with actual contract address)
contract_address = "0x5Dfc138bFBED1e1391582cE848f5dF89d7ee50D9"  # Replace with actual deployed contract address

# Create contract instance
contract_instance = web3.eth.contract(address=contract_address, abi=res_abi)

def create_and_send_transaction(user_address, user_private_key, message):
    try:
        # Get the current nonce from the blockchain
        blockchain_nonce = web3.eth.get_transaction_count(user_address)

        # Fetch the expected nonce from contract state
        expected_nonce = contract_instance.functions.nonces(user_address).call()

        print(f"Blockchain nonce: {blockchain_nonce}, Contract nonce: {expected_nonce}")

        # Wait until the blockchain nonce catches up
        while blockchain_nonce <= expected_nonce:
            blockchain_nonce = web3.eth.get_transaction_count(user_address)

        # Ensure the fetched nonce is exactly one more than the expected nonce
        if blockchain_nonce != expected_nonce + 1:
            raise ValueError(f"Invalid nonce. Expected nonce: {expected_nonce + 1}, Got nonce: {blockchain_nonce}")

        # Create message hash
        message_hash = web3.keccak(text=message + str(expected_nonce + 1)).hex()
        signed_message = web3.eth.account.sign_message(encode_defunct(hexstr=message_hash), private_key=user_private_key)
        
        # Construct the transaction
        tx = contract_instance.functions.writeText(message, expected_nonce + 1, signed_message.signature).build_transaction({
            'chainId': web3.eth.chain_id,
            'gas': 2000000,
            'gasPrice': web3.to_wei('5', 'gwei'),
            'nonce': blockchain_nonce,
        })

        # Sign the transaction
        signed_tx = web3.eth.account.sign_transaction(tx, private_key=user_private_key)

        # Send the transaction
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)

        if receipt['status'] == 1:
            print(f"Transaction sent successfully with nonce {blockchain_nonce}.")
        else:
            print(f"Transaction failed with nonce {blockchain_nonce}.")

    except ValueError as e:
        print(f"Error creating or sending transaction: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Example usage
def test_transactions():
    message = "Hello from UserB!"

    try:
        for i in range(3):
            create_and_send_transaction(userB_address, userB_private_key, message)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_transactions()
