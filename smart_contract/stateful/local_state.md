## Local state

### Put a value into local state - account not opted in

To do these experiments [this code](./example_stateful_contract.md) has been used.

We try to put a value into local state without opt in the account to the contract, even if the account is the creator of the contract. 

Firstly, we create the contract:

```
goal app create --creator BWPHWE6Z7WGRYUODABVBAZLHPDCDXEF5BYFYPWJQL2YNCF3RJATXQFB3UM --approval-prog approval_program.teal --clear-prog ./clear_state_program.teal --global-byteslices 1 --global-ints 1 --local-byteslices 1 --local-ints 1

Attempting to create app (approval size 288, hash Q73AJHTDEYBG23P6VZ2RA2DQUDGPRB37D3BSIBVBFMECINK4HFSA; clear size 6, hash ZYI7YTWEXF6FGMRDOJNAGIID5M7OKO554TJOVU2RCA7Z2QWQEBTA)
Issued transaction from account BWPHWE6Z7WGRYUODABVBAZLHPDCDXEF5BYFYPWJQL2YNCF3RJATXQFB3UM, txid YUK3KU5C5WGBO7QELJ3LR27ZJLDZEXUOTBSMNEKWYOVN62KUBNXQ (fee 1000)
Transaction YUK3KU5C5WGBO7QELJ3LR27ZJLDZEXUOTBSMNEKWYOVN62KUBNXQ still pending as of round 10459678
Transaction YUK3KU5C5WGBO7QELJ3LR27ZJLDZEXUOTBSMNEKWYOVN62KUBNXQ committed in round 10459680
Created app with app index 13128112
```

Then, we try to put a value into local state without opt in the account to the contract:

```
goal app call --app-id 13128112 --from BWPHWE6Z7WGRYUODABVBAZLHPDCDXEF5BYFYPWJQL2YNCF3RJATXQFB3UM  --app-arg "str:put_value_to_local" --app-arg "int:0"

Couldn't broadcast tx with algod: HTTP 400 Bad Request: TransactionPool.Remember: transaction HE6EUCG7EC7RTNJZAHZ7JV6VYKFAT3LUI6B7GWCYAUYXWYNH4TMA: failed to fetch app local state for acct BWPHWE6Z7WGRYUODABVBAZLHPDCDXEF5BYFYPWJQL2YNCF3RJATXQFB3UM: addr BWPHWE6Z7WGRYUODABVBAZLHPDCDXEF5BYFYPWJQL2YNCF3RJATXQFB3UM not opted in to app 13128112, cannot fetch state
```

As expected it doesn't work because the account it is not opted in to the contract.

We try to do the same operation but first we opt in to the contract:

```
goal app optin --app-id 13128112 --from BWPHWE6Z7WGRYUODABVBAZLHPDCDXEF5BYFYPWJQL2YNCF3RJATXQFB3UM

Issued transaction from account BWPHWE6Z7WGRYUODABVBAZLHPDCDXEF5BYFYPWJQL2YNCF3RJATXQFB3UM, txid QC5JEGYCJMNOY7U26EBJ7CPRJNESAG52EHKDBUA7ABYUCBL3UIUQ (fee 1000)
Transaction QC5JEGYCJMNOY7U26EBJ7CPRJNESAG52EHKDBUA7ABYUCBL3UIUQ still pending as of round 10459702
Transaction QC5JEGYCJMNOY7U26EBJ7CPRJNESAG52EHKDBUA7ABYUCBL3UIUQ committed in round 10459704
```

And then:

```
goal app call --app-id 13128112 --from BWPHWE6Z7WGRYUODABVBAZLHPDCDXEF5BYFYPWJQL2YNCF3RJATXQFB3UM --app-arg "str:put_value_to_local" --app-arg "int:0"

Issued transaction from account BWPHWE6Z7WGRYUODABVBAZLHPDCDXEF5BYFYPWJQL2YNCF3RJATXQFB3UM, txid 7MFARC53HK7USLMMGW2LCLR3DXUXZEQQ4HN6ZHG3YT5GOPDCTAYA (fee 1000)
Transaction 7MFARC53HK7USLMMGW2LCLR3DXUXZEQQ4HN6ZHG3YT5GOPDCTAYA still pending as of round 10459708
Transaction 7MFARC53HK7USLMMGW2LCLR3DXUXZEQQ4HN6ZHG3YT5GOPDCTAYA committed in round 10459710
```

