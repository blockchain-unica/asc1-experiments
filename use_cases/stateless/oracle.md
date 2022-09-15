## Oracle

We experiment with a smart signature that transfers all the funds of a contract account to A or B, depending on the choice of an orale O.
We three accounts with the following addresses:
```
# goal account list
[offline]	O	IPX7RJQPIHEEESTRRKF4QGNERGZE325NNFSYA5IX76VZRUTPQXZWNEMS7Q	0 microAlgos
[offline]	A	2GYIH5HXKDNXA3F7BBIAT5IX744E2WY75GIQRLEWURVRK3XXDQ6LMRAHXU	10000000 microAlgos	*Default
[offline]	B	3MTDHUNSO4RXC3ZPJ67C7TLEOFHFO2UNXHE34PN52VN2CSNYSEOXXHPFNY	10000000 microAlgos
```
The smart signature accepts all and only the following transactions:
- a close transaction to A, provided that the transaction contains the argument 0 and is signed by O;
- a close transaction to B, provided that the transaction contains the argument 1 and is signed by O.

We define the smart signature in PyTeal as follows:
```python
from pyteal import *

A = Addr("2GYIH5HXKDNXA3F7BBIAT5IX744E2WY75GIQRLEWURVRK3XXDQ6LMRAHXU")
B = Addr("3MTDHUNSO4RXC3ZPJ67C7TLEOFHFO2UNXHE34PN52VN2CSNYSEOXXHPFNY")
O = Addr("IPX7RJQPIHEEESTRRKF4QGNERGZE325NNFSYA5IX76VZRUTPQXZWNEMS7Q")

arg0 = Bytes("0")
arg1 = Bytes("1")

def oracle(a = A, b = B, o = O):

    typeOK   = And(Txn.type_enum() == TxnType.Payment, Txn.amount() == Int(0))
    versigO  = Ed25519Verify(Arg(0), Arg(1), o)
    closeToA = And(Arg(0) == arg0, versigO, Txn.close_remainder_to() == a)
    closeToB = And(Arg(0) == arg1, versigO, Txn.close_remainder_to() == b)

    return And(typeOK, Or(closeToA, closeToB))

if __name__ == "__main__":
    print(compileTeal(oracle(), Mode.Signature))
```

We produce the TEAL contract by executing the Python code above:
```
# python oracle.py > oracle.teal
```

We translate the oracle from PyTeal to TEAL. This generates a contract address:
```
# goal clerk compile oracle.teal
oracle.teal: NPNJ2B3QPG4MPHX5OVIYQGO4GXMPGIPHTBRSJZ4S3HXA5MERTPOOWT47ZE
```

Now, use a [faucet](https://bank.testnet.algorand.network/) to send some Algos to the contract account.
After that, we check the balance of the contract account:
```
# goal account balance -a NPNJ2B3QPG4MPHX5OVIYQGO4GXMPGIPHTBRSJZ4S3HXA5MERTPOOWT47ZE
10000000 microAlgos
```

We prepare a transaction T1 that transfers all the funds from the contract account to either A.
To do this, the contract requires that the argument at index 0 contains the base64 encoding of 0.
We use the first command to obtain such an encoding:
```
# echo -n 0 | base64
MA==
```

We prepare a transaction T1 that transfers all the funds from the contract account to either A.
```
# goal clerk send -F oracle.teal -t A -o T1 -a 0 --argb64 MA==
```

```
# goal clerk inspect T1
T1[0]
{
  "lsig": {
    "arg": [
      "MA=="
    ],
    "l": "#pragma version 2\nintcblock 1 0\nbytecblock 0x30 0x43eff8a60f41c8424a718a8bc819a489b24debad6965807517ffab98d26f85f3 0xd1b083f4f750db706cbf085009f517ff384d5b1fe99108ac96a46b156ef71c3c 0x31 0xdb2633d1b27723716f2f4fbe2fcd64714e576a8db9c9be3dbdd55ba149b8911d\ntxn TypeEnum\nintc_0 // 1\n==\ntxn Amount\nintc_1 // 0\n==\n&&\narg_0\nbytec_0 // \"0\"\n==\narg_0\narg_1\nbytec_1 // addr IPX7RJQPIHEEESTRRKF4QGNERGZE325NNFSYA5IX76VZRUTPQXZWNEMS7Q\ned25519verify\n&&\ntxn CloseRemainderTo\nbytec_2 // addr 2GYIH5HXKDNXA3F7BBIAT5IX744E2WY75GIQRLEWURVRK3XXDQ6LMRAHXU\n==\n&&\narg_0\nbytec_3 // \"1\"\n==\narg_0\narg_1\nbytec_1 // addr IPX7RJQPIHEEESTRRKF4QGNERGZE325NNFSYA5IX76VZRUTPQXZWNEMS7Q\ned25519verify\n&&\ntxn CloseRemainderTo\nbytec 4 // addr 3MTDHUNSO4RXC3ZPJ67C7TLEOFHFO2UNXHE34PN52VN2CSNYSEOXXHPFNY\n==\n&&\n||\n&&\nreturn\n"
  },
  "txn": {
    "fee": 1000,
    "fv": 24104434,
    "gen": "testnet-v1.0",
    "gh": "SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI=",
    "lv": 24105434,
    "note": "KoabzgHJRfo=",
    "rcv": "2GYIH5HXKDNXA3F7BBIAT5IX744E2WY75GIQRLEWURVRK3XXDQ6LMRAHXU",
    "snd": "NPNJ2B3QPG4MPHX5OVIYQGO4GXMPGIPHTBRSJZ4S3HXA5MERTPOOWT47ZE",
    "type": "pay"
  }
}
```

```
# goal clerk tealsign --sign-txid --keyfile keyfile.sk --lsig-txn T1 --set-lsig-arg-idx 0
```

Where "MA==" represents the encode in base64 of the value zero.

The file keyfile.sk has been generated using the following commands.

```
algorand@5856b1252bfb:/opt/algorand/node$ goal account export 7J6SHHBCIFAGBBQMJOXAKV2LCFU5CLXADWCMOJFDKM4MCDHSDYY3XV57QI -d data/ -w myWallet
algorand@5856b1252bfb:/opt/algorand/node$ algokey import -m "mnemonic sentence"  --keyfile keyfile.sk
```

```
# goal clerk rawsend -f tosign.tx -d ~/node/data  || true
```
