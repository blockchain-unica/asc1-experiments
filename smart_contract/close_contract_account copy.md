## Smart Contract

#### Close a Contract Account

We have previously created a contract account as shown [here](https://github.com/blockchain-unica/asc1-experiments/blob/master/smart_contract/create_contract_account.md#create_contract_account).
This is the address of our contract accont.

```
HQALLYAILGTWTDWI56XH7BPSPMX3SWSNIB735NDYDP3SF3RMUPGBPPUKVA
```

We can refund this address and check its balance with the command

```
algorand@b89f2bc2d65b:/opt/algorand/node$ goal account balance -a HQALLYAILGTWTDWI56XH7BPSPMX3SWSNIB735NDYDP3SF3RMUPGBPPUKVA -d data/
100000000 microAlgos
algorand@b89f2bc2d65b:/opt/algorand/node$
```

This contract account cannot send transactions but only receives transactions from a different account.

We closed the contract account using this instruction from the CLI.

```
algorand@b89f2bc2d65b:/opt/algorand/node$ goal clerk send -a 7000000 --from-program sample.teal -c 6MUBRKC4KZL3J4BECZUMAXVQA55UVQ5LA7EFF2VBPZ2XIB7QPTKKWWPRDE --argb64 YXR0YWNrIGF0IHRoZSBkYXdtIHNuYWtlIHZlcmJzIHJhbmNoIGZydWl0IEl0YWx5IGFwcGxlIHRyZWUgd29tYW4gbWFsZSBhdA== -t 6MUBRKC4KZL3J
4BECZUMAXVQA55UVQ5LA7EFF2VBPZ2XIB7QPTKKWWPRDE -o out.txn -d data/
algorand@b89f2bc2d65b:/opt/algorand/node$ 
```

We sent out the transaction.

```
algorand@b89f2bc2d65b:/opt/algorand/node$ goal clerk rawsend -f out.txn -d data/
Raw transaction ID IKI2RYXK3KHVT3DJ5YZLEHM6IPERVB5S6APIP5IYRM44GNFT3NMA issued
Transaction IKI2RYXK3KHVT3DJ5YZLEHM6IPERVB5S6APIP5IYRM44GNFT3NMA still pending as of round 8687862
Transaction IKI2RYXK3KHVT3DJ5YZLEHM6IPERVB5S6APIP5IYRM44GNFT3NMA committed in round 8687864
algorand@b89f2bc2d65b:/opt/algorand/node$
```

The new balance of the contract accout is now zero.

```
algorand@b89f2bc2d65b:/opt/algorand/node$ goal account balance -a HQALLYAILGTWTDWI56XH7BPSPMX3SWSNIB735NDYDP3SF3RMUPGBPPUKVA
0 microAlgos
algorand@b89f2bc2d65b:/opt/algorand/node$
```

Once the contract account is closed, we can still send new transaction from a different account to the closed contract account. We used the previous code deployed [here](https://github.com/blockchain-unica/asc1-experiments/blob/master/transactions/client_nodejs/send.js). Be aware to modify the receiver and the passphrase.

[Algorand's Doc - Using SDKs with Stateless Smart Contracts](https://developer.algorand.org/docs/features/asc1/stateless/sdks/) 

------