As expected it works.
We can verify the local state using:

```
goal app read --local --from BWPHWE6Z7WGRYUODABVBAZLHPDCDXEF5BYFYPWJQL2YNCF3RJATXQFB3UM --app-id 13128112

{
    "local": {
        "tt": 2,
        "ui": 1
    }
}
```

### Put a value in an additional account local state - additional account not opted in the contract


We have the following addresses:

```
BWPHWE6Z7WGRYUODABVBAZLHPDCDXEF5BYFYPWJQL2YNCF3RJATXQFB3UM	99986000 microAlgos [created app IDs: 13128112] [opted in app IDs: 13128112]
VU5CRNAPNZ62UIRP6P7DZ6PZUBZHILUHGR2WTPM323KHGZFWZ5UAVMOREY	99491000 microAlgos
```
We try to put a value in an additional account local state (VU5C..), even if it is not opted in the contract:

```
goal app call --app-id 13128112 --from BWPHWE6Z7WGRYUODABVBAZLHPDCDXEF5BYFYPWJQL2YNCF3RJATXQFB3UM --app-account VU5CRNAPNZ62UIRP6P7DZ6PZUBZHILUHGR2WTPM323KHGZFWZ5UAVMOREY --app-arg "str:put_value_to_local" --app-arg "int:1"
		
Couldn't broadcast tx with algod: HTTP 400 Bad Request: TransactionPool.Remember: transaction 66NIUJZUN6XOYHNCCSM6LQT5BQSABS5YCRWQQJKHPQNZ345HMLYA: failed to fetch app local state for acct VU5CRNAPNZ62UIRP6P7DZ6PZUBZHILUHGR2WTPM323KHGZFWZ5UAVMOREY: addr VU5CRNAPNZ62UIRP6P7DZ6PZUBZHILUHGR2WTPM323KHGZFWZ5UAVMOREY not opted in to app 13128112, cannot fetch state
```

This is an expected behaviour. The transaction has been rejected because the additional account it is not opted in the contract.

We try to do the same operation but first we opt in the additional account to the contract:

```
goal app optin --app-id 13128112 --from VU5CRNAPNZ62UIRP6P7DZ6PZUBZHILUHGR2WTPM323KHGZFWZ5UAVMOREY
		
Issued transaction from account VU5CRNAPNZ62UIRP6P7DZ6PZUBZHILUHGR2WTPM323KHGZFWZ5UAVMOREY, txid ENEJFYP5EWD2MYY23ZPKPXVM2PTRADI3DMHYPUT5E4UKEWJP2OAA (fee 1000)
Transaction ENEJFYP5EWD2MYY23ZPKPXVM2PTRADI3DMHYPUT5E4UKEWJP2OAA still pending as of round 10459738
Transaction ENEJFYP5EWD2MYY23ZPKPXVM2PTRADI3DMHYPUT5E4UKEWJP2OAA committed in round 10459740


goal app call --app-id 13128112 --from BWPHWE6Z7WGRYUODABVBAZLHPDCDXEF5BYFYPWJQL2YNCF3RJATXQFB3UM --app-account VU5CRNAPNZ62UIRP6P7DZ6PZUBZHILUHGR2WTPM323KHGZFWZ5UAVMOREY --app-arg "str:put_value_to_local" --app-arg "int:1"
		
Issued transaction from account BWPHWE6Z7WGRYUODABVBAZLHPDCDXEF5BYFYPWJQL2YNCF3RJATXQFB3UM, txid GAKAV7PESNYHWBYMSXRMBWYLMZQ5JTCWZEOVWP4FRK25C2BCM75Q (fee 1000)
Transaction GAKAV7PESNYHWBYMSXRMBWYLMZQ5JTCWZEOVWP4FRK25C2BCM75Q still pending as of round 10459747
Transaction GAKAV7PESNYHWBYMSXRMBWYLMZQ5JTCWZEOVWP4FRK25C2BCM75Q committed in round 10459749
```

