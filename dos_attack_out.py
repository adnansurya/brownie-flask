import requests
import random_acc
test_address = random_acc.generate_sender_address()
print(test_address)

url = 'http://127.0.0.1:5000/set_message'  # Replace with your desired URL
# data = {'sender_address': test_address, 'value': 'DOS ATTACK!'}  # Your data to send

contract_addr = '0xE20fEeB180423eEE0ffC2d4C0C48E9C188d60Cac'

def start_dos_attack(attack_limit):

    attack_count = 0
    while attack_count < attack_limit:
        print("Attack no.", attack_count)
        if attack_count >= attack_limit:
            break
        
        datatest = {
            "sender_address":  test_address['address'], 
            "value": "DOS ATTACK!", 
            "receiver_address" : test_address['address'], 
            "sender_pk" : test_address['private_key'],
            "address" :  contract_addr
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(url, data=datatest, verify=False, headers=headers)
        print(response.text)
        
        
        attack_count +=1
        
    print('DOS Attack Done')
    
start_dos_attack(1)