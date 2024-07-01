from brownie import project, network, accounts, web3

# Load Brownie project
p = project.load('brownie-dir')
p.load_config()

# Connect to the network (replace 'development' with your network)
network.connect('development')

# Access contracts from loaded project
VulnerableContract = p.VulnerableContract
AttackerContract = p.AttackerContract  # Adjust to your Attacker contract name

def test_reentrancy_attack_success():
    dev = accounts[0]  # Use the correct account index or use accounts.add() with the correct private key
    attacker = accounts[1]  # Use the correct account index or use accounts.add() with the correct private key

    # Deploy VulnerableContract
    vulnerable_contract = VulnerableContract.deploy({'from': dev})

    # Deploy AttackerContract and pass VulnerableContract address to constructor
    attacker_contract = AttackerContract.deploy(vulnerable_contract.address, {'from': attacker})

    # Set attacker as an authorized user
    vulnerable_contract.grantAccess(attacker_contract.address, True, {'from': dev})

    # Attempt reentrancy attack
    print("\nPerforming reentrancy attack on VulnerableContract...")

    # Send initial ether to the AttackerContract
    initial_balance = web3.eth.get_balance(attacker.address)
    tx = attacker.transfer(attacker_contract.address, web3.toWei(1, 'ether'))  # Send 1 ether to AttackerContract
    tx.wait(1)  # Wait for transaction to be mined

    # Call attack function to initiate reentrant calls
    attack_value = web3.toWei(2, 'ether')  # Try to withdraw 2 ether
    tx = attacker_contract.attack({'from': attacker, 'value': attack_value})
    tx.wait(1)  # Wait for transaction to be mined

    final_balance = web3.eth.get_balance(attacker.address)

    print(f"Initial balance: {initial_balance}")
    print(f"Final balance after attack: {final_balance}")

    # Check if attack was successful
    assert final_balance > initial_balance, "Reentrancy attack was not successful"

def test_reentrancy_attack_prevent():
    dev = accounts[0]  # Replace with correct account index or using accounts.add() with correct private key
    attacker = accounts[1]  # Replace with correct account index or using accounts.add() with correct private key

    # Deploy ProtectedContract
    protected_contract = ProtectedContract.deploy({'from': dev})

    # Set attacker as an authorized user
    protected_contract.grantAccess(attacker, True, {'from': dev})

    # Attempt reentrancy attack (should fail)
    print("\nAttempting reentrancy attack on ProtectedContract...")
    initial_balance = web3.eth.get_balance(attacker.address)
    try:
        protected_contract.writeText("Malicious Text", {'from': attacker, 'value': web3.toWei(1, 'ether')})
    except Exception as e:
        print(f"Exception encountered: {str(e)}")
    final_balance = web3.eth.get_balance(attacker.address)

    print(f"Initial balance: {initial_balance}")
    print(f"Final balance after failed attack: {final_balance}")

    # Ensure attack failed (transaction reverted)
    assert final_balance == initial_balance

# Main function to execute tests
def main():
    test_reentrancy_attack_success()
    test_reentrancy_attack_prevent()

# Ensure script runs main function when executed directly
if __name__ == "__main__":
    main()
