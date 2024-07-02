from eth_account import Account
import os

# Fungsi untuk mengenerate kunci privat dan alamat pengirim
def generate_sender_address():
    # Mengenerate kunci privat random
    private_key = os.urandom(32)
    
    # Membuat akun menggunakan kunci privat
    account = Account.from_key(private_key)
    
    return {
        "private_key": account.key.hex(),
        "address": account.address
    }

# Generate alamat pengirim
# sender_address = generate_sender_address()

# print(f"Private Key: {sender_address['private_key']}")
# print(f"Address: {sender_address['address']}")