As expected it works. We can verify the local state of the additional account using:

```
goal app read --local --from VU5CRNAPNZ62UIRP6P7DZ6PZUBZHILUHGR2WTPM323KHGZFWZ5UAVMOREY --app-id 13128112
{
    "local": {
        "tt": 2,
        "ui": 1
    }
}
```

### Get a value from additional account local state

We have the following accounts:

```
goal account list

BWPHWE6Z7WGRYUODABVBAZLHPDCDXEF5BYFYPWJQL2YNCF3RJATXQFB3UM 99991000 microAlgos [created app IDs: 13128112] [opted in app IDs: 13128112]
VU5CRNAPNZ62UIRP6P7DZ6PZUBZHILUHGR2WTPM323KHGZFWZ5UAVMOREY 99492000 microAlgos [opted in app IDs: 13128112]
DQKKD4CKN7UNSUNDNFK7VJMPWUSRPN2DZJALNFXTG5KLQESYAXT64M5M4M 99992000 microAlgos
```

The account VU5C.. that is opted in the contract 13128112 has the following local state associated to the mentioned contract:

```
goal app read --local --app-id 13128112 --from VU5CRNAPNZ62UIRP6P7DZ6PZUBZHILUHGR2WTPM323KHGZFWZ5UAVMOREY

{
  "local": {
    "tt": 2,
    "ui": 1
  }
}
```

We try to read a value from BWPH.. to additional account local state (VU5C..) associated to the app 13128112:

```
goal app call --app-id 13128112 --from BWPHWE6Z7WGRYUODABVBAZLHPDCDXEF5BYFYPWJQL2YNCF3RJATXQFB3UM --app-account VU5CRNAPNZ62UIRP6P7DZ6PZUBZHILUHGR2WTPM323KHGZFWZ5UAVMOREY --app-arg "str:get_value_from_local" --app-arg "int:1"
		
Issued transaction from account BWPHWE6Z7WGRYUODABVBAZLHPDCDXEF5BYFYPWJQL2YNCF3RJATXQFB3UM, txid SS2PU4VT5GPKVOOXOIJRGTI5G4HS7VNB3DXRIJ5F7PVN53OBYIVA (fee 1000)
Transaction SS2PU4VT5GPKVOOXOIJRGTI5G4HS7VNB3DXRIJ5F7PVN53OBYIVA still pending as of round 10459787
Transaction SS2PU4VT5GPKVOOXOIJRGTI5G4HS7VNB3DXRIJ5F7PVN53OBYIVA committed in round 10459789
```

The transaction has been accepted by the contract logic, so we can access to the additional account local state.

We do the same with another account (DQKK..) that's not opted in the app:

```
goal app call --app-id 13128112 --from BWPHWE6Z7WGRYUODABVBAZLHPDCDXEF5BYFYPWJQL2YNCF3RJATXQFB3UM --app-account DQKKD4CKN7UNSUNDNFK7VJMPWUSRPN2DZJALNFXTG5KLQESYAXT64M5M4M --app-arg "str:get_value_from_local" --app-arg "int:1"
		
Couldn't broadcast tx with algod: HTTP 400 Bad Request: TransactionPool.Remember: transaction 6N3ITSHQ3WNTYWO4T77GGVST5RHJINL4OZDFWVMC4IHOQZT4BNUQ: failed to fetch app local state for acct DQKKD4CKN7UNSUNDNFK7VJMPWUSRPN2DZJALNFXTG5KLQESYAXT64M5M4M: addr DQKKD4CKN7UNSUNDNFK7VJMPWUSRPN2DZJALNFXTG5KLQESYAXT64M5M4M not opted in to app 13128112, cannot fetch state
```

As expected, the transaction has been rejected because DQKK.. is not opted in the contract.

We do another test after opting in DQKK.. in the app:

```
goal app optin --app-id 13128112 --from DQKKD4CKN7UNSUNDNFK7VJMPWUSRPN2DZJALNFXTG5KLQESYAXT64M5M4M

Issued transaction from account DQKKD4CKN7UNSUNDNFK7VJMPWUSRPN2DZJALNFXTG5KLQESYAXT64M5M4M, txid OFSJGG3OTATCIR7DWTUIZ5QLF475SGXI6YLYTJBRLI3DCI367GLA (fee 1000)
Transaction OFSJGG3OTATCIR7DWTUIZ5QLF475SGXI6YLYTJBRLI3DCI367GLA still pending as of round 10459809
Transaction OFSJGG3OTATCIR7DWTUIZ5QLF475SGXI6YLYTJBRLI3DCI367GLA committed in round 10459811
        
goal app call --app-id 13128112 --from BWPHWE6Z7WGRYUODABVBAZLHPDCDXEF5BYFYPWJQL2YNCF3RJATXQFB3UM --app-account DQKKD4CKN7UNSUNDNFK7VJMPWUSRPN2DZJALNFXTG5KLQESYAXT64M5M4M --app-arg "str:get_value_from_local" --app-arg "int:1"

Couldn't broadcast tx with algod: HTTP 400 Bad Request: TransactionPool.Remember: transaction 4IZY4YCDXZCOGCJNGI2LKFT2G3P7E4JH3RHYI4DHJBQ4C6VZ5U3Q: transaction rejected by ApprovalProgram
```

As expected the transaction has been rejected by the contract logic because DQKK.. doesn't have anything stored in local state.


### Get a value from additional account local state - caller not opted in

We have the following accounts:

```
goal account list

VU5CRNAPNZ62UIRP6P7DZ6PZUBZHILUHGR2WTPM323KHGZFWZ5UAVMOREY 99492000 microAlgos [opted in app IDs: 13128112]
KK3SSF7NAKSUXFZ27QUTNBGL6525RPPO4HBL3FJYFSPJ45UMQGURECCGUU 99995000 microAlgos
```

The account VU5C.. that is opted in the contract 13128112 has the following local state associated to the mentioned contract:

```
goal app read --local --app-id 13128112 --from VU5CRNAPNZ62UIRP6P7DZ6PZUBZHILUHGR2WTPM323KHGZFWZ5UAVMOREY

{
  "local": {
    "tt": 2,
    "ui": 1
  }
}
```

We try to read a value from KK3S.. to additional account local state (VU5C..) associated to the app 13128112:

```
goal app call --app-id 13128112 --from KK3SSF7NAKSUXFZ27QUTNBGL6525RPPO4HBL3FJYFSPJ45UMQGURECCGUU --app-account VU5CRNAPNZ62UIRP6P7DZ6PZUBZHILUHGR2WTPM323KHGZFWZ5UAVMOREY --app-arg "str:get_value_from_local" --app-arg "int:1"
		
Issued transaction from account KK3SSF7NAKSUXFZ27QUTNBGL6525RPPO4HBL3FJYFSPJ45UMQGURECCGUU, txid YUVUNFGCRQSCRHNC54W2QU7SJ3QUPOLMKLJZHICVOHAPPF4QGELQ (fee 1000)
Transaction YUVUNFGCRQSCRHNC54W2QU7SJ3QUPOLMKLJZHICVOHAPPF4QGELQ still pending as of round 10500251
Transaction YUVUNFGCRQSCRHNC54W2QU7SJ3QUPOLMKLJZHICVOHAPPF4QGELQ committed in round 10500253
```

The transaction has been accepted by the contract logic, so we can access to the additional account local state. It works even if KK3S.. is not opted in the contract because the TransactionCall does not write to the local state.


### Get a value stored into an account local state associated to another app


We have the following accounts:

```
goal account list

BWPHWE6Z7WGRYUODABVBAZLHPDCDXEF5BYFYPWJQL2YNCF3RJATXQFB3UM 99991000 microAlgos [created app IDs: 13128112] [opted in app IDs: 13128112]
46JO4OCM3RNMD3S5SCSYLQX7LAGSR3QOIKFPZXOUIRR66NUPN62SULNUEM 99996000 microAlgos
KK3SSF7NAKSUXFZ27QUTNBGL6525RPPO4HBL3FJYFSPJ45UMQGURECCGUU 99995000 microAlgos
```

Suppose to create another contract (using the code mentioned above) with the account 46JO.., opt in the account to the new contract and store a value in the account local state:

