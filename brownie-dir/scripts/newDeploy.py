from brownie import project, network, accounts

def deploy_and_get_address():
    # Load Brownie project
    p = project.load('brownie-dir')
    p.load_config()

    # Connect to the network (replace 'development' with your network)
    network.connect('development')

    # Use the fourth account as the deployer (replace with the correct account)
    deployer = accounts[3]

    # Deploy the NewContract
    NewContract = p.NewContract
    deployed_contract = NewContract.deploy({'from': deployer})

    # Get the contract address
    contract_address = deployed_contract.address

    print(f"Contract deployed at address: {contract_address}")

    # Disconnect from the network
    network.disconnect()

    return contract_address

if __name__ == "__main__":
    deploy_and_get_address()
