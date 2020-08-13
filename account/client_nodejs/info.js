const algosdk = require('algosdk');

const algodToken = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
const algodServer = "http://localhost";
const algodPort = 4001;

let algodClient = new algosdk.Algodv2(algodToken, algodServer, algodPort);

const passphrase = "25-words mnemonic sentence";

let myAccount = algosdk.mnemonicToSecretKey(passphrase);
console.log("My address: %s", myAccount.addr);

(async() => {
    let accountInfo = await algodClient.accountInformation(myAccount.addr).do();
    console.log("Account balance: %d microAlgos", accountInfo.amount);
})().catch(e => {
    console.log(e);
});