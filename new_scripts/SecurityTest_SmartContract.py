from brownie import accounts, project, network
import pytest

# Memuat proyek Brownie
p = project.load('brownie-dir')
p.load_config()

from brownie.project.BrownieDirProject import *

# Mengimpor kontrak setelah memuat proyek
RestrictedText = p.RestrictedText

def test_initial_owner():
    owner = accounts[0]
    contract = RestrictedText.deploy({"from": owner})
    assert contract.owner() == owner
    print("test_initial_owner passed")

def test_grant_access():
    owner = accounts[0]
    user = accounts[1]
    contract = RestrictedText.deploy({"from": owner})
    contract.grantAccess(user, True, {"from": owner})
    assert contract.access(user) == True
    print("test_grant_access passed")

def test_write_and_read_text():
    owner = accounts[0]
    user = accounts[1]
    contract = RestrictedText.deploy({"from": owner})
    contract.grantAccess(user, True, {"from": owner})
    contract.writeText("Hello, World!", {"from": user})
    assert contract.readText({"from": user}) == "Hello, World!"
    print("test_write_and_read_text passed")

def test_restricted_access():
    owner = accounts[0]
    unauthorized_user = accounts[1]
    contract = RestrictedText.deploy({"from": owner})
    with pytest.raises(Exception, match="You do not have permission to read the text"):
        contract.readText({"from": unauthorized_user})
    print("test_restricted_access passed")

if __name__ == "__main__":
    # Pastikan bahwa jaringan pengembangan telah terhubung
    network.connect('development')
    
    # Jalankan pengujian
    test_initial_owner()
    test_grant_access()
    test_write_and_read_text()
    test_restricted_access()
    
    # Putuskan koneksi jaringan setelah pengujian selesai
    network.disconnect()