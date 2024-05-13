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

def getHistory():

    contract_address = '0xbeFa29CE4b5daa52550421c0681B8B03f315455C'

    contract = w3.eth.contract(address=contract_address, abi=res_abi)

    latest_block = w3.eth.block_number
    print(latest_block)

    # Loop melalui transaksi historis
    for block_number in range(latest_block, latest_block - 10 , -1):
        block = w3.eth.get_block(block_number, True)
        transactions = block.transactions
        for tx in transactions:

            # print(tx.hash.hex())
            # print(tx.to)
            print(tx.hash.hex())
            if tx.to == contract_address:
                # print('OK')
                tx_receipt = w3.eth.get_transaction_receipt(tx.hash)
               
                if tx_receipt.status == 1:
                # Proses log acara dari transaksi tersebut
                    for log in tx_receipt.logs:
                        # Periksa apakah log acara terkait dengan event TextChanged
                        if log.address == contract_address:
                            # Dekode data dari log acara
                            decoded_log = contract.events.TextChanged().process_log(log)
                            print(decoded_log['args']['newText'])
                            # Ambil teks yang baru dari log acara
                            # new_text = decoded_log[0]['args']['newText']
                            # print("New Text:", new_text)

getHistory()

# from datetime import datetime

# file_name = datetime.now().strftime("%m%d%Y_%H%M%S")
# print("nama file: " + file_name)

# def writeGanacheLog(fileName, row):    
#     # open the file in the write mode
#     with open('output_log/'+ fileName + '.csv', 'a') as f:       
#         f.write(row)


# def setMessageCtx(ctx_addr, sndr_addr, sndr_pk, value):
#     contract = w3.eth.contract(address=ctx_addr, abi=res_abi)
#     tx = contract.functions.writeText(value).build_transaction({
#         'from' : sndr_addr,
#         'nonce' : w3.eth.get_transaction_count(sndr_addr),
#         'gasPrice': 200000
#     })

#     signed_tx = w3.eth.account.sign_transaction(tx, sndr_pk)
#     tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
#     tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

#     print(tx_receipt)
    
#     now = datetime.now() # current date and time
#     date_time = now.strftime("%m/%d/%Y, %H:%M:%S")    
#     log_row = date_time + ";" + tx_receipt['transactionHash'].hex()  + ";" +  str(tx_receipt['blockNumber'])  + ";" +  str(tx_receipt['cumulativeGasUsed']) + ";" +  str(tx_receipt['gasUsed'])  + ";" +  tx_receipt['from']  + ";" +  tx_receipt['to']  + ";" +  str(tx_receipt['effectiveGasPrice']) + ";\n"
#     writeGanacheLog(file_name,log_row)
    
#     return tx_receipt['transactionHash'].hex()


# def readMessageFromHash(tx_hash, sndr_addr):    
#     tx = w3.eth.get_transaction(tx_hash)
#     ctx_address = tx['to']    
#     contract = w3.eth.contract(address=ctx_address, abi=res_abi)
#     restricted_text = contract.functions.readText().call({'from' : sndr_addr})
#     print(restricted_text)
#     return restricted_text

# def readMessageFromContract(ctx, sndr_addr):    
#     contract = w3.eth.contract(address=ctx, abi=res_abi)
#     restricted_text = contract.functions.readText().call({'from' : sndr_addr})
#     print(restricted_text)
#     return restricted_text


# def grantAccessToAccount(ctx, owner, acc, allow):

#     allowing = False
   
#     if int(allow) == 1:
#         allowing = True
        

#     contract = w3.eth.contract(address=ctx, abi=res_abi)
#     tx_hash = contract.functions.grantAccess(acc, allowing).transact({
#         'from': owner, 
#         'nonce' : w3.eth.get_transaction_count(owner),
#         'gasPrice': 200000
#     })

   

#     try:
#         tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
#         print(tx_receipt)
#     except:
#         res_message = 'Error Editing Access'

#     try:
#         restricted_text = contract.functions.readText().call({'from': acc})
#         print("Restricted Text from Allowed Account:", restricted_text)
#         res_message = 'Access Enabled'
#     except:
#         res_message = 'Access Disabled'

#     return res_message

# #1-#36 blockchain (web3)

# from flask import Flask, render_template, request, jsonify
# from markupsafe import escape
# import json

# log_header = 'timestamp ;txHash ;blockNumber ;cumulativeGasUsed ;gasUsed ;from ;to ;effectiveGasPrice; \n' 
# with open('output_log/'+ file_name+ '.csv', 'w') as f:
#     f.write(log_header)

# app = Flask(__name__)

# @app.route("/")
# def index():
#     #debugStr = "<p>Abi: " + str(abi) + "<br>Bytecode: " + str(bytecode) + "</p>"    
#     return render_template('index.html')

# @app.route("/set_message", methods=['POST'])
# def setMessage():
#     res_message = '-'
#     # print(request.method)
#     if request.method == 'POST':
#         sender_address = request.form['sender_address']
#         sender_pk = request.form['sender_pk']
#         address = request.form['address']
#         value = request.form['value']
#         res_message = setMessageCtx(address, sender_address, sender_pk, value)
#         print(res_message)
#     else:
#         res_message = 'error'

#     return jsonify(
#         message_text = res_message 
#     )



# @app.route("/get_message_hash", methods=['POST'])
# def getMessageHash():
#     message_text = ''
#     status = 'empty'    
#     if request.method == 'POST':     
#         tx_hash = request.form['tx_hash']
#         sender_address = request.form['sender_address']                
#         try:                        
#             message_text = readMessageFromHash(tx_hash, sender_address) #contract address created after deploying contract            
#         except:
#             message_text = 'error'
#         # return f"<p> Getting Message from Address : {escape(address)} <br>The Message : {escape(message_text)} </p>"
   
#     else:
#         message_text = 'wrong method'

#     return jsonify(
#         message_text = message_text
#     )

# @app.route("/get_message", methods=['POST'])
# def getMessageCtx():
#     message_text = ''
#     status = 'empty'    
#     if request.method == 'POST':     
#         contract_address = request.form['ctx_address']
#         sender_address = request.form['sender_address']                
#         try:                        
#             message_text = readMessageFromContract(contract_address, sender_address) #contract address created after deploying contract            
#         except:
#             message_text = 'error'
#         # return f"<p> Getting Message from Address : {escape(address)} <br>The Message : {escape(message_text)} </p>"
   
#     else:
#         message_text = 'wrong method'

#     return jsonify(
#         message_text = message_text
#     )
       
# @app.route("/grant_access", methods=['POST'])
# def grantAccess():
#     res_message = '-'
#     # print(request.method)
#     if request.method == 'POST':
#         owner_address = request.form['owner_address']
#         allow_address = request.form['allow_address']
#         ctx_address = request.form['ctx_address']
#         allowed = request.form['allowed']     
#         print(allowed)   
#         res_message = grantAccessToAccount(ctx_address, owner_address, allow_address, allowed)
#         print(res_message)
#     else:
#         res_message = 'error'

#     return jsonify(
#         message_text = res_message 
#     )