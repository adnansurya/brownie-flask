#script yang menengahi python dan java -web 3
#berisi server lokal (flash), dan blockchain (brownie)
from brownie import *
p = project.load('brownie-dir')
p.load_config()

from brownie.project.BrownieDirProject import *

res_abi = RestrictedText.abi
res_bytecode = RestrictedText.bytecode


from web3 import Web3
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))


from datetime import datetime

file_name = datetime.now().strftime("%m%d%Y_%H%M%S")
print("nama file: " + file_name)


def accountIsIdentified(acc_addr):    
    isIdentified = False
    list_acc = w3.eth.accounts
    for acc in list_acc:
        if acc == acc_addr:
            isIdentified = True
            break
    
    return isIdentified

def writeGanacheLog(fileName, row):    
    # open the file in the write mode
    with open('output_log/'+ fileName + '.csv', 'a') as f:       
        f.write(row)


def setMessageCtx(ctx_addr, sndr_addr, sndr_pk, value):
    to_addr = json.loads(value)['to_address']
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
    
    now = datetime.now() # current date and time
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")    
    log_row = date_time + ";" + tx_receipt['transactionHash'].hex()  + ";" +  str(tx_receipt['blockNumber'])  + ";" +  str(tx_receipt['cumulativeGasUsed']) + ";" +  str(tx_receipt['gasUsed'])  + ";" +  tx_receipt['from']  + ";" +  tx_receipt['to']  + ";" +  str(tx_receipt['effectiveGasPrice']) + ";" + to_addr + ";\n"
    writeGanacheLog(file_name,log_row)
    
    return tx_receipt['transactionHash'].hex()


def readMessageFromHash(tx_hash, sndr_addr, rcvr_addr):       
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
                decoded_text = decoded_log['args']['newText']    
                changer = decoded_log['args']['changer']
                if changer == sndr_addr:
                    pack_msg = json.loads(decoded_text)
                    to_addr = pack_msg['to_address']
                    print(to_addr)
                    if to_addr == rcvr_addr:
                        restricted_text = pack_msg['value']
                    else:
                        restricted_text = "ERROR : Wrong Receiver's Address"                                    
                else:
                    restricted_text = "ERROR : Wrong Sender's Address"
                                           
    print(restricted_text)
    return restricted_text

def readMessageFromContract(ctx, sndr_addr):    
    contract = w3.eth.contract(address=ctx, abi=res_abi)
    restricted_text = contract.functions.readText().call({'from' : sndr_addr})
    print(restricted_text)
    return restricted_text


def grantAccessToAccount(ctx, owner, acc, allow):

    allowing = False
   
    if int(allow) == 1:
        allowing = True        

    contract = w3.eth.contract(address=ctx, abi=res_abi)
    tx_hash = contract.functions.grantAccess(acc, allowing).transact({
        'from': owner, 
        'nonce' : w3.eth.get_transaction_count(owner),
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

def setMessageCtxOld(ctx_addr, sndr_addr, sndr_pk, value):
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
    
    now = datetime.now() # current date and time
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")    
    log_row = date_time + ";" + tx_receipt['transactionHash'].hex()  + ";" +  str(tx_receipt['blockNumber'])  + ";" +  str(tx_receipt['cumulativeGasUsed']) + ";" +  str(tx_receipt['gasUsed'])  + ";" +  tx_receipt['from']  + ";" +  tx_receipt['to']  + ";" +  str(tx_receipt['effectiveGasPrice']) + ";\n"
    writeGanacheLog(file_name,log_row)
    
    return tx_receipt['transactionHash'].hex()


def readMessageFromHashOld(tx_hash, sndr_addr):    
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

#1-#36 blockchain (web3)

from flask import Flask, render_template, request, jsonify
from markupsafe import escape
import json


log_header = 'timestamp ;txHash ;blockNumber ;cumulativeGasUsed ;gasUsed ;from ;to ;effectiveGasPrice; toAddr; \n' 
with open('output_log/'+ file_name+ '.csv', 'w') as f:
    f.write(log_header)

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
        value = request.form['value']             
        receiver_address = request.form['receiver_address']
        sender_pk = request.form['sender_pk']
        address = request.form['address']        
              
        if accountIsIdentified(sender_address): 
            json_msg = {
                "value" : value,
                "to_address" : receiver_address
            }
            packaged_msg = json.dumps(json_msg)
            print(packaged_msg)
            res_message = setMessageCtx(address, sender_address, sender_pk, packaged_msg)
            print(res_message)
        else:
            res_message = 'Unidentified Account'
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
        receiver_address = request.form['receiver_address'] 
        if accountIsIdentified(sender_address):                       
            try:                        
                message_text = readMessageFromHash(tx_hash, sender_address, receiver_address) #contract address created after deploying contract            
            except:
                message_text = 'error'
        # return f"<p> Getting Message from Address : {escape(address)} <br>The Message : {escape(message_text)} </p>"
        else:
            message_text = 'Unidentified Account'
    else:
        message_text = 'wrong method'

    return jsonify(
        message_text = message_text
    )

@app.route("/get_message", methods=['POST'])
def getMessageCtx():
    message_text = ''
    status = 'empty'    
    if request.method == 'POST':     
        contract_address = request.form['ctx_address']
        sender_address = request.form['sender_address']                
        try:                        
            message_text = readMessageFromContract(contract_address, sender_address) #contract address created after deploying contract            
        except:
            message_text = 'error'
        # return f"<p> Getting Message from Address : {escape(address)} <br>The Message : {escape(message_text)} </p>"
   
    else:
        message_text = 'wrong method'

    return jsonify(
        message_text = message_text
    )
       
@app.route("/grant_access", methods=['POST'])
def grantAccess():
    res_message = '-'
    # print(request.method)
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
        message_text = res_message 
    )
    
@app.route("/set_message_old", methods=['POST'])
def setMessageOld():
    res_message = '-'
    # print(request.method)
    if request.method == 'POST':
        sender_address = request.form['sender_address']
        sender_pk = request.form['sender_pk']
        address = request.form['address']
        value = request.form['value']
        res_message = setMessageCtxOld(address, sender_address, sender_pk, value)
        print(res_message)
    else:
        res_message = 'error'

    return jsonify(
        message_text = res_message 
    )



@app.route("/get_message_hash_old", methods=['POST'])
def getMessageHashOld():
    message_text = ''
    status = 'empty'    
    if request.method == 'POST':     
        tx_hash = request.form['tx_hash']
        sender_address = request.form['sender_address']                
        try:                        
            message_text = readMessageFromHashOld(tx_hash, sender_address) #contract address created after deploying contract            
        except:
            message_text = 'error'
        # return f"<p> Getting Message from Address : {escape(address)} <br>The Message : {escape(message_text)} </p>"
   
    else:
        message_text = 'wrong method'

    return jsonify(
        message_text = message_text
    )
    
@app.route("/tes_post", methods=['POST'])
def testPost():
    if request.method == 'POST': 
        sender_address = request.form['sender_address']
        # value = request.form['value']
        return(sender_address )
    else:
        return 'ERROR'
    