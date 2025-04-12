// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/interfaces/IERC20.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
using SafeERC20 for IERC20;


// interface IERC20 { 
//     // function transfer(address _to, uint256 _value) external returns (bool);
//     function balanceOf(address account) external view returns (uint256);
//     function approve(address _spender, uint256 _value) external returns (bool);
//     function transferFrom(address _from, address _to, uint256 _value) external returns (bool);
// }


contract GameAsset is ERC721 {
    address public owner;
    bool public isList;
    uint256 public price_in_uUSDC;
    string public AssetMetadata; //IPFS Hash
    IERC20 public USDC;
    address public BITAddress;

    // show change log in chain
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner, uint256 indexed price_in_uUSDC);
    constructor(address _BITAddress, string memory _IPFS_CID,address _init_owner) ERC721("BIT_Asset", "BIT_GA") {
        BITAddress = _BITAddress;
        AssetMetadata = _IPFS_CID; // Bind to a IPFS Hash
        owner = _init_owner;
        isList = false;
        price_in_uUSDC = 100; // Defualt price| 1,000,000uUSDC = 1 USDC
        USDC = IERC20(address(0xB4AcC2D7E94Eb1188Fd91c5b5F0B3aD06A140541)); // USDC Address
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the Asset owner can call this function");
        _;
    }

    modifier onlyAvailable() {
        require(isList == true, "The Asset is not available now");
        _;
    }

    function setAvailable(bool newIslist) public onlyOwner{
        isList = newIslist;
    }

    function setPrice(uint256 newPrice) public onlyOwner{
        price_in_uUSDC = newPrice;
    }  

    // Not for trade. Just a gift funcion.
    function transferOwnership(address newOwner) public onlyOwner {
        require(newOwner != address(0), "Invalid new owner address");
        emit OwnershipTransferred(owner, newOwner, price_in_uUSDC);
        owner = newOwner;
    }


    function Purchase() public onlyAvailable{
        require(USDC.allowance(address(msg.sender), address(this)) == price_in_uUSDC, "Approval failed"); // when buyer use this function, give approval to this contract to transfer USDC.
        // require(USDC.safeTransferFrom(msg.sender , owner, price_in_uUSDC), "Failed to send USDC");// once the contract get approval, transfer the USDC to owner.
        
        // USDC.forceApprove(address(this), price_in_uUSDC);
        
        USDC.safeTransferFrom(address(msg.sender) , address(owner), price_in_uUSDC);
        
        // transferOwnership after payment
        address newOwner = address(msg.sender);
        emit OwnershipTransferred(owner, newOwner, price_in_uUSDC);
        owner = newOwner;
        isList = false;
    }
}
