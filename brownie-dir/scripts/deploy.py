from brownie import *
p = project.load('brownie-dir')
p.load_config()

from brownie.project.BrownieDirProject import *
RestrictedText = p.RestrictedText

def deploy_contract():
    admin = accounts[0]
    contract = RestrictedText.deploy({'from': admin})
    print(f"Contract deployed at address: {contract.address}")
    return contract

def main():
    network.connect('development')
    contract = deploy_contract()

if __name__ == "__main__":
    main()