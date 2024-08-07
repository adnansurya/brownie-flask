import requests
import random_acc


setter_url = 'http://127.0.0.1:5000/set_message'  # Replace with your desired URL

getter_url = 'http://127.0.0.1:5000/get_message_hash'

headers = {"Content-Type": "application/x-www-form-urlencoded"}

contract_addr = '0xE20fEeB180423eEE0ffC2d4C0C48E9C188d60Cac'


def start_sybil_attack(attack_limit):
    attack_count = 0
    
    while attack_count < attack_limit:
        if attack_count >= attack_limit:
            break                       
        
        print("Attack no.", attack_count+1)
                
        setter_address = random_acc.generate_sender_address()
        print(setter_address)
        
        getter_address = random_acc.generate_sender_address()
        print(getter_address)
        
        datatest = {
            "sender_address":  setter_address['address'], 
            "value": "Sybil Write ATTACK!", 
            "receiver_address" : getter_address['address'], 
            "sender_pk" : setter_address['private_key'],
            "address" :  contract_addr
        }
        
        response = requests.post(setter_url, data=datatest, verify=False, headers=headers)
        print(response.text)
        
     
        
        datatest = {
            "sender_address":  setter_address['address'], 
            "value": "Sybil Read ATTACK!", 
            "receiver_address" : getter_address['address'], 
            "tx_hash" : "0x26d738d596424715b7a17524228fa410386aac98b2dd14c8278c9dfed7a72e0b"
        }
        
        response = requests.post(getter_url, data=datatest, verify=False, headers=headers)
        print(response.text)
                 
        attack_count +=1
                   
    print('Sybil Attack Done')
    
start_sybil_attack(10)