// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract MessageStorage {
    string public message;

    constructor() {
        setMessage('constructor message');
    }

    function setMessage(string memory _message) public {
        message = _message;
    }

    function getMessage() view public returns (string memory) {
        return message;
    }
}