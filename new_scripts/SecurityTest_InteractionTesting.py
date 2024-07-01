import requests
from brownie import accounts, project, network

# Load Brownie project
p = project.load('brownie-dir')
p.load_config()

# Import contract after loading project
RestrictedText = p.RestrictedText

def test_set_message():
    # Ensure enough accounts are available for testing
    if len(accounts) < 2:
        accounts.add("0xa57b8527317729b9043ef7c0f4ee15d644a17cdcebb018a762e3afa24db6220e")
        accounts.add("0x50f5155b8f8828973814202f77e14de8159477cb02a4634ff15a5c9d0245968e")

    assert len(accounts) >= 2, "Need at least two accounts for testing"

    admin = accounts[0]
    user = accounts[1]
    contract = RestrictedText.deploy({"from": admin})
    
    # Grant access to another account
    contract.grantAccess(user, True, {"from": admin})
    
    # Set up the local Flask server details
    base_url = "http://127.0.0.1:5000"
    
    # Payload for /set_message endpoint
    payload = {
        "sender_address": user.address,
        "sender_pk": "test_private_key",  # Placeholder since we don't have actual private keys
        "address": contract.address,
        "value": "Hello, World!"
    }
    
    print(f"Payload for /set_message: {payload}")

    try:
        response = requests.post(f"{base_url}/set_message", data=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    data = response.json()
    assert "message_text" in data

def test_get_message():
    # Ensure enough accounts are available for testing
    if len(accounts) < 2:
        accounts.add("0xa57b8527317729b9043ef7c0f4ee15d644a17cdcebb018a762e3afa24db6220e")
        accounts.add("0x50f5155b8f8828973814202f77e14de8159477cb02a4634ff15a5c9d0245968e")

    assert len(accounts) >= 2, "Need at least two accounts for testing"

    admin = accounts[0]
    user = accounts[1]
    contract = RestrictedText.deploy({"from": admin})
    contract.grantAccess(user, True, {"from": admin})
    contract.writeText("Hello, World!", {"from": user})
    
    # Set up the local Flask server details
    base_url = "http://127.0.0.1:5000"
    
    # Payload for /get_message endpoint
    payload = {
        "ctx_address": contract.address,
        "sender_address": user.address
    }
    
    print(f"Payload for /get_message: {payload}")

    try:
        response = requests.post(f"{base_url}/get_message", data=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    data = response.json()
    assert data["message_text"] == "Hello, World!"

if __name__ == "__main__":
    # Ensure network is connected
    network.connect('development')
    test_set_message()
    test_get_message()
