## Smart Contract

#### Testing teal programs - Oracle

We create a wallet and an account.

```
algorand@5856b1252bfb:/opt/algorand/node$ goal wallet new myWallet
Please choose a password for wallet 'myWallet':
Please confirm the password:
Creating wallet...
Created wallet 'myWallet'
Your new wallet has a backup phrase that can be used for recovery.
Keeping this backup phrase safe is extremely important.
Would you like to see it now? (Y/n): n
algorand@5856b1252bfb:/opt/algorand/node$ 
```

We also defined three accounts with the following addresses:

```
Address 1: 6ZHGHH5Z5CTPCF5WCESXMGRSVK7QJETR63M3NY5FJCUYDHO57VTCMJOBGY
Address 2: FP2UC5HN4TJ7AIK6OY5RAS52XA6GYCOQUK3HTR55UOACPZM6RCUKAP5VAM
Address 3: 7J6SHHBCIFAGBBQMJOXAKV2LCFU5CLXADWCMOJFDKM4MCDHSDYY3XV57QI
```

We used these three account into the next pyTeal program.

```
# adapted from:
# https://developer.algorand.org/articles/verify-signatures-and-signed-data-within-algorand-smart-contracts/

from pyteal import *

"""Versig-arg"""

# python -c "import os, base64; print(base64.b64encode('this is a test').decode('utf-8'))"

a = Addr("6ZHGHH5Z5CTPCF5WCESXMGRSVK7QJETR63M3NY5FJCUYDHO57VTCMJOBGY")
b = Addr("FP2UC5HN4TJ7AIK6OY5RAS52XA6GYCOQUK3HTR55UOACPZM6RCUKAP5VAM")
o = Addr("7J6SHHBCIFAGBBQMJOXAKV2LCFU5CLXADWCMOJFDKM4MCDHSDYY3XV57QI")
timeout = 3000

event0 = Bytes("0")
event1 = Bytes("1")

def oracle(tmpl_a = a,
           tmpl_b = b,
           tmpl_o = o,
           tmpl_timeout = timeout):
    type_cond = And(Txn.type_enum() == TxnType.Payment, Txn.amount() == Int(0))
    versig_cond = Ed25519Verify(Arg(0), Arg(1), tmpl_o)
    a_timeout_cond = And(Txn.first_valid() > Int(tmpl_timeout), Txn.close_remainder_to() == tmpl_a)
    a_wins_cond = And(Arg(0) == event0, versig_cond, Txn.close_remainder_to() == tmpl_a)
    b_wins_cond = And(Arg(0) == event1, versig_cond, Txn.close_remainder_to() == tmpl_b)
    return And(type_cond, Or(a_timeout_cond, a_wins_cond, b_wins_cond))

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
