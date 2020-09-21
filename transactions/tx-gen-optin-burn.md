## Assets

### Gen

Assume that we have a testnet account with some ALGOs:

```
goal account balance -a PB3WPU4KGRK3K3DRZTGIARSVJSUKHL2LG5B4HDMEOBLDRBPKTOY734KFKU

300000 microAlgos
```

We issue a transaction which generates 1000 units of a new asset:
```
goal asset create --creator PB3WPU4KGRK3K3DRZTGIARSVJSUKHL2LG5B4HDMEOBLDRBPKTOY734KFKU --total 1000

Issued transaction from account PB3WPU4KGRK3K3DRZTGIARSVJSUKHL2LG5B4HDMEOBLDRBPKTOY734KFKU, txid KD2SCZTDFN2RZOL5R66MKLOWXPQYK4M2LMEBLP6VXNL4HECKCT3A (fee 1000)
Transaction KD2SCZTDFN2RZOL5R66MKLOWXPQYK4M2LMEBLP6VXNL4HECKCT3A still pending as of round 9380933
Transaction KD2SCZTDFN2RZOL5R66MKLOWXPQYK4M2LMEBLP6VXNL4HECKCT3A committed in round 9380935
Created asset with asset index 12277079
```

Send 1 unit of the new asset to another address (which has not opted in):

```
goal asset send -a 1 --assetid 12277079 -f PB3WPU4KGRK3K3DRZTGIARSVJSUKHL2LG5B4HDMEOBLDRBPKTOY734KFKU -t WGJVDVVHS7VBNNPBW4CXR4IRVS3J6IHSU3TV57BE5QMHD74HNYPNS62NV4 -o tx-gen-asset.tx -s

goal clerk inspect tx-gen-asset.tx
tx-gen-asset.tx[0]
{
  "sig": "LjOjS06Px8avfbmSW5YmQZTANn6/RAeWzl9hxXavX3wkeuNhxeDnMXbJxxScXQpXNAoJCgaxRaMkHDPs3aG1Ag==",
  "txn": {
    "aamt": 1,
    "arcv": "WGJVDVVHS7VBNNPBW4CXR4IRVS3J6IHSU3TV57BE5QMHD74HNYPNS62NV4",
    "fee": 1000,
    "fv": 9381116,
    "gh": "SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI=",
    "lv": 9382116,
    "note": "eI6sdBGekW4=",
    "snd": "PB3WPU4KGRK3K3DRZTGIARSVJSUKHL2LG5B4HDMEOBLDRBPKTOY734KFKU",
    "type": "axfer",
    "xaid": 12277079
  }
}
```

As expected, the transaction is rejected:
```
goal clerk rawsend -f tx-gen-asset.tx

Warning: Couldn't broadcast tx with algod: HTTP 400 Bad Request: TransactionPool.Remember: transaction JBZAQMWBIBJFWWPNLNBCVTWM2EBTUAYXM2PLKKQG2Y2MXD4DXMVA: asset 12277079 missing from WGJVDVVHS7VBNNPBW4CXR4IRVS3J6IHSU3TV57BE5QMHD74HNYPNS62NV4
Encountered errors in sending 1 transactions:
  JBZAQMWBIBJFWWPNLNBCVTWM2EBTUAYXM2PLKKQG2Y2MXD4DXMVA: HTTP 400 Bad Request: TransactionPool.Remember: transaction JBZAQMWBIBJFWWPNLNBCVTWM2EBTUAYXM2PLKKQG2Y2MXD4DXMVA: asset 12277079 missing from WGJVDVVHS7VBNNPBW4CXR4IRVS3J6IHSU3TV57BE5QMHD74HNYPNS62NV4
Rejected transactions written to tx-gen-asset.tx.rej
```

### Opt-in

Send 0 unit of the new asset to to opt-in:

