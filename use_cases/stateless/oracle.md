## Oracle

We experiment with a smart signature that transfers all the funds of a contract account to A or B, depending on the choice of an orale O.
We three accounts with the following addresses:
```
# goal account list
```
The smart signature accepts all and only the following transactions:
- a close transaction to A, provided that the transaction contains the argument 0 and is signed by O;
- a close transaction to B, provided that the transaction contains the argument 1 and is signed by O.

We define the smart signature in PyTeal as follows:
```
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

We compile the code using goal clerk compile and it will generate a contract address that can be funded using the dispenser on testnet.

```
algorand@5856b1252bfb: goal clerk compile oracle.teal -d data/
oracle.teal: HYQIJ3DYAH35IVVCELQSWZK7LB2B5UZJ2GEXX75JNNU6GFOCVBVOOALKM4
```

We prepare the transaction to be sent.

```
algorand@5856b1252bfb:/opt/algorand/node$ goal clerk send --from-program verify_contract.teal -t AP4UC5HN4TJ7AIFJ8DDHLED92F8JE34KUK3HTR55UOACPWGF0DKL0E2JSQ -o tosign.tx --argb64 MA== -d data/
algorand@5856b1252bfb:/opt/algorand/node$ goal clerk tealsign --sign-txid --keyfile keyfile.sk --lsig-txn tosign.tx --set-lsig-arg-idx 0
```

Where "MA==" represents the encode in base64 of the value zero.


The file keyfile.sk has been generated using the following commands.

```
algorand@5856b1252bfb:/opt/algorand/node$ goal account export 7J6SHHBCIFAGBBQMJOXAKV2LCFU5CLXADWCMOJFDKM4MCDHSDYY3XV57QI -d data/ -w myWallet
algorand@5856b1252bfb:/opt/algorand/node$ algokey import -m "mnemonic sentence"  --keyfile keyfile.sk
algorand@5856b1252bfb:/opt/algorand/node$ goal clerk rawsend -f tosign.tx -d ~/node/data  || true
```
