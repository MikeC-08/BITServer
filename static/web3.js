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
  showAccountText.innerHTML = 'Connected ' + account
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
    showAccountText.innerHTML = 'Connect to MetaMask'
  } else if (accounts[0] !== currentAccount) {
    // Reload your interface with accounts[0].
    currentAccount = accounts[0]
    connectedAccount = currentAccount
    // Update the account displayed (see the HTML for the connect button)
    showAccountText.innerHTML = 'Connected ' + currentAccount
  }
}
function giveApprove(assetAddress,allowPrice){
  const USDCAddress = '0xB4AcC2D7E94Eb1188Fd91c5b5F0B3aD06A140541'
  let hexWidth = 64; 
  let MethodID = '0x095ea7b3' // https://etherscan.io/methodidconverter

  let allowPrice_hex = allowPrice.toString(16)
  let leftAlignedAllowPrice_hex = allowPrice_hex.padStart(hexWidth, "0");
  let leftAlignedAssetAddress_hex = assetAddress.slice(2).padStart(hexWidth, "0");

  let approveData = MethodID + leftAlignedAssetAddress_hex + leftAlignedAllowPrice_hex
  console.log(approveData)
  // 0xfce353f6 61626300 00000000 00000000 00000000 00000000 00000000 00000000 00000000   64656600 00000000 00000000 00000000 00000000 00000000 00000000 00000000
  // 0x095ea7b3 Bf58718F 95C8b68f 90d592c3 43DD676c 5fD2f643 00000000 00000000 000000     b4c30000 00000000 00000000 00000000 00000000 00000000 00000000 00000000
  // 0xfce353f661626300000000000000000000000000000000000000000000000000000000006465660000000000000000000000000000000000000000000000000000000000
  // 0x095ea7b3Bf58718F95C8b68f90d592c343DD676c5fD2f643000000000000000000000000b4c3000000000000000000000000000000000000000000000000000000000000

  window.ethereum.request({
    "method": "eth_sendTransaction",
    "params": [
     {
        from: connectedAccount,
        to: USDCAddress,
        value: 0,
        data: approveData.toLowerCase(),
        // Customizable by the user during MetaMask confirmation.
        gasLimit: '0x5028',
        // Customizable by the user during MetaMask confirmation.
        maxPriorityFeePerGas: '0x3b9aca00',
        // Customizable by the user during MetaMask confirmation.
        maxFeePerGas: '0x2540be400',
     }
   ],
   })
   .then((txHash) => {
    
    console.log("tests");
    console.log(txHash);
    return true
  })
   .catch((error) => {
    console.error(error)
    console.log("Approve failed");
    return false
  });

}

window.onload = function() {
  let confirmButton = document.getElementsByClassName("confirmButton")[0];
  let confirmBlock = document.getElementById("confirmBlock");
  let purchaseButton = document.getElementsByClassName("purchaseButton")[0];

  let priceText = document.getElementById("priceConfirm");
  let gasPriceText = document.getElementById("gasPriceConfirm");
  let estimateGasText = document.getElementById("estimateGasConfirm");
  let gasFeeText = document.getElementById("gasFeeConfirm");
  let platformFeeText = document.getElementById("platformFeeConfirm");

  let priceValue = document.getElementById("price").innerHTML;
  let gasPriceValue = document.getElementById("gasPrice").innerHTML;
  let addressStr = document.getElementById("address").innerHTML;

  purchaseButton.addEventListener("click", () => {

    // approve estimate gas
    path = "/approve_transaction?address=" + connectedAccount + "&price=" + priceValue + "&asset=" + addressStr
    fetch(path)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log(data);

      if (confirm("Note: Approval requires a certain Gas Fee.\nGas Price: "+ gasPriceValue+" Wei/Unit\nEstimate Gas: " + data.gas + " Units\nGas Fee: " + data.gas * gasPriceValue +" Wei\nAre you sure you want to approve?") == true){
        path = "/transaction?address=" + connectedAccount + "&price=" + priceValue + "&asset=" + addressStr
        //giveApprove(USDCAddress, assetAddress, gas, data, allowPrice)
        hasApprove = giveApprove(addressStr, data.gas);
          if (hasApprove == true){
          fetch(path)
          .then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            return response.json();
          })
          .then(data => {
            console.log(data);
            gasPriceText.innerHTML = gasPriceValue + " Wei/Unit";
            estimateGasText.innerHTML = data.gas + " Units";
            gasFeeText.innerHTML = data.gas * gasPriceValue + " Wei";
            platformFeeText.innerHTML = priceValue * 0.05 + " uUSDT";
            
          })
          .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
          });

          confirmBlock.style.display = 'block';
          confirmButton.addEventListener("click", () => {
              // 在確認按鈕上添加的點擊事件處理程序
          });
        }
      }
      else{
        
      }
      
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });
    //
      
  });



};