```
goal asset send -a 0 --assetid 12277079 -f WGJVDVVHS7VBNNPBW4CXR4IRVS3J6IHSU3TV57BE5QMHD74HNYPNS62NV4 -t WGJVDVVHS7VBNNPBW4CXR4IRVS3J6IHSU3TV57BE5QMHD74HNYPNS62NV4 -o tx-optin-asset.tx -s

goal clerk inspect tx-optin-asset.tx tx-optin-asset.tx[0]
{
  "sig": "eG5JXYrYoUOOzJnL3mFefKCrTwT9/uk66L98hNk83FkQnDbHRsz3YtuCP2O4r65TtXtASfZ1kNDjNGP+dK72Bg==",
  "txn": {
    "arcv": "WGJVDVVHS7VBNNPBW4CXR4IRVS3J6IHSU3TV57BE5QMHD74HNYPNS62NV4",
    "fee": 1000,
    "fv": 9382283,
    "gh": "SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI=",
    "lv": 9383283,
    "note": "oCFaKmQVR4s=",
    "snd": "WGJVDVVHS7VBNNPBW4CXR4IRVS3J6IHSU3TV57BE5QMHD74HNYPNS62NV4",
    "type": "axfer",
    "xaid": 12277079
  }
}

goal clerk rawsend -f tx-optin-asset.tx 

Raw transaction ID UQS6DAOGFX4PL6XS2ZSI6DI2K3CLXYHCYVHYQLUL2IJBC3BDZ5CQ issued
Transaction UQS6DAOGFX4PL6XS2ZSI6DI2K3CLXYHCYVHYQLUL2IJBC3BDZ5CQ still pending as of round 9382294
Transaction UQS6DAOGFX4PL6XS2ZSI6DI2K3CLXYHCYVHYQLUL2IJBC3BDZ5CQ committed in round 9382296
```

We try again to send 1 unit of the new asset to another address (which now has opted in):

```
goal asset send -a 1 --assetid 12277079 -f PB3WPU4KGRK3K3DRZTGIARSVJSUKHL2LG5B4HDMEOBLDRBPKTOY734KFKU -t WGJVDVVHS7VBNNPBW4CXR4IRVS3J6IHSU3TV57BE5QMHD74HNYPNS62NV4 -o tx-pay-asset.tx -s

goal clerk rawsend -f tx-pay-asset.tx

Raw transaction ID BKBRJBYQPEJAA4FWGIRFJMFLRVFR64WGCU6U6QDNTQNJZLNLGCTQ issued

Transaction BKBRJBYQPEJAA4FWGIRFJMFLRVFR64WGCU6U6QDNTQNJZLNLGCTQ still pending as of round 9382315
Transaction BKBRJBYQPEJAA4FWGIRFJMFLRVFR64WGCU6U6QDNTQNJZLNLGCTQ committed in round 9382317
```

The transaction is successful: the account balance is zero.

```
goal account list

[offline] Unnamed-2 PB3WPU4KGRK3K3DRZTGIARSVJSUKHL2LG5B4HDMEOBLDRBPKTOY734KFKU
          298000 microAlgos [created asset IDs: 12277079 (1000 )]
          999 units (creator PB3WPU4KGRK3K3DRZTGIARSVJSUKHL2LG5B4HDMEOBLDRBPKTOY734KFKU, ID 12277079)
[offline] Unnamed-1 WGJVDVVHS7VBNNPBW4CXR4IRVS3J6IHSU3TV57BE5QMHD74HNYPNS62NV4
          99794000 microAlgos
          1 units (creator PB3WPU4KGRK3K3DRZTGIARSVJSUKHL2LG5B4HDMEOBLDRBPKTOY734KFKU, ID 12277079)
```


### Burn (creator without all token units)

Destroying the asset fails, because the the transaction issuer is not the manager:
```
goal asset destroy --creator WGJVDVVHS7VBNNPBW4CXR4IRVS3J6IHSU3TV57BE5QMHD74HNYPNS62NV4 --assetid 12277079

Couldn't broadcast tx with algod: HTTP 400 Bad Request: TransactionPool.Remember: transaction ZM4Y54PIJ46PZ66CVPX37XUGV6XRETR54NHICH3GCQZ6XMTNGPWA: this transaction should be issued by the manager. It is issued by WGJVDVVHS7VBNNPBW4CXR4IRVS3J6IHSU3TV57BE5QMHD74HNYPNS62NV4, manager key PB3WPU4KGRK3K3DRZTGIARSVJSUKHL2LG5B4HDMEOBLDRBPKTOY734KFKU
```

Destroying the asset fails, because the manager does not have all the units:

