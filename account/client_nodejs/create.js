const algosdk = require('algosdk');

var account = algosdk.generateAccount();
var passphrase = algosdk.secretKeyToMnemonic(account.sk);
var isValid = algosdk.isValidAddress(account.addr);
console.log("My address: " + account.addr);
console.log("My passphrase: " + passphrase);
console.log(isValid);