// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VulnerableContract {
    string private restrictedText;
    mapping(address => bool) public access;
    address private owner;

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

    function writeText(string memory _newText) public payable {
        require(access[msg.sender] || msg.sender == owner, "You do not have permission to write the text");

        // Simulate reentrancy vulnerability by transferring Ether before state changes
        address payable sender = payable(msg.sender);
        sender.transfer(msg.value); // Ensure Ether is transferred first

        // Now update the state
        restrictedText = _newText;
        emit TextChanged(_newText, msg.sender);
    }

    function readText() public view returns (string memory) {
        require(access[msg.sender], "You do not have permission to read the text");
        return restrictedText;
    }

    receive() external payable {} // Ensure contract can receive ether
}
