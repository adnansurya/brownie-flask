from brownie import *
p = project.load('brownie-dir')
p.load_config()

from brownie.project.BrownieDirProject import *

abi = MessageStorage.abi
bytecode = MessageStorage.bytecode


from web3 import Web3
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

#function to get message from contract
def getMessageFromContract(tnx_address):
    msgContract = w3.eth.contract(address=tnx_address, abi=abi)
    currentMessage = msgContract.functions.getMessage().call()
    print(currentMessage)
    return currentMessage

def setMessageToContract(tnx_address, sender_address, sender_pk, value):
    # checked_tnx_address = Web3.to_checksum_address(tnx_address) #checksum if needed

    msgContract = w3.eth.contract(address=tnx_address, abi=abi)    
    tnx_created = msgContract.functions.setMessage(value).build_transaction({
        'from' : sender_address,
        'nonce' : w3.eth.get_transaction_count(sender_address),
        'gasPrice': 200000
    })
    tnx_signed = w3.eth.account.sign_transaction(tnx_created, sender_pk)
    tnx_hash = w3.eth.send_raw_transaction(tnx_signed.rawTransaction)

    tnx_receipt = w3.eth.wait_for_transaction_receipt(tnx_hash)
    print(tnx_receipt)    



from flask import Flask, render_template, request
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def index():
    #debugStr = "<p>Abi: " + str(abi) + "<br>Bytecode: " + str(bytecode) + "</p>"    
    return render_template('index.html')

@app.route("/get_message/<address>")
def getMessage(address):    
    message_text = getMessageFromContract(address) #contract address created after deploying contract
    return f"<p> Getting Message from Address : {escape(address)} <br>The Message : {escape(message_text)} </p>"


@app.route("/set_message", methods=['POST'])
def setMessage():
    res_message = '-'
    if request.method == 'POST':
        sender_address = request.form['sender_address']
        sender_pk = request.form['sender_pk']
        address = request.form['address']
        value = request.form['value']
        res_message = address + ' - ' + value
        setMessageToContract(address, sender_address, sender_pk, value)
    else:
        res_message = 'error'

    return res_message