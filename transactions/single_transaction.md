## Transactions

#### Single transaction - no sign

This is the process to create and send a single transaction from one address to another.

```
./sandbox enter
```

You can now interact with the node and run commands from within the container.

```
$ ./sandbox enter
Entering /bin/bash session in the sandbox container...
```

Be sure to have a wallet. You can verify your wallet ID by typing the command ```./goal wallet list``` from within the shell.

```
Aalgorand@1238443847f0:/opt/algorand/node$ ./goal wallet list
##################################################
Wallet: myWallet (default)
ID:     363b261e61c294cd85d890fa08202234
##################################################
```

We previously created two accounts. See the account list typing the command ```./goal account list```

```
algorand@1238443847f0:/opt/algorand/node$ ./goal account list
Please enter the password for wallet 'myWallet':
[offline]       Unnamed-0       GKQFFBB74PQY7KS5T5A73NPNGQKWOO2GHVRXKS2NEGXYKLANAOP74U3EE4      100000000 microAlgos    *Default
[offline]       Unnamed-1       HUUQGQ3MTIZLRNCANCPWJGD2VJAGKCLDJFVRYWQSTIJILQ6HEZUOJNWUW4      0 microAlgos
```

Construct a payment transaction to send 1 Algo as follows. You can write some notes, for example "Hello World" that will be send with the transaction. The minimum fee is 1000 microAllgos.

```
algorand@1238443847f0:/opt/algorand/node$ ./goal clerk send --from=GKQFFBB74PQY7KS5T5A73NPNGQKWOO2GHVRXKS2NEGXYKLANAOP74U3EE4 --to=HUUQGQ3MTIZLRNCA
NCPWJGD2VJAGKCLDJFVRYWQSTIJILQ6HEZUOJNWUW4 --fee=1000 --amount=1000000 --note="Hello World" --out="hello-world.txn"
```

Sign the transaction. Then, it will be requested to add your wallet password.

```
algorand@1238443847f0:/opt/algorand/node$ ./goal clerk sign --infile="hello-world.txn" --outfile="hello-world.stxn"
Please enter the password for wallet 'myWallet':
```

Submit the transaction.

```
algorand@1238443847f0:/opt/algorand/node$ ./goal clerk rawsend --filename="hello-world.stxn"
Raw transaction ID RBUH65P6OPXZ7JDULP6VQD4B45QQT3DETNYY7LXB7IXVX2CI3KQQ issued
Transaction RBUH65P6OPXZ7JDULP6VQD4B45QQT3DETNYY7LXB7IXVX2CI3KQQ still pending as of round 8526020
Transaction RBUH65P6OPXZ7JDULP6VQD4B45QQT3DETNYY7LXB7IXVX2CI3KQQ committed in round 8526022
```

Wait for confirmation and check if your transaction was executed.

```
algorand@1238443847f0:/opt/algorand/node$ ./goal account list
Please enter the password for wallet 'myWallet':
[offline]       Unnamed-0       GKQFFBB74PQY7KS5T5A73NPNGQKWOO2GHVRXKS2NEGXYKLANAOP74U3EE4      98999000 microAlgos     *Default
[offline]       Unnamed-1       HUUQGQ3MTIZLRNCANCPWJGD2VJAGKCLDJFVRYWQSTIJILQ6HEZUOJNWUW4      1000000 microAlgos
```

You should now find the new value into your account deposit.

[Algorand's Doc - Your first transaction](https://developer.algorand.org/docs/build-apps/hello_world/) 

------