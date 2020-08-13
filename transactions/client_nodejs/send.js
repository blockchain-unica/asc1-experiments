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

    let params = await algodClient.getTransactionParams().do();
    // comment out the next two lines to use suggested fee
    params.fee = 1000;
    params.flatFee = true;
    const receiver = "JYZOLEPL6FXPIDAMTYTANR4U5OLQ3HE4Q2QKW7J3JU3PGLQGOMBE5SC2HQ";
    let note = algosdk.encodeObj("Hello World");

    let txn = algosdk.makePaymentTxnWithSuggestedParams(myAccount.addr, receiver, 10000000, undefined, note, params);

    let signedTxn = txn.signTxn(myAccount.sk);
    let txId = txn.txID().toString();
    console.log("Signed transaction with txID: %s", txId);

    await algodClient.sendRawTransaction(signedTxn).do();
})().catch(e => {
    console.log(e);
});