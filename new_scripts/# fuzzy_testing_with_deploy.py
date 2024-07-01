# fuzzy_testing_with_deploy.py

from brownie import accounts, network, project
import random
import string

# Load Brownie project
p = project.load('brownie-dir')
p.load_config()

from brownie.project.BrownieDirProject import *

# Import contract after loading the project
RestrictedText = p.RestrictedText

# Modify your deploy_contract function to also grant access to the admin account
def deploy_contract():
    network.connect('development')  # Connect to local network (Ganache)

    # Add Ganache account using private key directly
    ganache_private_key = "0xf1ada957a8d0a24a4f4b1814c6580f5fc179b8f7564b6de8f4a6632602e8928c"
    admin = accounts.add(ganache_private_key)

    # Deploy the contract using the admin account
    contract_deployed = RestrictedText.deploy({'from': admin})
    print(f"Contract deployed at address: {contract_deployed.address}")

    # Grant access to the admin account
    contract_deployed.grantAccess(admin, True, {'from': admin})

    return contract_deployed, admin  # Return both deployed contract and admin account


# Function to perform random write and read operations
# Perform fuzzy testing function with admin account
def perform_fuzzy_testing(deployed_contract, admin):
    accounts_list = [admin]  # Use admin account directly for testing

    for _ in range(10):  # Perform 10 random operations
        account = random.choice(accounts_list)
        random_text = generate_random_string(random.randint(1, 50))

        # Perform random operation: write or read
        if random.choice([True, False]):
            tx = deployed_contract.writeText(random_text, {'from': account})
            print(f"Write operation by {account}: {tx.status}")
        else:
            try:
                text = deployed_contract.readText({'from': account})
                print(f"Read operation by {account}: {text}")
            except Exception as e:
                print(f"Read operation failed: {str(e)}")


# Function to generate random string
def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

if __name__ == "__main__":
    # Deploy the contract and obtain admin account
    deployed_contract, admin = deploy_contract()

    # Perform fuzzy testing on the deployed contract
    perform_fuzzy_testing(deployed_contract, admin)