```
goal app create --creator 46JO4OCM3RNMD3S5SCSYLQX7LAGSR3QOIKFPZXOUIRR66NUPN62SULNUEM --approval-prog approval_program.teal --clear-prog ./clear_state_program.teal --global-byteslices 1 --global-ints 1 --local-byteslices 1 --local-ints 1 -d /opt/algorand/node/data

Attempting to create app (approval size 288, hash Q73AJHTDEYBG23P6VZ2RA2DQUDGPRB37D3BSIBVBFMECINK4HFSA; clear size 6, hash ZYI7YTWEXF6FGMRDOJNAGIID5M7OKO554TJOVU2RCA7Z2QWQEBTA)
Issued transaction from account 46JO4OCM3RNMD3S5SCSYLQX7LAGSR3QOIKFPZXOUIRR66NUPN62SULNUEM, txid 3I3F4T27ADM5K6QOYSCFE35BFAIPCRVYZ6SSGPF6T32I3OC5BROQ (fee 1000)
Transaction 3I3F4T27ADM5K6QOYSCFE35BFAIPCRVYZ6SSGPF6T32I3OC5BROQ still pending as of round 10424193
Transaction 3I3F4T27ADM5K6QOYSCFE35BFAIPCRVYZ6SSGPF6T32I3OC5BROQ committed in round 10424195
Created app with app index 13114506


goal app optin --app-id 13114506 --from 46JO4OCM3RNMD3S5SCSYLQX7LAGSR3QOIKFPZXOUIRR66NUPN62SULNUEM

Issued transaction from account 46JO4OCM3RNMD3S5SCSYLQX7LAGSR3QOIKFPZXOUIRR66NUPN62SULNUEM, txid ZUVWNY2WNZDLW2RKWSRANTTXFIZ7GOBLP3DUPAH44KGDSW3OA6WA (fee 1000)
Transaction ZUVWNY2WNZDLW2RKWSRANTTXFIZ7GOBLP3DUPAH44KGDSW3OA6WA still pending as of round 10424315
Transaction ZUVWNY2WNZDLW2RKWSRANTTXFIZ7GOBLP3DUPAH44KGDSW3OA6WA committed in round 10424317


goal app call --app-id 13114506 --from 46JO4OCM3RNMD3S5SCSYLQX7LAGSR3QOIKFPZXOUIRR66NUPN62SULNUEM --app-arg "str:put_value_to_local" --app-arg "int:0"

Issued transaction from account 46JO4OCM3RNMD3S5SCSYLQX7LAGSR3QOIKFPZXOUIRR66NUPN62SULNUEM, txid YY4RI37QOMFVNNIOIZM757TDOH3VB6JMXISXZVY4NTWIF6CYPFOQ (fee 1000)
Transaction YY4RI37QOMFVNNIOIZM757TDOH3VB6JMXISXZVY4NTWIF6CYPFOQ still pending as of round 10424339
Transaction YY4RI37QOMFVNNIOIZM757TDOH3VB6JMXISXZVY4NTWIF6CYPFOQ committed in round 10424341
```

We can verify the local state using:

```
goal app read --local --from 46JO4OCM3RNMD3S5SCSYLQX7LAGSR3QOIKFPZXOUIRR66NUPN62SULNUEM --app-id 13114506
{
    "local": {
        "tt": 2,
        "ui": 1
    }
}
```

We try to read the local value of 46J0.. associated to the app 13114506 from BWPH.. with the app 13128112:

```
goal app call --app-id 13128112 --from BWPHWE6Z7WGRYUODABVBAZLHPDCDXEF5BYFYPWJQL2YNCF3RJATXQFB3UM --app-account 46JO4OCM3RNMD3S5SCSYLQX7LAGSR3QOIKFPZXOUIRR66NUPN62SULNUEM --app-arg "str:get_value_from_local_other" --app-arg "int:1" --app-arg "int:13114506"

Issued transaction from account BWPHWE6Z7WGRYUODABVBAZLHPDCDXEF5BYFYPWJQL2YNCF3RJATXQFB3UM, txid V3KCRMGESHCD64K6BYTYXBQNKRAEM5C4KRXBVRHXPFP35PFJM7VA (fee 1000)
Transaction V3KCRMGESHCD64K6BYTYXBQNKRAEM5C4KRXBVRHXPFP35PFJM7VA still pending as of round 10460274
Transaction V3KCRMGESHCD64K6BYTYXBQNKRAEM5C4KRXBVRHXPFP35PFJM7VA committed in round 10460276
```

