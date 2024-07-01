from brownie import project, network, accounts

def main():
    # Load Brownie project
    p = project.load('brownie-dir')
    p.load_config()

    # Connect to the network (replace 'development' with your network)
    network.connect('development')
    ReentrancyAttackSuccess = p.VulnerableContract
    ReentrancyAttackPrevent = p.ProtectedContract
    # Menghubungkan dengan akun di Ganache atau jaringan lainnya
    dev = accounts[3]  # Ganti dengan private key Anda atau menggunakan accounts[0] jika menggunakan Ganache GUI

    # Deploy kontrak ReentrancyAttackSuccess
    print("Deploying ReentrancyAttackSuccess...")
    success_contract = ReentrancyAttackSuccess.deploy({'from': dev})
    print(f"ReentrancyAttackSuccess deployed at: {success_contract.address}")

    # Deploy kontrak ReentrancyAttackPrevent
    print("\nDeploying ReentrancyAttackPrevent...")
    prevent_contract = ReentrancyAttackPrevent.deploy({'from': dev})
    print(f"ReentrancyAttackPrevent deployed at: {prevent_contract.address}")

if __name__ == "__main__":
    main()
