import solcx
from brownie import accounts, project, Contract

# Set Solidity compiler version
solcx.set_solc_version('0.8.17')

# Load Brownie project
p = project.load('brownie-dir')
p.load_config()

# Assuming Contract_New is the unique contract name after renaming
Contract_New = p.Contract_New

# Deploy the contract
def deploy_contract():
    # Deploy the contract
    contract = Contract_New.deploy({'from': accounts[3]})
    return contract

# Simulate Reentrancy Attack
def simulate_reentrancy_attack(contract):
    # Prepare the attack transaction
    attack_value = "0.00001 ether"
    try:
        # Simulate calling writeText which initiates reentrancy
        tx = contract.writeText("Malicious text", {'from': accounts[4], 'value': attack_value})
        tx.wait(1)  # Wait for transaction receipt
        print("Reentrancy attack successful. Transaction hash:", tx.txid)
    except Exception as e:
        print(f"Reentrancy attack failed: {str(e)}")

# Main function to deploy contract and simulate attack
def main():
    # Deploy the contract
    contract = deploy_contract()
    print(f"Contract deployed at address: {contract.address}")

    # Simulate the reentrancy attack
    simulate_reentrancy_attack(contract)

if __name__ == '__main__':
    main()
