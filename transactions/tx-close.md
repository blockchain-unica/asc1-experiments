## Close transaction

Assume that we have a testnet account with some ALGOs:

```
goal account balance -a PB3WPU4KGRK3K3DRZTGIARSVJSUKHL2LG5B4HDMEOBLDRBPKTOY734KFKU

100000 microAlgos
```

We construct a transaction which pays 0 microALGOS from that account to itself, and closes the account:
```
goal clerk send -a 0 -f PB3WPU4KGRK3K3DRZTGIARSVJSUKHL2LG5B4HDMEOBLDRBPKTOY734KFKU -t PB3WPU4KGRK3K3DRZTGIARSVJSUKHL2LG5B4HDMEOBLDRBPKTOY734KFKU -c WGJVDVVHS7VBNNPBW4CXR4IRVS3J6IHSU3TV57BE5QMHD74HNYPNS62NV4 -o tx-close-algo.tx
```

The transaction is constructed correctly:

```
goal clerk inspect tx-close-algo.tx

tx-close-algo.tx[0]
{
  "txn": {
    "amt": 100000,
    "fee": 1000,
    "fv": 9378414,
    "gen": "testnet-v1.0",
    "gh": "SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI=",
    "lv": 9379414,
    "note": "Qu1J0s9dn1s=",
    "rcv": "WGJVDVVHS7VBNNPBW4CXR4IRVS3J6IHSU3TV57BE5QMHD74HNYPNS62NV4",
    "snd": "WGJVDVVHS7VBNNPBW4CXR4IRVS3J6IHSU3TV57BE5QMHD74HNYPNS62NV4",
    "type": "pay"
  }
}

```

We sign the transaction:
```
goal clerk sign -i tx-close-algo.tx -o tx-close-algo.stx
```

Finally, we send the transaction to the testnet:

```
goal clerk rawsend -f tx-close-algo.stx

Raw transaction ID EG625HZLE4HCAGKWAHRE5LDH5IZIMUWACKBG4MROHAIJK5JEJAUQ issued
Transaction EG625HZLE4HCAGKWAHRE5LDH5IZIMUWACKBG4MROHAIJK5JEJAUQ still pending as of round 9379884
Transaction EG625HZLE4HCAGKWAHRE5LDH5IZIMUWACKBG4MROHAIJK5JEJAUQ committed in round 9379886
```

The transaction is successful: the account balance is zero.

```
goal account balance -a PB3WPU4KGRK3K3DRZTGIARSVJSUKHL2LG5B4HDMEOBLDRBPKTOY734KFKU

0 microAlgos
```

------
