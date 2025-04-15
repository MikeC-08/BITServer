// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BIT{
    address public creator;
    mapping(address => bool) public itemsCreatorManager;
    mapping(address => bool) public itemsCreator;
    mapping(uint32 => address) public sub_items;

    constructor() {
        creator = msg.sender;
        itemsCreatorManager[creator] = true;
        itemsCreator[creator] = true;
    }
    event Received(address sender, uint amount);
    receive() external payable {
        emit Received(msg.sender, msg.value);
    }
        


    function setItemsCreator(address _target, bool _permission) public{
        require(itemsCreatorManager[creator] == true, "You do not have items Creator Manager permissions");
        itemsCreator[_target] = _permission;
    }
    modifier itemsCreatorReq() {
        require(itemsCreator[creator] == true, "You do not have items Creator permissions");
        _;
    }

    function getSubItemAddress(uint32 _subitem) public view returns (address){
        return sub_items[_subitem];
    }

    function addNewSubItemAddrWithID(uint32 _id, address _newSubItemAddr) itemsCreatorReq public{
        require(sub_items[_id] == 0x0000000000000000000000000000000000000000, "Duplicated item ID");
        sub_items[_id] = _newSubItemAddr;
    }

}