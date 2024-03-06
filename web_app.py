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



from flask import Flask, render_template
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
