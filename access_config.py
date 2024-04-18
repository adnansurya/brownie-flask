from brownie import *
p = project.load('brownie-dir')
p.load_config()

from brownie.project.BrownieDirProject import *

res_abi = RestrictedText.abi
res_bytecode = RestrictedText.bytecode

from web3 import Web3
import global_variables as gv


# Inisialisasi Web3 dengan alamat node Ethereum (misalnya, Ganache)
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Alamat kontrak pintar dan ABI (Interface Kontrak)
contract_address = gv.acc1.addr


# Inisialisasi kontrak pintar
contract = web3.eth.contract(address=contract_address, abi=res_abi)

# Alamat pengirim (pemilik kontrak)
owner_address = '0x9fcF6fa3f16c4570B5F68EAA576718d18725fCB2'

# Alamat yang ingin ditambahkan atau dihapus aksesnya
address_to_grant = '0xef31eCf71605E32C54EC25BF31d08eF240ae2e31'

# Status akses yang ingin diberikan (True untuk memberikan akses, False untuk mencabut akses)
allow_access = True

# Panggil fungsi grantAccess pada kontrak pintar untuk menambahkan atau menghapus akses
tx_hash = contract.functions.grantAccess(address_to_grant, allow_access).transact({
        'from': owner_address, 
        'nonce' : web3.eth.get_transaction_count(owner_address),
        'gasPrice': 200000
    })

# Tunggu hingga transaksi berhasil
web3.eth.wait_for_transaction_receipt(tx_hash)

# Panggil fungsi readText pada kontrak pintar untuk membaca teks
restricted_text = contract.functions.readText().call()

print("Restricted Text:", restricted_text)
