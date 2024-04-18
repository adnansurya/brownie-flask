from brownie import MessageStorage, RestrictedText, accounts

def main():

    admin = accounts[0]  #first index account in ganache as admin

    #deploy contract using the admin account
    # contractDeploy = MessageStorage.deploy({
    #     "from" : admin
    # })

    contractDeploy = RestrictedText.deploy({
        "from" : admin
    })
    print(contractDeploy)