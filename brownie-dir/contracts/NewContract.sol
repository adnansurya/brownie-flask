// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract NewContract {
    string private restrictedText;
    mapping(address => bool) public access;
    mapping(address => uint256) public nonces;
    mapping(bytes32 => bool) public executed; // Track executed transactions
    event TextChanged(string newText, address changer);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only contract owner can call this function");
        _;
    }

    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function grantAccess(address _address, bool _allowAccess) public onlyOwner {
        access[_address] = _allowAccess;
    }

    function writeText(string memory _newText, uint256 nonce, bytes memory signature) public {
        require(access[msg.sender] || msg.sender == owner, "You do not have permission to write the text");
        require(nonce == nonces[msg.sender] + 1, "Invalid nonce");
        
        bytes32 messageHash = keccak256(abi.encodePacked(address(this), _newText, nonce));
        require(!executed[messageHash], "Transaction already executed");
        require(recoverSigner(messageHash, signature) == msg.sender, "Invalid signature");

        restrictedText = _newText;
        nonces[msg.sender] = nonce;
        executed[messageHash] = true;
        emit TextChanged(_newText, msg.sender);
    }

    function readText() public view returns (string memory) {
        require(access[msg.sender], "You do not have permission to read the text");
        return restrictedText;
    }

    function recoverSigner(bytes32 messageHash, bytes memory signature) internal pure returns (address) {
        bytes32 ethSignedMessageHash = keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n32", messageHash));
        (bytes32 r, bytes32 s, uint8 v) = splitSignature(signature);
        return ecrecover(ethSignedMessageHash, v, r, s);
    }

    function splitSignature(bytes memory sig) internal pure returns (bytes32 r, bytes32 s, uint8 v) {
        require(sig.length == 65, "Invalid signature length");

        assembly {
            r := mload(add(sig, 32))
            s := mload(add(sig, 64))
            v := byte(0, mload(add(sig, 96)))
        }
    }
}
