// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ReentrancyAttackPrevent {
    string private restrictedText;
    mapping(address => bool) public access;
    address private owner;
    bool private reentrancyLock; // Mutex to prevent reentrancy

    event TextChanged(string newText, address changer);

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only contract owner can call this function");
        _;
    }

    function grantAccess(address _address, bool _allowAccess) public onlyOwner {
        access[_address] = _allowAccess;
    }

    function writeText(string memory _newText) public {
        require(access[msg.sender] || msg.sender == owner, "You do not have permission to write the text");
        require(!reentrancyLock, "Reentrant call detected");
        
        reentrancyLock = true;
        restrictedText = _newText;
        emit TextChanged(_newText, msg.sender);
        reentrancyLock = false;
    }

    function readText() public view returns (string memory) {
        require(access[msg.sender], "You do not have permission to read the text");
        return restrictedText;
    }
}
