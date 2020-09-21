## Pay transaction with sender equal to receiver

The goal of this experiment is to test the behaviour of a Pay transaction where the snd and rcv fields are equal.

Assume that we have a testnet account with some ALGOs:

```
goal account balance -a WGJVDVVHS7VBNNPBW4CXR4IRVS3J6IHSU3TV57BE5QMHD74HNYPNS62NV4

100100000 microAlgos
```

We construct a transaction which pays 100000 microALGOS from that account to itself:
```
goal clerk send -a 100000 -f WGJVDVVHS7VBNNPBW4CXR4IRVS3J6IHSU3TV57BE5QMHD74HNYPNS62NV4 -t WGJVDVVHS7VBNNPBW4CXR4IRVS3J6IHSU3TV57BE5QMHD74HNYPNS62NV4 -o tx-pay-snd_eq_rcv.tx
```

The transaction is constructed correctly:

```
goal clerk inspect tx-pay-snd_eq_rcv.tx

tx-pay-snd_eq_rcv.tx[0]
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
goal clerk sign -i tx-pay-snd_eq_rcv.tx -o tx-pay-snd_eq_rcv.stx
```

Finally, we send the transaction to the testnet:

```
goal clerk rawsend -f tx-pay-snd_eq_rcv.stx

Raw transaction ID YTW3XYD5OQBBRMXCCKSU5QYHFE5YQEFWHZKAR4YLMBMSODJ4NN6A issued
Transaction YTW3XYD5OQBBRMXCCKSU5QYHFE5YQEFWHZKAR4YLMBMSODJ4NN6A still pending as of round 9378473
Transaction YTW3XYD5OQBBRMXCCKSU5QYHFE5YQEFWHZKAR4YLMBMSODJ4NN6A committed in round 9378475
```

The transaction is successful: the fees are subtracted from the balance.

```
goal account balance -a WGJVDVVHS7VBNNPBW4CXR4IRVS3J6IHSU3TV57BE5QMHD74HNYPNS62NV4

100099000 microAlgos
```

------
