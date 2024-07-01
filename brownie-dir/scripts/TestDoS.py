from flask import Flask, jsonify
from web3 import Web3, HTTPProvider
from datetime import datetime
import threading
import time

from brownie import project, accounts, network

# Load the Brownie project
p = project.load('brownie-dir')
p.load_config()

# Get the ABI and bytecode of RestrictedText contract
RestrictedText = p.RestrictedText
res_abi = p.RestrictedText.abi
res_bytecode = p.RestrictedText.bytecode

# Initialize Flask application
app = Flask(__name__)

# Setup Web3 provider
w3 = Web3(HTTPProvider('http://localhost:8545'))

# Address of the deployed RestrictedText contract
contract_address = "0x59fA51F266F909232757Fdf829a4948d3efe8459"  # Update with your contract address

# Flag to control the DoS attack simulation
dos_attack_running = True

# Function to write text to the smart contract
def write_text():
    sender_account = str(accounts[0])  # Replace with the account you want to use for sending transactions

    # Get the contract instance at the given address
    restricted_text_contract = w3.eth.contract(address=str(contract_address), abi=res_abi)

    # Send transaction to write text to the contract
    tx_hash = restricted_text_contract.functions.writeText("DoS attack!").transact({'from': sender_account})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)  # Wait for transaction receipt (adjust timeout as needed)

    # Log the transaction details or handle as needed
    if tx_receipt.status == 1:
        print(f"Transaction successful. Hash: {tx_receipt.transactionHash}")
    else:
        print(f"Transaction failed. Hash: {tx_receipt.transactionHash}")

# Example of calling the function
network.connect('development')  # Connect to the development network (Ganache or local blockchain)
write_text()