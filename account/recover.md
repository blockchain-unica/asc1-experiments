## Account

#### Recover an account

This is the process to recover an account.

We have previously created an account funded with 100 Algos. Then, we deleted the account following the same procedure as described [here](https://github.com/blockchain-unica/asc1-experiments/blob/master/account/delete.md#delete_account).

To recover the previously deleted account we need to start recovering the wallet by typing ```./goal wallet new newWallet -r```. Then, you will need to prompt your recovery mnemonic and choose a password.

```
algorand@275e965cc9fb:/opt/algorand/node$ ./goal wallet new newWallet -r
Please type your recovery mnemonic below, and hit return when you are done:
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
Please choose a password for wallet 'newWallet':
Please confirm the password:
Creating wallet...
Created wallet 'newWallet'
```

Now, you can procede by restoring the old account as follows.

```
algorand@275e965cc9fb:/opt/algorand/node$ ./goal account new -w newWallet
Please enter the password for wallet 'newWallet':
Created new account with address 5HFGHOGBGHFDA7BFZBRXC73Y3BJ644B4ZAYX3LY3S6WKFJFZKGRNNOSDRE
algorand@275e965cc9fb:/opt/algorand/node$ ./goal account list -w newWallet
[offline]       Unnamed-0       5HFGHOGBGHFDA7BFZBRXC73Y3BJ644B4ZAYX3LY3S6WKFJFZKGRNNOSDRE      100000000 microAlgos    *Default
```

[Algorand's Doc - goal wallet new](https://developer.algorand.org/docs/reference/cli/goal/wallet/new/) 
