from brownie import MessageStorage, accounts

def main():

    admin = accounts[0]  #first index account in ganache as admin

    #deploy contract using the admin account
    contractDeploy = MessageStorage.deploy({
        "from" : admin
    })

    print(contractDeploy)