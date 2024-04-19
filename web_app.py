from brownie import *
p = project.load('brownie-dir')
p.load_config()

from brownie.project.BrownieDirProject import *

abi = MessageStorage.abi
bytecode = MessageStorage.bytecode

res_abi = RestrictedText.abi
res_bytecode = RestrictedText.bytecode


from web3 import Web3
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))



def setMessageCtx(ctx_addr, sndr_addr, sndr_pk, value):
    contract = w3.eth.contract(address=ctx_addr, abi=res_abi)
    tx = contract.functions.writeText(value).build_transaction({
        'from' : sndr_addr,
        'nonce' : w3.eth.get_transaction_count(sndr_addr),
        'gasPrice': 200000
    })

    signed_tx = w3.eth.account.sign_transaction(tx, sndr_pk)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print(tx_receipt)
    
    return tx_receipt['transactionHash'].hex()


def readMessageFromHash(tx_hash, sndr_addr):    
    tx = w3.eth.get_transaction(tx_hash)
    ctx_address = tx['to']    
    contract = w3.eth.contract(address=ctx_address, abi=res_abi)
    restricted_text = contract.functions.readText().call({'from' : sndr_addr})
    print(restricted_text)
    return restricted_text


from flask import Flask, render_template, request, jsonify
from markupsafe import escape
import json

app = Flask(__name__)

@app.route("/")
def index():
    #debugStr = "<p>Abi: " + str(abi) + "<br>Bytecode: " + str(bytecode) + "</p>"    
    return render_template('index.html')

@app.route("/set_message", methods=['POST'])
def setMessage():
    res_message = '-'
    # print(request.method)
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
        message_text = res_message 
    )



@app.route("/get_message_hash", methods=['POST'])
def getMessageHash():
    message_text = ''
    status = 'empty'    
    if request.method == 'POST':     
        tx_hash = request.form['tx_hash']
        sender_address = request.form['sender_address']                
        try:                        
            message_text = readMessageFromHash(tx_hash, sender_address) #contract address created after deploying contract            
        except:
            status = 'error'
        # return f"<p> Getting Message from Address : {escape(address)} <br>The Message : {escape(message_text)} </p>"
   
    else:
        status = 'wrong method'

    return jsonify(
        message_text = message_text,
        status = status
    )
       