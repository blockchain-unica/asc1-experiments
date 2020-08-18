## Smart Contract

#### Re-create a Contract Account

Before starting this tutorial, there are some important premises that need to be made.

We previously created a contract account following the instruction showed [here](https://github.com/blockchain-unica/asc1-experiments/blob/master/smart_contract/create_contract_account.md#create_contract_account). Then, we closed the account as explained [here](https://github.com/blockchain-unica/asc1-experiments/blob/master/smart_contract/close_contract_account%20copy.md#close_contract_account).

We defined the same private key of 73 letters

```
attack at the dawm snake verbs ranch fruit Italy apple tree woman male at
```

Then, we codified this key obtaining a base64 string.

```
PS C:\Users\Cristian Lepore\Downloads\sandbox> python3 -c "import hashlib;import base64;print(base64.b64encode(hashlib.sha256(str('attack at the dawm snake verbs ranch fruit Italy apple tree woman male at').encode('utf-8')).digest()).decode('utf-8'))"
G/Pk8y3Rzy9eyowgCdx+NREYyIxYR4BeFuTpMESfz10=
PS C:\Users\Cristian Lepore\Downloads\sandbox> 
```

We wrote and compiled the program as described [here](https://github.com/blockchain-unica/asc1-experiments/blob/master/smart_contract/create_contract_account.md#create_contract_account).

```
algorand@b89f2bc2d65b:/opt/algorand/node$ cat sample.teal
// Check the Fee is resonable
// In this case 10,000 microalgos
txn Fee
int 10000
<=
// Check the length of the passphrase is correct
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
// Make sure the CloseRemainderTo is not set
txn CloseRemainderTo
txn Receiver
==
&&
algorand@b89f2bc2d65b:/opt/algorand/node$
```

We compiled the program as described below.

```
algorand@b89f2bc2d65b:/opt/algorand/node$ goal clerk compile sample.teal
sample.teal: HQALLYAILGTWTDWI56XH7BPSPMX3SWSNIB735NDYDP3SF3RMUPGBPPUKVA
algorand@b89f2bc2d65b:/opt/algorand/node$
```

We now have the same contract account with the same address as the closed one. This address can be refund and receive any transactions.

------