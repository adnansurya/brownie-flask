# script yang menengahi python dan java -web 3
# berisi server lokal (Flask), dan blockchain (Brownie)
from brownie import *
from flask import Flask, render_template, request, jsonify
from web3 import Web3, HTTPProvider
from datetime import datetime
import threading
import traceback
import json

# Load the Brownie project
p = project.load('brownie-dir')
p.load_config()

res_abi = p.RestrictedText.abi
res_bytecode = p.RestrictedText.bytecode

# Initialize Flask application
app = Flask(__name__)

# Setup Web3 provider
w3 = Web3(HTTPProvider('http://localhost:8545'))

# Address of the deployed RestrictedText contract
#contract_address = "0x09E7813943024B1D215059E57FD4EB9201faB3aB"  # Update with your contract address

# Global flag to control the DoS attack simulation
dos_attack_running = True

file_name = datetime.now().strftime("%m%d%Y_%H%M%S")
print("nama file: " + file_name)

def writeGanacheLog(fileName, row):
    # open the file in the write mode
    with open('output_DoS/' + fileName + '.csv', 'a') as f:
        f.write(row)

def setMessageCtx(ctx_addr, sndr_addr, sndr_pk, value):
    contract = w3.eth.contract(address=ctx_addr, abi=res_abi)
    tx = contract.functions.writeText(value).build_transaction({
        'from': sndr_addr,
        'nonce': w3.eth.get_transaction_count(sndr_addr),
        'gasPrice': 200000
    })

    signed_tx = w3.eth.account.sign_transaction(tx, sndr_pk)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print(tx_receipt)
    
    now = datetime.now()  # current date and time
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    log_row = date_time + ";" + tx_receipt['transactionHash'].hex() + ";" + str(tx_receipt['blockNumber']) + ";" + str(tx_receipt['cumulativeGasUsed']) + ";" + str(tx_receipt['gasUsed']) + ";" + tx_receipt['from'] + ";" + tx_receipt['to'] + ";" + str(tx_receipt['effectiveGasPrice']) + ";\n"
    writeGanacheLog(file_name, log_row)
    
    return tx_receipt['transactionHash'].hex()

def readMessageFromHash(tx_hash, sndr_addr):
    tx = w3.eth.get_transaction(tx_hash)
    ctx_address = tx['to']
    contract = w3.eth.contract(address=ctx_address, abi=res_abi)

    tx_receipt = w3.eth.get_transaction_receipt(tx_hash)
    restricted_text = '-'
    
    if tx_receipt.status == 1:
        # Proses log acara dari transaksi tersebut
        for log in tx_receipt.logs:
            # Periksa apakah log acara terkait dengan event TextChanged
            if log.address == ctx_address:
                # Dekode data dari log acara
                decoded_log = contract.events.TextChanged().process_log(log)
                restricted_text = decoded_log['args']['newText']
    print(restricted_text)
    return restricted_text

def readMessageFromContract(ctx, sndr_addr):
    contract = w3.eth.contract(address=ctx, abi=res_abi)
    restricted_text = contract.functions.readText().call({'from': sndr_addr})
    print(restricted_text)
    return restricted_text

def grantAccessToAccount(ctx, owner, acc, allow):
    allowing = False
    if int(allow) == 1:
        allowing = True

    contract = w3.eth.contract(address=ctx, abi=res_abi)
    tx_hash = contract.functions.grantAccess(acc, allowing).transact({
        'from': owner,
        'nonce': w3.eth.get_transaction_count(owner),
        'gasPrice': 200000
    })

    try:
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(tx_receipt)
    except:
        res_message = 'Error Editing Access'

    try:
        restricted_text = contract.functions.readText().call({'from': acc})
        print("Restricted Text from Allowed Account:", restricted_text)
        res_message = 'Access Enabled'
    except:
        res_message = 'Access Disabled'

    return res_message

# DoS attack function
def dos_attack(ctx):
    global dos_attack_running
    attack_count = 0
    while dos_attack_running and attack_count < 1000:
        try:
            tx = w3.eth.contract(address=str(ctx), abi=res_abi).functions.writeText("DoS attack!").build_transaction({
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
        print("DoS simulation succeeded")

# Start the DoS attack in a separate thread
dos_thread = threading.Thread(target=dos_attack)
dos_thread.start()

log_header = 'timestamp;txHash;blockNumber;cumulativeGasUsed;gasUsed;from;to;effectiveGasPrice;\n'
with open('output_log/' + file_name + '.csv', 'w') as f:
    f.write(log_header)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/set_message", methods=['POST'])
def setMessage():
    res_message = '-'
    if request.method == 'POST':
        sender_address = request.form['sender_address']
        sender_pk = request.form['sender_pk']
        address = request.form['address']
        value = request.form['value']
        res_message = setMessageCtx(address, sender_address, sender_pk, value)
        print(res_message)
    else:
        res_message = 'error'

    return jsonify(
        message_text=res_message
    )

@app.route("/get_message_hash", methods=['POST'])
def getMessageHash():
    message_text = ''
    if request.method == 'POST':
        tx_hash = request.form['tx_hash']
        sender_address = request.form['sender_address']
        try:
            message_text = readMessageFromHash(tx_hash, sender_address)
        except:
            message_text = 'error'
    else:
        message_text = 'wrong method'

    return jsonify(
        message_text=message_text
    )

@app.route("/get_message", methods=['POST'])
def getMessageCtx():
    message_text = ''
    if request.method == 'POST':
        contract_address = request.form['ctx_address']
        sender_address = request.form['sender_address']
        try:
            message_text = readMessageFromContract(contract_address, sender_address)
        except:
            message_text = 'error'
    else:
        message_text = 'wrong method'

    return jsonify(
        message_text=message_text
    )

@app.route("/grant_access", methods=['POST'])
def grantAccess():
    res_message = '-'
    if request.method == 'POST':
        owner_address = request.form['owner_address']
        allow_address = request.form['allow_address']
        ctx_address = request.form['ctx_address']
        allowed = request.form['allowed']
        print(allowed)
        res_message = grantAccessToAccount(ctx_address, owner_address, allow_address, allowed)
        print(res_message)
    else:
        res_message = 'error'

    return jsonify(
        message_text=res_message
    )

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
