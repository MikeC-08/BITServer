const ethereumButton = document.querySelector(".enableEthereumButton")
let connectedAccount = null
const showAccountText = document.querySelector(".showAccount")




ethereumButton.addEventListener("click", () => {
  getAccount()
})
window.ethereum // Or window.ethereum if you don't support EIP-6963.
  .on("chainChanged", handleChainChanged)

function handleChainChanged(chainId) {
  // We recommend reloading the page, unless you must do otherwise.
  window.location.reload()
  
}
// While awaiting the call to eth_requestAccounts, you should disable any buttons the user can
// select to initiate the request. MetaMask rejects any additional requests while the first is still
// pending.
async function getAccount() {
  const accounts = await window.ethereum // Or window.ethereum if you don't support EIP-6963.
    .request({ method: "eth_requestAccounts" })
    .catch((err) => {
      if (err.code === 4001) {
        // EIP-1193 userRejectedRequest error.
        // If this happens, the user rejected the connection request.
        console.log("Please connect to MetaMask.")
      } else {
        console.error(err)
      }
    })
  const account = accounts[0]
  connectedAccount = account
  showAccountText.innerHTML = '<img src="https://images.ctfassets.net/clixtyxoaeas/1ezuBGezqfIeifWdVtwU4c/d970d4cdf13b163efddddd5709164d2e/MetaMask-icon-Fox.svg" height="12px">'+' Connected <img src="https://images.ctfassets.net/clixtyxoaeas/1ezuBGezqfIeifWdVtwU4c/d970d4cdf13b163efddddd5709164d2e/MetaMask-icon-Fox.svg" height="12px">' + account
}

let currentAccount = null
window.ethereum // Or window.ethereum if you don't support EIP-6963.
  .request({ method: "eth_accounts" })
  .then(handleAccountsChanged)
  .catch((err) => {
    // Some unexpected error.
    // For backwards compatibility reasons, if no accounts are available, eth_accounts returns an
    // empty array.
    console.error(err)
  })

// Note that this event is emitted on page load. If the array of accounts is non-empty, you're
// already connected.
window.ethereum // Or window.ethereum if you don't support EIP-6963.
  .on("accountsChanged", handleAccountsChanged)



