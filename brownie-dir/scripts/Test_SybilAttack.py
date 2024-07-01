from brownie import *
p = project.load('brownie-dir')
p.load_config()

from brownie.project.BrownieDirProject import *
RestrictedText = p.RestrictedText

def deploy_contract():
    admin = accounts[3]
    contract = RestrictedText.deploy({'from': admin})
    print(f"Contract deployed at address: {contract.address}")
    return contract

def simulate_sybil_attack(contract):
    attacker1 = accounts.add('0xd0c4c9f9d4b60b1eaeca51212eee251b01fcbcd7b7750054c957105722930389')
    attacker2 = accounts.add('0xe0be693d7f7259bb2bc723f573b1c987ecde90753d5bc5c0b7cb17feab67aea2')

    # Attacker1 writes malicious text
    malicious_text = "This is a malicious text!"
    contract.writeText(malicious_text, {'from': attacker1})

    # Attacker2 reads the text
    retrieved_text = contract.readText({'from': attacker2})
    print(f"Retrieved text by attacker: {retrieved_text}")

    return malicious_text, retrieved_text


def main():
    network.connect('development')
    contract = deploy_contract()
    admin = accounts[3]

    print("\nSimulating Sybil attack:")
    malicious_text, retrieved_text = simulate_sybil_attack(contract)
    assert malicious_text == retrieved_text, "Sybil attack simulation failed!"


if __name__ == "__main__":
    main()