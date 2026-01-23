// SPDX-License-Identifier: MIT
pragma solidity ^0.5.16;

contract HelloWorld {
    string public message;

    constructor() public {
        message = "Hello World";
    }

    function getMessage() public view returns(string memory) {
        return message;
    }
}

