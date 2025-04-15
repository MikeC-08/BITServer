// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/interfaces/IERC20.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
using SafeERC20 for IERC20;


// interface IERC20 { 
//     // function transfer(address _to, uint256 _value) external returns (bool);
//     function symbol() external view returns (string memory);
// }


contract GameAsset is ERC721 {
    address public owner;
    address public token_address;
    bool public isList;
    uint256 public price_in_uToken;
    string public AssetMetadata; //IPFS Hash
    IERC20 public Token;
    address payable public BITAddress;
    uint256 public platform_fee_eth;

    // show change log in chain
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner, uint256 indexed price_in_uToken, address token_address);
    constructor(address payable _BITAddress, string memory _IPFS_CID, address _init_owner, address _token_address, uint256 _platform_fee_eth) ERC721("BIT_Asset", "BITA") {
        BITAddress = _BITAddress;
        AssetMetadata = _IPFS_CID; // Bind to a IPFS Hash
        owner = _init_owner;
        isList = false;
        price_in_uToken = 999999; // Defualt price| 1,000,000uToken = 1 uToken
        token_address = _token_address;
        Token = IERC20(_token_address); // Token Address
        platform_fee_eth = _platform_fee_eth;
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
        price_in_uToken = newPrice;
    }  

    function sendEth(uint _value) private returns(bool) {
        BITAddress.transfer(_value);
        return true;
    }

    // Not for trade. Just a gift funcion.
    function transferOwnership(address newOwner) public payable onlyOwner {
        require(newOwner != address(0), "Invalid new owner address");
        require(msg.value == platform_fee_eth, "Please pay the correct platform fee.");
        
        // send to platform_fee to BIT
        require(sendEth(msg.value), "Failed to send Ether");

        
        emit OwnershipTransferred(owner, newOwner, 0, token_address);
        owner = newOwner;
    }


    function Purchase() public onlyAvailable payable {
        require(Token.allowance(address(msg.sender), address(this)) == price_in_uToken, "Approval failed."); // when buyer use this function, give approval to this contract to transfer Token.
        require(Token.balanceOf(address(msg.sender)) > price_in_uToken, "Tokens are not sufficient to purchase the underlying asset."); // when buyer use this function, give approval to this contract to transfer Token.
        require(msg.value == platform_fee_eth, "Please pay the correct platform fee.");


        require(sendEth(msg.value), "Failed to send Ether");

        Token.safeTransferFrom(address(msg.sender) , address(owner), price_in_uToken);

        // transferOwnership after payment
        emit OwnershipTransferred(owner, address(msg.sender), price_in_uToken, token_address);
        owner = address(msg.sender);
        // Set asset not available for public to Purchase
        isList = false;
    }
}
