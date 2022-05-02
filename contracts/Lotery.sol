// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;


contract Lotery {
    address public owner;
    address[] public partisipants;

    constructor() {
        owner = msg.sender;
    }

    function getBalance() public view returns(uint) {
        return address(this).balance;
    }

    function getParticipants() public view returns(address[] memory) {
        return partisipants;
    }

    function enter() public payable {
        require(msg.value > .01 ether);

        partisipants.push(msg.sender);
    }

    function getRandom() public view returns(uint) {
        return uint(keccak256(abi.encodePacked(block.timestamp, block.difficulty, msg.sender)));
    }

    function pickRandomWinner() public returns(address){
        require(msg.sender == owner, "only owner can pick winner"); 
        require(partisipants.length > 0, "should be at least one partisipant"); 

        uint winnerId;
        if (partisipants.length == 1) {
            winnerId = 0;
        } else {
            winnerId = getRandom() % partisipants.length;   
        }
        address winner = partisipants[winnerId];
        payable(winner).transfer(address(this).balance);
        
        // reset partisipants array
        partisipants = new address[](0);

        return winner;
    }
}