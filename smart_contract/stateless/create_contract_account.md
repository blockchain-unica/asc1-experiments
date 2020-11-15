## Smart Contract

#### Create a Contract Account

Writing a simple smart contract that works as a contract account.

We created the following file called sample.teal within our node folder.

```
algorand@b89f2bc2d65b:/opt/algorand/node$ cat sample.teal
// Check the Fee
txn Fee
int 10000
<=
arg 0
len
int 73
==
&&
// The sha256 value of the passphrase
arg 0
sha256
byte base64 G/Pk8y3Rzy9eyowgCdx+NREYyIxYR4BeFuTpMESfz10=
==
&&
// The CloseRemainderTo address must be equal to the receiver address
txn CloseRemainderTo
txn Receiver
==
&&
algorand@b89f2bc2d65b:/opt/algorand/node$
```

The meaning of this program is fully explained in [here](https://developer.algorand.org/tutorials/writing-simple-smart-contract/#step-1).

Compiling the .teal program we obtained the following address.

```
algorand@b89f2bc2d65b:/opt/algorand/node$ goal clerk compile sample.teal
sample.teal: HQALLYAILGTWTDWI56XH7BPSPMX3SWSNIB735NDYDP3SF3RMUPGBPPUKVA
algorand@b89f2bc2d65b:/opt/algorand/node$
```

We have created a new address that can be used as a normal account address.

[Algorand's Doc - Using SDKs with Stateless Smart Contracts](https://developer.algorand.org/docs/features/asc1/stateless/sdks/) 

------