// eth_accounts always returns an array.
function handleAccountsChanged(accounts) {
  
  if (accounts.length === 0) {
    // MetaMask is locked or the user has not connected any accounts.
    console.log("Please connect to MetaMask.")
    showAccountText.innerHTML = 'Connect to <img src="https://images.ctfassets.net/clixtyxoaeas/1ezuBGezqfIeifWdVtwU4c/d970d4cdf13b163efddddd5709164d2e/MetaMask-icon-Fox.svg" height="12px">MetaMask<img src="https://images.ctfassets.net/clixtyxoaeas/1ezuBGezqfIeifWdVtwU4c/d970d4cdf13b163efddddd5709164d2e/MetaMask-icon-Fox.svg" height="12px">'
  } else if (accounts[0] !== currentAccount) {
    
    // Reload your interface with accounts[0].
    currentAccount = accounts[0]
    connectedAccount = currentAccount
    // Update the account displayed (see the HTML for the connect button)
    showAccountText.innerHTML = '<img src="https://images.ctfassets.net/clixtyxoaeas/1ezuBGezqfIeifWdVtwU4c/d970d4cdf13b163efddddd5709164d2e/MetaMask-icon-Fox.svg" height="12px">'+' Connected <img src="https://images.ctfassets.net/clixtyxoaeas/1ezuBGezqfIeifWdVtwU4c/d970d4cdf13b163efddddd5709164d2e/MetaMask-icon-Fox.svg" height="12px">' + currentAccount
    
    // get var
    let AssetAddress = document.getElementById("address").innerHTML.toLowerCase();
    let OwnerAddress = document.getElementById("owner").innerHTML.toLowerCase();
    let updatePriceButton = document.getElementById("updatePriceButton");
    let updateAvailableButton = document.getElementById("updateAvailableButton");
    let available = document.getElementById("available").innerHTML.toLowerCase();
    

    let ownerBlock = document.getElementById("ownerBlock");
    let purchaseButton = document.getElementsByClassName("purchaseButton")[0];
    let noAvailableText = document.getElementById('noAvailableText')
    // Check if available or not
    if(currentAccount == OwnerAddress || available == "false"){
      purchaseButton.classList.add('disabled');
      noAvailableText.style.display = 'block';
    }
    else{
      purchaseButton.classList.remove('disabled');
      noAvailableText.style.display = 'None';
    }

    if(currentAccount == OwnerAddress){
      ownerBlock.style.display = 'block';
    }
    else{
      ownerBlock.style.display = 'None';
      
    }
    // Check if owner
    updatePriceButton.addEventListener("click", function() {
      let newPrice = document.getElementById("newPrice").value;
      let currentPrice = document.getElementById("price").innerHTML;
      console.log(currentPrice == newPrice);
      if(currentPrice != newPrice){
        setNewPrice(AssetAddress, newPrice);
      }else{
        alert("Cannot set price to be the same or lower than 0.");
      }
    }
    )
    updateAvailableButton.addEventListener("click", function() {
        let newAvailable = null;
        let newAvailable_elements  = document.getElementsByName('available');
        let currentAvailable = document.getElementById("available").innerHTML;
        for(let i = 0; i < newAvailable_elements.length; i++){
          if(newAvailable_elements[i].checked == true){
            newAvailable = newAvailable_elements[i].value;
            break;
          }
        }

        if(currentAvailable != newAvailable){
          setNewAvailable(AssetAddress, newAvailable);
        }
        else{
          alert("Cannot set availability to be the same");
        }
      }
  )
  }
}

function transaction_sent(to, data, value=0){
  window.ethereum.request({
    "method": "eth_sendTransaction",
    "params": [
     {
        from: connectedAccount,
        to: to,
        value: value,
        data: data.toLowerCase(),
        // '0x5028' = Customizable by the user during MetaMask confirmation.
        gasLimit: '0x5028',
        // '0x3b9aca00' = Customizable by the user during MetaMask confirmation.
        maxPriorityFeePerGas: '0x3b9aca00',
        // '0x2540be400' = Customizable by the user during MetaMask confirmation.
        maxFeePerGas: '0x2540be400',
     }
   ],
   })
   .then((txHash) => {
    console.log(txHash);
    window.location.reload()
    return true, txHash
  })
   .catch((error) => {
    console.error(error)
    console.log("transaction failed");
    window.location.reload()
    return false, error
  });
}

function setNewAvailable(assetAddress, newAvailable){
  console.log(newAvailable);
  let hexWidth = 64; 
  let MethodID = '0xe2df20d1'; // setAvailable(bool) https://etherscan.io/methodidconverter
  if (newAvailable.toLowerCase() == 'true'){
    newAvailable = 1;
  }else{
    newAvailable = 0;
  }


  let firstVariable_hex = newAvailable.toString(16);
  console.log(firstVariable_hex)
  firstVariable_hex = firstVariable_hex.padStart(hexWidth, "0");


  let functionData = MethodID + firstVariable_hex;
  transaction_sent(assetAddress,functionData);
}

function setNewPrice(assetAddress, newPrice){
  let hexWidth = 64; 
  let MethodID = '0x91b7f5ed'; // setPrice(uint256) https://etherscan.io/methodidconverter
    
  let firstVariable_hex = parseInt(newPrice).toString(16);
  console.log(firstVariable_hex)
  firstVariable_hex = firstVariable_hex.padStart(hexWidth, "0");


  let functionData = MethodID + firstVariable_hex;
  transaction_sent(assetAddress,functionData);
}



