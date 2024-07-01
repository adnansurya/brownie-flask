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

# Global flag to control the DoS attack simulation
dos_attack_running = True

# Define header for the CSV log file
log_header = 'timestamp;txHash;blockNumber;cumulativeGasUsed;gasUsed;from;to;effectiveGasPrice\n'

# Function to grant access to an address
def grant_access():
    sender_account = str(accounts[0])  # Replace with the account you want to use for sending transactions

    # Get the contract instance at the given address
    restricted_text_contract = w3.eth.contract(address=str(contract_address), abi=res_abi)

    # Grant access to the sender account
    tx_hash = restricted_text_contract.functions.grantAccess(sender_account, True).transact({'from': sender_account})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)  # Wait for transaction receipt (adjust timeout as needed)

    if tx_receipt.status == 1:
        print(f"Access granted. Hash: {tx_receipt.transactionHash.hex()}")
        return True
    else:
        print(f"Failed to grant access. Hash: {tx_receipt.transactionHash.hex()}")
        return False

# Example of calling the function
network.connect('development')  # Connect to the development network (Ganache or local blockchain)
access_granted = grant_access()

# Function to write log to CSV file
def write_log(row):
    file_name = datetime.now().strftime("%m%d%Y_%H%M%S")
    with open('output_DoS/' + file_name + '.csv', 'a') as f:
        # Write header if the file is newly created
        if f.tell() == 0:
            f.write(log_header)
        f.write(row)

# Function for successful DoS attack simulation
def successful_dos_attack():
    global dos_attack_running
    attack_count = 0
    while dos_attack_running and attack_count < 30:
        try:
            tx = w3.eth.contract(address=str(contract_address), abi=res_abi).functions.writeText("DoS attack!").build_transaction({
                'from': str(accounts[0]),
                'gas': 2000000,
                'gasPrice': w3.eth.gas_price
            })
            tx_hash = w3.eth.send_transaction(tx)
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            log_row = f"{now};{tx_receipt.transactionHash.hex()};{tx_receipt.blockNumber};{tx_receipt.cumulativeGasUsed};{tx_receipt.gasUsed};{tx_receipt['from']};{tx_receipt['to']};{tx_receipt.effectiveGasPrice}\n"
            write_log(log_row)
            attack_count += 1
        except Exception as e:
            print(f"Error: {e}")
    if attack_count >= 30:
        print("Simulasi DoS berhasil")

# Function for failed DoS attack simulation
def failed_dos_attack():
    while True:
        time.sleep(5)  # Wait for 5 seconds
        try:
            restricted_text = w3.eth.contract(address=str(contract_address), abi=res_abi).functions.readText().call()
            print(f"Simulasi DoS gagal: Current text: {restricted_text}")
        except Exception as e:
            print(f"Simulasi DoS gagal: Error: {e}")

# Function for another failed DoS attack simulation (new function added)
def another_failed_dos_attack():
    while True:
        time.sleep(5)  # Wait for 5 seconds
        try:
            sender_account = str(accounts[0])
            restricted_text_contract = w3.eth.contract(address=str(contract_address), abi=res_abi)

            # Attempt to execute another restricted action
            # Replace with a function that might require additional permissions or conditions
            # In this case, we can simulate a hypothetical "restrictedAction" function
            # that requires specific conditions or permissions not met here.
            # For illustration, this is commented out due to the error message.

            # tx_hash = restricted_text_contract.functions.restrictedAction().transact({'from': sender_account})
            # tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

            # Log the attempt (though it should fail due to the commented error message)
            now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            log_row = f"{now};NoTxHash;NoBlock;NoCumulativeGasUsed;NoGasUsed;{sender_account};{contract_address};NoEffectiveGasPrice\n"
            write_log(log_row)
            print("Simulasi DoS gagal-coba: Another restricted action attempted")
        except Exception as e:
            print(f"Simulasi DoS gagal-coba: Error: {e}")

# Ensure access is granted before starting the attack
if access_granted:
    # Thread to run successful DoS attack simulation
    dos_thread = threading.Thread(target=successful_dos_attack)
    dos_thread.start()
    
    # Thread to run failed DoS attack simulation
    failed_dos_thread = threading.Thread(target=failed_dos_attack)
    failed_dos_thread.start()
    
    # Thread to run another failed DoS attack simulation
    another_failed_dos_thread = threading.Thread(target=another_failed_dos_attack)
    another_failed_dos_thread.start()
else:
    print("Cannot start DoS simulation as access grant failed.")

# Endpoint for failed DoS attack simulation (new endpoint added)
@app.route('/check_failed_dos', methods=['GET'])
def check_failed_dos():
    try:
        return jsonify({'message': 'DoS simulation failed. Please check logs for details.'})
    except Exception as e:
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
