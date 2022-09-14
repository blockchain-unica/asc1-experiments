## Oracle

We experiment with a smart signature that transfers all the funds of a contract account to A or B, depending on the choice of an orale O.
We three accounts with the following addresses:
```
# goal account list
[offline]	O	IPX7RJQPIHEEESTRRKF4QGNERGZE325NNFSYA5IX76VZRUTPQXZWNEMS7Q	0 microAlgos
[offline]	A	2GYIH5HXKDNXA3F7BBIAT5IX744E2WY75GIQRLEWURVRK3XXDQ6LMRAHXU	0 microAlgos	*Default
[offline]	B	3MTDHUNSO4RXC3ZPJ67C7TLEOFHFO2UNXHE34PN52VN2CSNYSEOXXHPFNY	0 microAlgos
```
The smart signature accepts all and only the following transactions:
- a close transaction to A, provided that the transaction contains the argument 0 and is signed by O;
- a close transaction to B, provided that the transaction contains the argument 1 and is signed by O.

We define the smart signature in PyTeal as follows:
```python
from pyteal import *

A = Addr("KUWCLDWCJGS7RKUKUWUMDXUUXG6W3I4Y4FFKU2ARXXK2O7TWJHSAKWXFMI")
B = Addr("L5YTCHB4OJXMYIW336MAYQ5V4MMFU4ACAMQZQX4PU5IBR4UNHGCJ2NJLUY")
O = Addr("JIDFTPWM2O65L5DWZ2FRMCZVPMGP44VYPHOV3G4XEX2JYO25G4P2ZHUT24")

arg0 = Bytes("0")
arg1 = Bytes("1")

def oracle(tmpl_a = A, tmpl_b = B, tmpl_o = O):

    typeOK   = And(Txn.type_enum() == TxnType.Payment, Txn.amount() == Int(0))
    versigO  = Ed25519Verify(Arg(0), Arg(1), tmpl_o)
    closeToA = And(Arg(0) == arg0, versigO, Txn.close_remainder_to() == tmpl_a)
    closeToB = And(Arg(0) == arg1, versigO, Txn.close_remainder_to() == tmpl_b)

    return And(typeOK, Or(closeToA, closeToB))

if __name__ == "__main__":
    print(compileTeal(oracle(), Mode.Signature))
```

We produce the TEAL contract by executing the Python code above:
```
# python oracle.py > oracle.teal
```

We compile the code using goal clerk compile and it will generate a contract address that can be funded using the dispenser on testnet.

```
# goal clerk compile oracle.teal
oracle.teal: NPNJ2B3QPG4MPHX5OVIYQGO4GXMPGIPHTBRSJZ4S3HXA5MERTPOOWT47ZE
```

Use a [[faucet]](https://bank.testnet.algorand.network/) to send some Algos to the contract account.

Now, we prepare a transaction T1 that transfers the funds from the contract to either A or B.
```
# goal clerk send --from-program oracle.teal -t KUWCLDWCJGS7RKUKUWUMDXUUXG6W3I4Y4FFKU2ARXXK2O7TWJHSAKWXFMI -o T1 --argb64 MA== -d data/
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