```
goal asset destroy --creator PB3WPU4KGRK3K3DRZTGIARSVJSUKHL2LG5B4HDMEOBLDRBPKTOY734KFKU --assetid 12277079

Couldn't broadcast tx with algod: HTTP 400 Bad Request: TransactionPool.Remember: transaction HKEF2IFDNPU4F3IA6FJP4FJX5ZZ6TVHA2M3HAH5OJB2JKA4COETQ: cannot destroy asset: creator is holding only 999/1000
```

### Burn (creator is manager)

We tranfer all the units to the manager account, and then retry the destroy transaction:

```
goal asset send -a 1 --assetid 12277079 -f WGJVDVVHS7VBNNPBW4CXR4IRVS3J6IHSU3TV57BE5QMHD74HNYPNS62NV4 -t PB3WPU4KGRK3K3DRZTGIARSVJSUKHL2LG5B4HDMEOBLDRBPKTOY734KFKU -o tx-pay-asset2.tx -s

goal clerk rawsend -f tx-pay-asset2.tx

goal asset destroy --creator PB3WPU4KGRK3K3DRZTGIARSVJSUKHL2LG5B4HDMEOBLDRBPKTOY734KFKU --assetid 12277079

Issued transaction from account PB3WPU4KGRK3K3DRZTGIARSVJSUKHL2LG5B4HDMEOBLDRBPKTOY734KFKU, txid 3C2UH2VHYXYOCLG5XAYHJVUJ27SMJUF2ZHQ5TR5WW7FBQLKYJNRQ (fee 1000)
Transaction 3C2UH2VHYXYOCLG5XAYHJVUJ27SMJUF2ZHQ5TR5WW7FBQLKYJNRQ still pending as of round 9382666
Transaction 3C2UH2VHYXYOCLG5XAYHJVUJ27SMJUF2ZHQ5TR5WW7FBQLKYJNRQ committed in round 9382668
```

Now the destroy is successful:
```
goal account list

[offline] Unnamed-2 PB3WPU4KGRK3K3DRZTGIARSVJSUKHL2LG5B4HDMEOBLDRBPKTOY734KFKU
	  296000 microAlgos
[offline] Unnamed-1 WGJVDVVHS7VBNNPBW4CXR4IRVS3J6IHSU3TV57BE5QMHD74HNYPNS62NV4
	  99793000 microAlgos
	  0 base units (no decimal info)  (creator , ID 12277079)
```

This seems an implementation error, because the account WGJ... still records the presence of the asset.
To confirm the error, we try to opt-in again for the same account:

```
goal asset send -a 0 --assetid 12277079 -f WGJVDVVHS7VBNNPBW4CXR4IRVS3J6IHSU3TV57BE5QMHD74HNYPNS62NV4 -t WGJVDVVHS7VBNNPBW4CXR4IRVS3J6IHSU3TV57BE5QMHD74HNYPNS62NV4 -o tx-optin-asset2.tx -s

goal clerk rawsend -f tx-optin-asset2.tx

Raw transaction ID 5NJ3IIUVPIUD5ZWJLYJEP5RQXZC7MV234I47EQENS4SXW457MRTQ issued
Transaction 5NJ3IIUVPIUD5ZWJLYJEP5RQXZC7MV234I47EQENS4SXW457MRTQ still pending as of round 9382949
Transaction 5NJ3IIUVPIUD5ZWJLYJEP5RQXZC7MV234I47EQENS4SXW457MRTQ committed in round 9382951
```

The opt-in transaction succeeds, although the asset has been destroyed.

We try to opt-in for the destroyed asset from another account:

```
goal asset send -a 0 --assetid 12277079 -f AYQJVSEBPRM26SOLWRFFOULELKONQKVAKPRDBI6DQRRJTESLUZDDFCZS3A -t AYQJVSEBPRM26SOLWRFFOULELKONQKVAKPRDBI6DQRRJTESLUZDDFCZS3A -o tx-optin-asset3.tx -s

goal clerk rawsend -f tx-optin-asset3.tx

Warning: Couldn't broadcast tx with algod: HTTP 400 Bad Request: TransactionPool.Remember: transaction YORE2SDEKRDCIUELMZBRB3DW65POOTDLCIHCUU2YSHVFUAG7FB4Q: asset 12277079 does not exist or has been deleted

Encountered errors in sending 1 transactions:
  YORE2SDEKRDCIUELMZBRB3DW65POOTDLCIHCUU2YSHVFUAG7FB4Q: HTTP 400 Bad Request: TransactionPool.Remember: transaction YORE2SDEKRDCIUELMZBRB3DW65POOTDLCIHCUU2YSHVFUAG7FB4Q: asset 12277079 does not exist or has been deleted
```