function purchase(assetAddress){
  console.log('Purchasing')
  let MethodID = '0x49c15bd9'
  let plaformFee = document.getElementById('plaformFee').innerHTML; 
  // 0.000001 
  // 0.000000001
  // 0.000001
  // let firstVariable_hex = newPrice.toString(16);
  // console.log(firstVariable_hex)
  // firstVariable_hex = firstVariable_hex.padStart(hexWidth, "0");


  let functionData = MethodID;
  transaction_sent(assetAddress,functionData, "1".toString(16));
}
function clearApprove(assetAddress){
  let hexWidth = 64; 
  let MethodID = '0x095ea7b3'; // approve(address,uint256) https://etherscan.io/methodidconverter
  let currencyAddress = document.getElementById('currencyAddress');

  let allowPrice = 0;

  //0x095ea7b3  00000000 00000000 00000000 9a676e78 1a523b5d 0c0e4373 1313a708 cb607508   00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000
  //0x095ea7b3  00000000 00000000 00000000 2ba0aE59 fFEd8b01 5774AB70 a00C085a 7461604e   00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000
  let allowPrice_hex = parseInt(allowPrice).toString(16);
  let leftAlignedAllowPrice_hex = allowPrice_hex.padStart(hexWidth, "0");
  let leftAlignedAssetAddress_hex = assetAddress.slice(2).padStart(hexWidth, "0");

  let functionData = MethodID + leftAlignedAssetAddress_hex + leftAlignedAllowPrice_hex
  console.log("Clear: ", functionData);
  transaction_sent(currencyAddress,functionData);
}

function giveApprove(assetAddress,allowPrice){
  let hexWidth = 64; 
  let MethodID = '0x095ea7b3'; // approve(address,uint256) https://etherscan.io/methodidconverter
  let currencyAddress = document.getElementById('currencyAddress').innerHTML;
  console.log("Giving Allow(",allowPrice,") to:", assetAddress)
  console.log("currencyAddress: ",currencyAddress)

  let allowPrice_hex = parseInt(allowPrice).toString(16)
  let leftAlignedAllowPrice_hex = allowPrice_hex.padStart(hexWidth, "0");
  let leftAlignedAssetAddress_hex = assetAddress.slice(2).padStart(hexWidth, "0");

  let functionData = MethodID + leftAlignedAssetAddress_hex + leftAlignedAllowPrice_hex
  // 0xfce353f6 61626300 00000000 00000000 00000000 00000000 00000000 00000000 00000000   64656600 00000000 00000000 00000000 00000000 00000000 00000000 00000000
  // 0x095ea7b3 Bf58718F 95C8b68f 90d592c3 43DD676c 5fD2f643 00000000 00000000 000000     b4c30000 00000000 00000000 00000000 00000000 00000000 00000000 00000000
  // 0xfce353f661626300000000000000000000000000000000000000000000000000000000006465660000000000000000000000000000000000000000000000000000000000
  // 0x095ea7b3Bf58718F95C8b68f90d592c343DD676c5fD2f643000000000000000000000000b4c3000000000000000000000000000000000000000000000000000000000000
  transaction_sent(currencyAddress,functionData);
}

window.onload = function() {

  let purchaseButton = document.getElementsByClassName("purchaseButton")[0];
  let priceValue = document.getElementById("price").innerHTML;
  let addressStr = document.getElementById("address").innerHTML;




  purchaseButton.addEventListener("click", () => {
        check_approve_path  = "/check_approve?assetAddress=" + addressStr + "&buyer=" + connectedAccount + "&price="+ priceValue;
        fetch(check_approve_path)
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(data => {
          console.log(data)
          if(data.approved == 'True'){
            hasApprove = true;
            console.log('Already Approved');
            purchase(addressStr);
          }
          else{
            console.log('Not Approved. Requesting Approve.');
            if(data.allowance != 0){clearApprove(addressStr);}
            hasApprove = giveApprove(addressStr, priceValue);
            purchase(addressStr);
          }
        })
        .catch(error => {
          console.error('There was a problem with the fetch operation:', error);
        });
  });
};