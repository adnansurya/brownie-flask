from brownie import *
p = project.load('brownie-dir')
p.load_config()

from brownie.project.BrownieDirProject import *

abi = MessageStorage.abi
bytecode = MessageStorage.bytecode


from web3 import Web3
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

#contract address created after deploying contract
msgContract = w3.eth.contract(address='0x6945a73F33bB02526ed89cA5D95BA4312f0EE490', abi=abi)
currentMessage = msgContract.functions.getMessage().call()

print(currentMessage)


from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello_world():

    debugStr = "<p>Abi: " + str(abi) + "<br>Bytecode: " + str(bytecode) + "</p>"
    return debugStr