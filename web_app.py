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



from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    #debugStr = "<p>Abi: " + str(abi) + "<br>Bytecode: " + str(bytecode) + "</p>"
    
    #contract address created after deploying contract
    message_text = getMessageFromContract('0x6945a73F33bB02526ed89cA5D95BA4312f0EE490')
    displayStr = "<p>" + message_text + "</p>"
    return displayStr