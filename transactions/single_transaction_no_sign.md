## Transactions

#### Single transaction

We would like to demonstrate that is possible to deliver a transaction without sign the transaction itself

You can now interact with the node and run commands from within the container.

```
$ ./sandbox enter
Entering /bin/bash session in the sandbox container...
```

Be sure to have a wallet. You can verify your wallet ID by typing the command ```./goal wallet list``` from within the shell.

```
algorand@1238443847f0:/opt/algorand/node$ ./goal wallet list
##################################################
Wallet: myWallet (default)
ID:     363b261e61c294cd85d890fa08202234
##################################################
```

We previously created two accounts. See the account list typing the command ```./goal account list```

```
algorand@1238443847f0:/opt/algorand/node$ ./goal account list
Please enter the password for wallet 'myWallet':
[offline]       Unnamed-0       HCQR36YHX3YP5IJX5XX776TDBQOQUQ3G4ZYMSLIPV2FL4GDA772HKSWIQU      100000000 microAlgos    *Default
[offline]       Unnamed-1       PENOKN5IT45O2C2AR6LWELMUDHCBDCR67SRJ72FIIN3ZMNTYF5ZZ6XSDEM      0 microAlgos
```

Construct a payment transaction to send 1 Algo as follows. You can write some notes, for example "Hello World" that will be send with the transaction. The minimum fee is 1000 microAllgos.

```
algorand@1238443847f0:/opt/algorand/node$ ./goal clerk send --from=GKQFFBB74PQY7KS5T5A73NPNGQKWOO2GHVRXKS2NEGXYKLANAOP74U3EE4 --to=HUUQGQ3MTIZLRNCA
NCPWJGD2VJAGKCLDJFVRYWQSTIJILQ6HEZUOJNWUW4 --fee=1000 --amount=1000000 --note="Hello World" --out="hello-world.txn"
```

We can inspect the content of the transaction using the command:

```
algorand@d0d0d4a939b9:/opt/algorand/node$ goal clerk inspect hello-world.txn -d data/
hello-world.txn[0]
{
  "txn": {
    "amt": 1000000,
    "fee": 1000,
    "fv": 9181699,
    "gen": "testnet-v1.0",
    "gh": "SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI=",
    "lv": 9182699,
    "note": "SGVsbG8gV29ybGQ=",
    "rcv": "PENOKN5IT45O2C2AR6LWELMUDHCBDCR67SRJ72FIIN3ZMNTYF5ZZ6XSDEM",
    "snd": "HCQR36YHX3YP5IJX5XX776TDBQOQUQ3G4ZYMSLIPV2FL4GDA772HKSWIQU",
    "type": "pay"
  }
}
```

Submit the transaction without any sign.

```
algorand@d0d0d4a939b9:/opt/algorand/node$ goal clerk send --argb64 MA== -t PENOKN5IT45O2C2AR6LWELMUDHCBDCR67SRJ72FIIN3ZMNTYF5ZZ6XSDEM -d d
ata/ --amount 5000000
Please enter the password for wallet 'myWallet':
Sent 5000000 MicroAlgos from account HCQR36YHX3YP5IJX5XX776TDBQOQUQ3G4ZYMSLIPV2FL4GDA772HKSWIQU to address PENOKN5IT45O2C2AR6LWELMUDHCBDCR
67SRJ72FIIN3ZMNTYF5ZZ6XSDEM, transaction ID: FZROPJHNYGT3AVAMG4343DLIP7J3RI5Q22HN3Y5KAA4Q7MUK2GXA. Fee set to 1000
Transaction FZROPJHNYGT3AVAMG4343DLIP7J3RI5Q22HN3Y5KAA4Q7MUK2GXA still pending as of round 9181769
Transaction FZROPJHNYGT3AVAMG4343DLIP7J3RI5Q22HN3Y5KAA4Q7MUK2GXA committed in round 9181771
```

Wait for confirmation and check if your transaction was executed.

```
algorand@d0d0d4a939b9:/opt/algorand/node$ goal account list
[offline]       Unnamed-0       HCQR36YHX3YP5IJX5XX776TDBQOQUQ3G4ZYMSLIPV2FL4GDA772HKSWIQU      94999000 microAlgos     *Default
[offline]       Unnamed-1       PENOKN5IT45O2C2AR6LWELMUDHCBDCR67SRJ72FIIN3ZMNTYF5ZZ6XSDEM      5000000 microAlgos
```

You should now find the new value into your account deposit.

[Algorand's Doc - Your first transaction](https://developer.algorand.org/docs/build-apps/hello_world/) 

------