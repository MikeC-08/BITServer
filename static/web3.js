const ethereumButton = document.querySelector(".enableEthereumButton")
let connectedAccount = null
const showAccountText = document.querySelector(".showAccount")


ethereumButton.addEventListener("click", () => {
  getAccount()
})

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
  let addressStr = document.getElementById("address").innerHTML;

  purchaseButton.addEventListener("click", () => {
    path = "/transaction?address=" + connectedAccount + "&price=" + priceValue + "&asset=" + addressStr
    fetch(path)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log(data);
      gasPriceText.innerHTML = data.gasPrice/1000000000 + " Wei/Unit";
      estimateGasText.innerHTML = data.gas + " Units";
      gasFeeText.innerHTML = data.gas * data.gasPrice / 1000000000 + " Wei";
      platformFeeText.innerHTML = priceValue * 0.05 + " USDT";
      
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });


      confirmBlock.style.display = 'block';
  });

  confirmButton.addEventListener("click", () => {
    // 在確認按鈕上添加的點擊事件處理程序
});

};