### Burn (creator is not manager)

We create another asset, and configure its asset manager to another address:
```
goal asset create --creator PB3WPU4KGRK3K3DRZTGIARSVJSUKHL2LG5B4HDMEOBLDRBPKTOY734KFKU --total 1000

Issued transaction from account PB3WPU4KGRK3K3DRZTGIARSVJSUKHL2LG5B4HDMEOBLDRBPKTOY734KFKU, txid IK4IWIVOIQ2YSE4J3AIOG5W73JFEGSKDNBLK6YMF4VX4BV5MOMRA (fee 1000)
Transaction IK4IWIVOIQ2YSE4J3AIOG5W73JFEGSKDNBLK6YMF4VX4BV5MOMRA still pending as of round 9383578
Transaction IK4IWIVOIQ2YSE4J3AIOG5W73JFEGSKDNBLK6YMF4VX4BV5MOMRA committed in round 9383580
Created asset with asset index 12277140

goal asset config --assetid 12277140 --manager PB3WPU4KGRK3K3DRZTGIARSVJSUKHL2LG5B4HDMEOBLDRBPKTOY734KFKU --new-manager AYQJVSEBPRM26SOLWRFFOULELKONQKVAKPRDBI6DQRRJTESLUZDDFCZS3A

Issued transaction from account PB3WPU4KGRK3K3DRZTGIARSVJSUKHL2LG5B4HDMEOBLDRBPKTOY734KFKU, txid 7MDYY5MQAK6S5E4YMY3TZVBV3ZC6HLDBK2U5BHPYZ7DHASIVIZCQ (fee 1000)
Transaction 7MDYY5MQAK6S5E4YMY3TZVBV3ZC6HLDBK2U5BHPYZ7DHASIVIZCQ still pending as of round 9389433
Transaction 7MDYY5MQAK6S5E4YMY3TZVBV3ZC6HLDBK2U5BHPYZ7DHASIVIZCQ committed in round 9389435
```

We try to burn the asset, but the transaction fails because it is not signed by the manager:
```
goal asset destroy --creator PB3WPU4KGRK3K3DRZTGIARSVJSUKHL2LG5B4HDMEOBLDRBPKTOY734KFKU --assetid 12277140

Couldn't broadcast tx with algod: HTTP 400 Bad Request: TransactionPool.Remember: transaction HNF4E2HIJCRLXU57JB2FGPYYC2HAGEZGODC4TYO4XP3RC2BPJ2QQ: this transaction should be issued by the manager. It is issued by PB3WPU4KGRK3K3DRZTGIARSVJSUKHL2LG5B4HDMEOBLDRBPKTOY734KFKU, manager key AYQJVSEBPRM26SOLWRFFOULELKONQKVAKPRDBI6DQRRJTESLUZDDFCZS3A
```

The burn succeeds if it is signed by the manager:
```
goal asset destroy --manager AYQJVSEBPRM26SOLWRFFOULELKONQKVAKPRDBI6DQRRJTESLUZDDFCZS3A --assetid 12277140

Issued transaction from account AYQJVSEBPRM26SOLWRFFOULELKONQKVAKPRDBI6DQRRJTESLUZDDFCZS3A, txid CCLS7T7NKIVJHU5XTARWL5ZGAC7Y2MJHL5Y5IWC3NQTKJ52TWR4A (fee 1000)
Transaction CCLS7T7NKIVJHU5XTARWL5ZGAC7Y2MJHL5Y5IWC3NQTKJ52TWR4A still pending as of round 9389538
Transaction CCLS7T7NKIVJHU5XTARWL5ZGAC7Y2MJHL5Y5IWC3NQTKJ52TWR4A committed in round 9389540
```

------
