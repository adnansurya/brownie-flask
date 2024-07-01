from flask import Flask, jsonify
from web3 import Web3, HTTPProvider
import threading
import traceback

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
contract_address = "0x09E7813943024B1D215059E57FD4EB9201faB3aB"  # Update with your contract address

# Global flag to control the DoS attack simulation
dos_attack_running = True

# Function for successful DoS attack simulation
def dos_attack():
    global dos_attack_running
    attack_count = 0
    while dos_attack_running and attack_count < 1000:
        try:
            tx = w3.eth.contract(address=str(contract_address), abi=res_abi).functions.writeText("DoS attack!").build_transaction({
                'from': str(accounts.add('0xf1ada957a8d0a24a4f4b1814c6580f5fc179b8f7564b6de8f4a6632602e8928c')),
                'gas': 2000000,
                'gasPrice': w3.eth.gas_price
            })
            tx_hash = w3.eth.send_transaction(tx)
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            attack_count += 1
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
    if attack_count >= 1000:
        print("DoS simulation succeed")

# Start the DoS attack in a separate thread
dos_thread = threading.Thread(target=dos_attack)
dos_thread.start()

# Endpoint for failed DoS attack simulation
@app.route('/check_failed_dos', methods=['GET'])
def check_failed_dos():
    try:
        return jsonify({'message': 'DoS simulation failed. Please check logs for details.'})
    except Exception as e:
        print(f"Error in /check_failed_dos: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)})

# Endpoint to stop DoS attack simulation
@app.route('/stop_dos_attack', methods=['GET'])
def stop_dos_attack():
    global dos_attack_running
    dos_attack_running = False
    return jsonify({'message': 'DoS attack simulation stopped'})

# Main endpoint to start the server
if __name__ == '__main__':
    app.run(debug=True)
