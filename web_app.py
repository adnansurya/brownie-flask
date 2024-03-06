from brownie import *
p = project.load('brownie-dir')
p.load_config()

from brownie.project.BrownieDirProject import *

abi = MessageStorage.abi
bytecode = MessageStorage.bytecode

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():

    debugStr = "<p>Abi: " + str(abi) + "<br>Bytecode: " + str(bytecode) + "</p>"
    return debugStr