As expected it works.

We try to do the same with an account that does not have anything stored in his local store:

```
goal app optin --app-id 13114506 --from KK3SSF7NAKSUXFZ27QUTNBGL6525RPPO4HBL3FJYFSPJ45UMQGURECCGUU

Issued transaction from account KK3SSF7NAKSUXFZ27QUTNBGL6525RPPO4HBL3FJYFSPJ45UMQGURECCGUU, txid FRVSCYKCQA2ZYDBLZG2Y64W7ZIOYFJVEG7L2QVBQJKKLGNBDCSSQ (fee 1000)
Transaction FRVSCYKCQA2ZYDBLZG2Y64W7ZIOYFJVEG7L2QVBQJKKLGNBDCSSQ still pending as of round 10424614
Transaction FRVSCYKCQA2ZYDBLZG2Y64W7ZIOYFJVEG7L2QVBQJKKLGNBDCSSQ committed in round 10424616
        
goal app call --app-id 13128112 --from BWPHWE6Z7WGRYUODABVBAZLHPDCDXEF5BYFYPWJQL2YNCF3RJATXQFB3UM --app-account KK3SSF7NAKSUXFZ27QUTNBGL6525RPPO4HBL3FJYFSPJ45UMQGURECCGUU --app-arg "str:get_value_from_local_other" --app-arg "int:1" --app-arg "int:13114506"

Couldn't broadcast tx with algod: HTTP 400 Bad Request: TransactionPool.Remember: transaction BO267OS74AUFFY337CQSZCXOYYLBJN2JNZNIUL3U23CEA75LQFTQ: transaction rejected by ApprovalProgram
```

As we expected the transaction has been rejected by the contract logic because there is no anything stored into the account local state.

### Get a value stored into an account local state associated to another app - caller not opted in

We start from the previous experiment in which we have the following accounts:

```
goal account list

46JO4OCM3RNMD3S5SCSYLQX7LAGSR3QOIKFPZXOUIRR66NUPN62SULNUEM	99996000 microAlgos	[created app IDs: 13114506]	[opted in app IDs: 13114506]
KK3SSF7NAKSUXFZ27QUTNBGL6525RPPO4HBL3FJYFSPJ45UMQGURECCGUU	99994000 microAlgos
BWPHWE6Z7WGRYUODABVBAZLHPDCDXEF5BYFYPWJQL2YNCF3RJATXQFB3UM	99985000 microAlgos	[created app IDs: 13128112]	[opted in app IDs: 13128112]
```

As we know, 46JO.. has the following value stored in the local state associated to the contract 13114506:

```
goal app read --local --from 46JO4OCM3RNMD3S5SCSYLQX7LAGSR3QOIKFPZXOUIRR66NUPN62SULNUEM --app-id 13114506

{
  "local": {
    "tt": 2,
    "ui": 1
  }
}
```

Now we try to get the value from the local state of 46JO associated to 13114506 with a TransactionCall to the contract 13128112 in which the caller is KK3S... Notice that the account KK3S.. is not opted in to 13128112.

```
goal app call --app-id 13128112 --from KK3SSF7NAKSUXFZ27QUTNBGL6525RPPO4HBL3FJYFSPJ45UMQGURECCGUU --app-account 46JO4OCM3RNMD3S5SCSYLQX7LAGSR3QOIKFPZXOUIRR66NUPN62SULNUEM --app-arg "str:get_value_from_local_other" --app-arg "int:1" --app-arg "int:13114506"

Issued transaction from account KK3SSF7NAKSUXFZ27QUTNBGL6525RPPO4HBL3FJYFSPJ45UMQGURECCGUU, txid AW45JDF5STPB27MXDA5DFTLPOGP5ANZO6F5T75O565UG3QYSE6HA (fee 1000)
Transaction AW45JDF5STPB27MXDA5DFTLPOGP5ANZO6F5T75O565UG3QYSE6HA still pending as of round 10500388
Transaction AW45JDF5STPB27MXDA5DFTLPOGP5ANZO6F5T75O565UG3QYSE6HA committed in round 10500390
```

