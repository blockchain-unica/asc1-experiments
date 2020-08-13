const algosdk = require('algosdk');

const kmdtoken = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
const kmdserver = "http://localhost";
const kmdport = "4002";

const kmdclient = new algosdk.Kmd(kmdtoken, kmdserver, kmdport);

var walletid = null;
var wallethandle = null;

(async() => {
    let walletid = (await kmdclient.createWallet("MyTestWallet1", "testpassword", "", "sqlite")).wallet.id;
    console.log("Created wallet:", walletid);

    let wallethandle = (await kmdclient.initWalletHandle(walletid, "testpassword")).wallet_handle_token;
    console.log("Got wallet handle:", wallethandle);

    let address1 = (await kmdclient.generateKey(wallethandle)).address;
    console.log("Created new account:", address1);
})().catch(e => {
    console.log(e);
});