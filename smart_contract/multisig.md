## Smart Contract

#### Multisig - Contract account + normal account

The goal of this test is to check if it is possible to pay an address, when we have a multisig account.
The multisig account is performed by a normal address and a contract account together.

First thing first, we created a wallet and an account.

```
algorand@5856b1252bfb:/opt/algorand/node$ goal wallet new myWallet
Please choose a password for wallet 'myWallet':
Please confirm the password:
Creating wallet...
Created wallet 'myWallet'
Your new wallet has a backup phrase that can be used for recovery.
Keeping this backup phrase safe is extremely important.
Would you like to see it now? (Y/n): n
algorand@5856b1252bfb:/opt/algorand/node$ goal account new
Please enter the password for wallet 'myWallet':
Created new account with address XCS3PTNQ2U72W44C5NPQGTLOQQLT2K52ZTQQ6CNIR56TMPVNVJ44OQE6AY
algorand@5856b1252bfb:/opt/algorand/node$
```

Startig from a teal program, we produced a contract account such as:

```
algorand@5856b1252bfb:/opt/algorand/node$ goal clerk compile sample.teal
sample.teal: 6Z3C3LDVWGMX23BMSYMANACQOSINPFIRF77H7N3AWJZYV6OH6GWTJKVMXY
algorand@5856b1252bfb:/opt/algorand/node$
```

In order to sign the transaction we need to delegate the signature of the contract account. This will be done as:

```
algorand@5856b1252bfb:/opt/algorand/node$ goal clerk compile sample.teal -o mydelegatedsig.lsig -s -a XCS3PTNQ2U72W44C5NPQGTLOQQLT2K52ZTQQ6CNIR56TMPVNVJ44OQE6AY -d data/
Please enter the password for wallet 'myWallet':
algorand@5856b1252bfb:/opt/algorand/node$
```

We now have a file called ```mydelegatedsig.lsig``` that can be used to sign any transaction on behalf of the sender.

We also produced a new account to be used within the multisign account.
```
UPQMPCYUSQO743TC45Y45N7XCQ5GINGNYTZJ6PMPCDZYT6MBHSJQLYXVSY
```

We are now ready to create a multisig account.

```
create a multisignature account
algorand@5856b1252bfb:/opt/algorand/node$ goal account multisig new UPQMPCYUSQO743TC45Y45N7XCQ5GINGNYTZJ6PMPCDZYT6MBHSJQLYXVSY 6Z3C3LDVWGMX23BMSYMANACQOSINPFIRF77H7N3AWJZYV6OH6GWTJKVMXY -T 2
Please enter the password for wallet 'myWallet':
Created new account with address CZBFYPZPBONDNO5CVIGKYI6A7CH6VF3R5NP22ZMNA6FQ4EN7JGVAYB62ZM
algorand@5856b1252bfb:/opt/algorand/node$
```

We can as usual verify these accounts by typing:
```
algorand@aa660d80813b:/opt/algorand/node$ goal account list
[offline]       Unnamed-1       UPQMPCYUSQO743TC45Y45N7XCQ5GINGNYTZJ6PMPCDZYT6MBHSJQLYXVSY      0 microAlgos
[offline]       Unnamed-0       XCS3PTNQ2U72W44C5NPQGTLOQQLT2K52ZTQQ6CNIR56TMPVNVJ44OQE6AY      0 microAlgos    *Default
[offline]       Unnamed-2       CZBFYPZPBONDNO5CVIGKYI6A7CH6VF3R5NP22ZMNA6FQ4EN7JGVAYB62ZM      0 microAlgos    [2/2 multisig]
algorand@aa660d80813b:/opt/algorand/node$
```

We create the output file, ready to be sent.

```
./goal clerk send --from=CZBFYPZPBONDNO5CVIGKYI6A7CH6VF3R5NP22ZMNA6FQ4EN7JGVAYB62ZM --to=CMTIY5FU45V6HT6DWOFYMUGHP6O7FRW64UXYHCYBXXLW7Q6KRFLTCOEQJY --fee=1000 --amount=500000 --note="Hello World" --out="out.txn"
```

The address must sign the transaction.

```
goal clerk multisig sign -t hello-world.txn -a UPQMPCYUSQO743TC45Y45N7XCQ5GINGNYTZJ6PMPCDZYT6MBHSJQLYXVSY
Please enter the password for wallet 'myWallet':
algorand@5856b1252bfb:/opt/algorand/node$
```

Finally, the contract account must sign the transaction.

```
goal clerk send -a 100000 -t CMTIY5FU45V6HT6DWOFYMUGHP6O7FRW64UXYHCYBXXLW7Q6KRFLTCOEQJY -L mydelegatedsig.lsig -d data/ -o hello-world.txn
```

The transaction is delivered.
```
./goal clerk rawsend --filename="hello-world.txn"
```

Final result:

```
algorand@aa660d80813b:/opt/algorand/node$ ./goal clerk rawsend --filename="hello-world.txn"
Raw transaction ID SWPOJITX6GP2WWEOA6A6XQXU5BS7W7LGPLCIIQCEAKO7STOZOVLQ issued
Transaction SWPOJITX6GP2WWEOA6A6XQXU5BS7W7LGPLCIIQCEAKO7STOZOVLQ still pending as of round 9019561
Transaction SWPOJITX6GP2WWEOA6A6XQXU5BS7W7LGPLCIIQCEAKO7STOZOVLQ committed in round 9019563
algorand@aa660d80813b:/opt/algorand/node$
```

------