As we expected it works even if KK3S.. is not opted in to the contract 13128112. This because the TransactionCall is used to get a value from the local state, and no write operation to local state is made.

### Use more than 4 additional accounts

Assume that we have the following accounts:

```
goal account list

DQKKD4CKN7UNSUNDNFK7VJMPWUSRPN2DZJALNFXTG5KLQESYAXT64M5M4M	99992000 microAlgos [opted in app 13128112]
VU5CRNAPNZ62UIRP6P7DZ6PZUBZHILUHGR2WTPM323KHGZFWZ5UAVMOREY	99492000 microAlgos
46JO4OCM3RNMD3S5SCSYLQX7LAGSR3QOIKFPZXOUIRR66NUPN62SULNUEM	99996000 microAlgos
TWPAXE6X5Z3ELUJJEPDRH3QBCDRWSEWVDMUOTEEEZ5SJ5S4MELTZRVXZOE	99990000 microAlgos
XH72MYAIR7PXBIMMZFSMFPHWUWMIMON354BYQVMYPH6AO6UTIDI6DHIJYI	99998000 microAlgos
```
And assume that DQKK... creates the contract using the code mentioned above.



We try to add more than 4 additional accounts to the app call:

```
goal app call --app-id 13128112 --from DQKKD4CKN7UNSUNDNFK7VJMPWUSRPN2DZJALNFXTG5KLQESYAXT64M5M4M --app-account VU5CRNAPNZ62UIRP6P7DZ6PZUBZHILUHGR2WTPM323KHGZFWZ5UAVMOREY --app-account TWPAXE6X5Z3ELUJJEPDRH3QBCDRWSEWVDMUOTEEEZ5SJ5S4MELTZRVXZOE --app-account XH72MYAIR7PXBIMMZFSMFPHWUWMIMON354BYQVMYPH6AO6UTIDI6DHIJYI --app-account KK3SSF7NAKSUXFZ27QUTNBGL6525RPPO4HBL3FJYFSPJ45UMQGURECCGUU --app-account 46JO4OCM3RNMD3S5SCSYLQX7LAGSR3QOIKFPZXOUIRR66NUPN62SULNUEM --app-arg "str:put_value_to_local" --app-arg "int:0"
```


As expected, the transaction fails:

```
Couldn't broadcast tx with algod: HTTP 400 Bad Request: tx.Accounts too long, max number of accounts is 4
```


Then, we try to do the same app call with 4 additional accounts:

```
goal app call --app-id 13128112 --from DQKKD4CKN7UNSUNDNFK7VJMPWUSRPN2DZJALNFXTG5KLQESYAXT64M5M4M --app-account VU5CRNAPNZ62UIRP6P7DZ6PZUBZHILUHGR2WTPM323KHGZFWZ5UAVMOREY --app-account TWPAXE6X5Z3ELUJJEPDRH3QBCDRWSEWVDMUOTEEEZ5SJ5S4MELTZRVXZOE --app-account XH72MYAIR7PXBIMMZFSMFPHWUWMIMON354BYQVMYPH6AO6UTIDI6DHIJYI --app-account KK3SSF7NAKSUXFZ27QUTNBGL6525RPPO4HBL3FJYFSPJ45UMQGURECCGUU --app-arg "str:put_value_to_local" --app-arg "int:0"
```

As expected, it works:

```
Issued transaction from account DQKKD4CKN7UNSUNDNFK7VJMPWUSRPN2DZJALNFXTG5KLQESYAXT64M5M4M, txid LUMZF2CLJ4JVH45DZS7TS4RAWSNSZ7SRYLY6NW72V6AJGZS4MXIA (fee 1000)
Transaction LUMZF2CLJ4JVH45DZS7TS4RAWSNSZ7SRYLY6NW72V6AJGZS4MXIA still pending as of round 10459864
Transaction LUMZF2CLJ4JVH45DZS7TS4RAWSNSZ7SRYLY6NW72V6AJGZS4MXIA committed in round 10459866
```

