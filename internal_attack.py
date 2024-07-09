import requests
from web3 import Web3


w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
internal_accounts = w3.eth.accounts
internal_accounts_pk = ['4afdfc1d04c0e289d61664256e85293f2a30f7b7e5bbdaa5ace6815a429aac47', 
                        'c5d07a11345b9ab5f0c521afec138348d152b01af568e2a8b9229fc5b62e5b8b', 
                        '02722783ca21b0526a888201614e3787f42ebca9d4a21e77f0c30bc798d89c46', 
                        '31e2a52e3c31cf2896e07cf69cbee7aaf8711567f9677fa4ca54b20eb77b4436', 
                        '409294ac0cf7b46a3967958dd221551b4f3a4c2a49e849e94fb87d03cfadde18', 
                        'ce8b2e713c8657c9ed2bc551848650fe8b1a484e5abadae6c26fbfee6c254d92', 
                        'b18c7ac56c1e40ba65419cf95cc68dd94e469f3d76408290cc5935fa0447df47', 
                        'fc5947221f9192ffb41817e557e4d28e4309c2b941bfff959dadaff5ff0b46a9', 
                        '26841f9820ac08293a9aa1103dc07ee62f004cf003e3311be89ee3eb7d2690ba', 
                        '2b3ce1b22a9d298aa09e03f0812f07ae53d230d82255427216dba727ed2c4961']


contract_addr = '0xE20fEeB180423eEE0ffC2d4C0C48E9C188d60Cac'

setter_url = 'http://127.0.0.1:5000/set_message'  # Replace with your desired URL

getter_url = 'http://127.0.0.1:5000/get_message_hash'

headers = {"Content-Type": "application/x-www-form-urlencoded"}


def start_internal_attack(attack_limit):
    attack_count = 0
    attacker_index = 0
    while attack_count < attack_limit:
                    
        if attack_count >= attack_limit:
            break                       
        
        if attacker_index > 7:
            attacker_index = 0
            
        print("Attack no.", attack_count+1)
                
        setter_address = internal_accounts[attacker_index+2]
        setter_pk = internal_accounts_pk[attacker_index+2]
        print("By Account : " + setter_address)
        
        attacker_index +=1
        getter_address = internal_accounts[attacker_index+2]
        
        datatest = {
            "sender_address":  setter_address, 
            "value": "Internal Write ATTACK!", 
            "receiver_address" : getter_address, 
            "sender_pk" : setter_pk,
            "address" :  contract_addr
        }
        print(datatest)
        
        response = requests.post(setter_url, data=datatest, verify=False, headers=headers)
        print(response.text)
         
        print("By Account : " + getter_address)
        
        datatest = {
            "sender_address":  getter_address, 
            "value": "Internal Read ATTACK!", 
            "receiver_address" : getter_address, 
            "tx_hash" : "0x26d738d596424715b7a17524228fa410386aac98b2dd14c8278c9dfed7a72e0b"
        }
        
        response = requests.post(getter_url, data=datatest, verify=False, headers=headers)
        print(response.text)
                 
        attack_count +=1
        attacker_index +=1
                   
    print('Internal Attack Done')
    
start_internal_attack(10)
