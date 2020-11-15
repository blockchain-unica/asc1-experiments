## Global state

### Add no more than 2 additional contracts

We suppose to have the following accounts:

```
goal account list

DQKKD4CKN7UNSUNDNFK7VJMPWUSRPN2DZJALNFXTG5KLQESYAXT64M5M4M	99992000 microAlgos
KK3SSF7NAKSUXFZ27QUTNBGL6525RPPO4HBL3FJYFSPJ45UMQGURECCGUU	99995000 microAlgos
XH72MYAIR7PXBIMMZFSMFPHWUWMIMON354BYQVMYPH6AO6UTIDI6DHIJYI	99998000 microAlgos
H7AVRUTZA2WKLCJJP2Z5XNONE3FNMLAKEWAYAFGLC5ZVN3ZORVGOUJ33FY	99999000 microAlgos
```
We create the following contracts with [this code](./example_stateful_contract.md):

```
goal contract create --creator DQKKD4CKN7UNSUNDNFK7VJMPWUSRPN2DZJALNFXTG5KLQESYAXT64M5M4M --approval-prog approval_program.teal --clear-prog ./clear_state_program.teal --global-byteslices 1 --global-ints 1 --local-byteslices 1 --local-ints 1 -d /opt/algorand/node/data

    Attempting to create app (approval size 288, hash Q73AJHTDEYBG23P6VZ2RA2DQUDGPRB37D3BSIBVBFMECINK4HFSA; clear size 6, hash ZYI7YTWEXF6FGMRDOJNAGIID5M7OKO554TJOVU2RCA7Z2QWQEBTA)
    Issued transaction from account DQKKD4CKN7UNSUNDNFK7VJMPWUSRPN2DZJALNFXTG5KLQESYAXT64M5M4M, txid BXJUBLW2E3SZPMTBQ2DD2D5ANB26R3CYFIUVWW3VR6S5PK3ANVGA (fee 1000)
    Transaction BXJUBLW2E3SZPMTBQ2DD2D5ANB26R3CYFIUVWW3VR6S5PK3ANVGA still pending as of round 10425183
    Transaction BXJUBLW2E3SZPMTBQ2DD2D5ANB26R3CYFIUVWW3VR6S5PK3ANVGA committed in round 10425185
    Created app with app index 13114568


goal app create --creator KK3SSF7NAKSUXFZ27QUTNBGL6525RPPO4HBL3FJYFSPJ45UMQGURECCGUU --approval-prog approval_program.teal --clear-prog ./clear_state_program.teal --global-byteslices 1 --global-ints 1 --local-byteslices 1 --local-ints 1 -d /opt/algorand/node/data

    Attempting to create app (approval size 288, hash Q73AJHTDEYBG23P6VZ2RA2DQUDGPRB37D3BSIBVBFMECINK4HFSA; clear size 6, hash ZYI7YTWEXF6FGMRDOJNAGIID5M7OKO554TJOVU2RCA7Z2QWQEBTA)
    Issued transaction from account KK3SSF7NAKSUXFZ27QUTNBGL6525RPPO4HBL3FJYFSPJ45UMQGURECCGUU, txid D3CGJXMD4AQRJ5XNAHIBMRZGY7AUTKWJEPXIB2EPKWUUYRR2IC7A (fee 1000)
    Transaction D3CGJXMD4AQRJ5XNAHIBMRZGY7AUTKWJEPXIB2EPKWUUYRR2IC7A still pending as of round 10425204
    Transaction D3CGJXMD4AQRJ5XNAHIBMRZGY7AUTKWJEPXIB2EPKWUUYRR2IC7A committed in round 10425206
    Created app with app index 13114570


goal app create --creator XH72MYAIR7PXBIMMZFSMFPHWUWMIMON354BYQVMYPH6AO6UTIDI6DHIJYI --approval-prog approval_program.teal --clear-prog ./clear_state_program.teal --global-byteslices 1 --global-ints 1 --local-byteslices 1 --local-ints 1 -d /opt/algorand/node/data

    Attempting to create app (approval size 288, hash Q73AJHTDEYBG23P6VZ2RA2DQUDGPRB37D3BSIBVBFMECINK4HFSA; clear size 6, hash ZYI7YTWEXF6FGMRDOJNAGIID5M7OKO554TJOVU2RCA7Z2QWQEBTA)
    Issued transaction from account XH72MYAIR7PXBIMMZFSMFPHWUWMIMON354BYQVMYPH6AO6UTIDI6DHIJYI, txid MMXHN4UGTVGM366PGIAFS7SW2OJI7VQEA42YSP2KSWI6FBF2DS2A (fee 1000)
    Transaction MMXHN4UGTVGM366PGIAFS7SW2OJI7VQEA42YSP2KSWI6FBF2DS2A still pending as of round 10425229
    Transaction MMXHN4UGTVGM366PGIAFS7SW2OJI7VQEA42YSP2KSWI6FBF2DS2A committed in round 10425231
    Created app with app index 13114575


goal app create --creator H7AVRUTZA2WKLCJJP2Z5XNONE3FNMLAKEWAYAFGLC5ZVN3ZORVGOUJ33FY --approval-prog approval_program.teal --clear-prog ./clear_state_program.teal --global-byteslices 1 --global-ints 1 --local-byteslices 1 --local-ints 1 -d /opt/algorand/node/data

    Attempting to create app (approval size 288, hash Q73AJHTDEYBG23P6VZ2RA2DQUDGPRB37D3BSIBVBFMECINK4HFSA; clear size 6, hash ZYI7YTWEXF6FGMRDOJNAGIID5M7OKO554TJOVU2RCA7Z2QWQEBTA)
    Issued transaction from account H7AVRUTZA2WKLCJJP2Z5XNONE3FNMLAKEWAYAFGLC5ZVN3ZORVGOUJ33FY, txid L2YO4MZTZWEM5L6B5XCJPADIUP7UR3QFQHRHPAW6DZWUYV5PEPIA (fee 1000)
    Transaction L2YO4MZTZWEM5L6B5XCJPADIUP7UR3QFQHRHPAW6DZWUYV5PEPIA still pending as of round 10425257
    Transaction L2YO4MZTZWEM5L6B5XCJPADIUP7UR3QFQHRHPAW6DZWUYV5PEPIA committed in round 10425259
    Created app with app index 13114577
```

We try to add more than 2 additional contracts to a contract call:

```
goal app call --app-id 13114568 --from DQKKD4CKN7UNSUNDNFK7VJMPWUSRPN2DZJALNFXTG5KLQESYAXT64M5M4M --foreign-app 13114570 --foreign-app 13114575 --foreign-app 13114577 --app-arg "str:put_value_to_global"

Couldn't broadcast tx with algod: HTTP 400 Bad Request: tx.ForeignApps too long, max number of foreign apps is 2:
```
As expected the transaction has been rejected.

We try with at most 2 additional accounts:

```
goal app call --app-id 13114568 --from DQKKD4CKN7UNSUNDNFK7VJMPWUSRPN2DZJALNFXTG5KLQESYAXT64M5M4M --foreign-app 13114570 --foreign-app 13114575 --app-arg "str:put_value_to_global"

Issued transaction from account DQKKD4CKN7UNSUNDNFK7VJMPWUSRPN2DZJALNFXTG5KLQESYAXT64M5M4M, txid YPRNLULQUPLNFUVNXYPTWBWNB63DSQCQQMXKANRFSFBWSDF7U3EA (fee 1000)
Transaction YPRNLULQUPLNFUVNXYPTWBWNB63DSQCQQMXKANRFSFBWSDF7U3EA still pending as of round 10439216
Transaction YPRNLULQUPLNFUVNXYPTWBWNB63DSQCQQMXKANRFSFBWSDF7U3EA committed in round 10439218
```

As expected it works.

### Put a value in the global state - account not opted in

We try to put a value in the global state even if the account is not opten in the contract:

```
goal app call --app-id 13114568 --from BWPHWE6Z7WGRYUODABVBAZLHPDCDXEF5BYFYPWJQL2YNCF3RJATXQFB3UM --app-arg "str:put_value_to_global"

Issued transaction from account BWPHWE6Z7WGRYUODABVBAZLHPDCDXEF5BYFYPWJQL2YNCF3RJATXQFB3UM, txid ZOO3X7XFLPCZBAXPOLFZ5HQQVN4PWLCI2L6S56Y75DNTG2CFSKGA (fee 1000)
Transaction ZOO3X7XFLPCZBAXPOLFZ5HQQVN4PWLCI2L6S56Y75DNTG2CFSKGA still pending as of round 10439317
Transaction ZOO3X7XFLPCZBAXPOLFZ5HQQVN4PWLCI2L6S56Y75DNTG2CFSKGA committed in round 10439319
```

As expected it works. This because opting in the account to the contract is needed only if we have to call an application transaction call that writes into local state. We can get the value stored in global store's app using:

```
goal app read --global --app-id 13114568

    {
        "global": {
            "tt": 2,
            "ui": 1
        }
    }
```

### Read account global state from another additional contract

We try to read a account global state from another additional contract.

To do this we put a value in account global state with id 13114570:

```
goal app call --app-id 13114570 --from KK3SSF7NAKSUXFZ27QUTNBGL6525RPPO4HBL3FJYFSPJ45UMQGURECCGUU --app-arg "str:put_value_to_global"

Issued transaction from account KK3SSF7NAKSUXFZ27QUTNBGL6525RPPO4HBL3FJYFSPJ45UMQGURECCGUU, txid USAIRQWKDG64EGXBB2MY3F4PMHYF6ABNHBMTMC6LKN4KIYI6E6SA (fee 1000)
Transaction USAIRQWKDG64EGXBB2MY3F4PMHYF6ABNHBMTMC6LKN4KIYI6E6SA still pending as of round 10439715
Transaction USAIRQWKDG64EGXBB2MY3F4PMHYF6ABNHBMTMC6LKN4KIYI6E6SA committed in round 10439717
```

We verify if the value has been correctly stored:

```
goal app read --global --app-id 13114570

        {
            "global": {
                "tt": 2,
                "ui": 1
           }
        }
```

Then, we try to read the value from another contract (id: 13114568) in which the called it is not opted in to the calling contract:

```
goal app call --app-id 13114568 --from BWPHWE6Z7WGRYUODABVBAZLHPDCDXEF5BYFYPWJQL2YNCF3RJATXQFB3UM --foreign-app 13114570 --app-arg "str:get_value_from_global" --app-arg "int:1"

Issued transaction from account BWPHWE6Z7WGRYUODABVBAZLHPDCDXEF5BYFYPWJQL2YNCF3RJATXQFB3UM, txid DJRWVOVIFC7OIXVOKCUQ6G26QCUF64H6DN4FHECKBME4RZT6GKGQ (fee 1000)
Transaction DJRWVOVIFC7OIXVOKCUQ6G26QCUF64H6DN4FHECKBME4RZT6GKGQ still pending as of round 10439782
Transaction DJRWVOVIFC7OIXVOKCUQ6G26QCUF64H6DN4FHECKBME4RZT6GKGQ committed in round 10439784
```

As expected the transaction has been accepted by the contract logic, so we get the global value of contract 13114570.

Now we try to make the same call with another additional contract without the global value:

```
goal app call --app-id 13114568 --from BWPHWE6Z7WGRYUODABVBAZLHPDCDXEF5BYFYPWJQL2YNCF3RJATXQFB3UM --foreign-app 13114577 --app-arg "str:get_value_from_global" --app-arg "int:1"

Couldn't broadcast tx with algod: HTTP 400 Bad Request: TransactionPool.Remember: transaction QJJ4IZDPTMPJ7LZ3R3FZ62SOZRAGPPGHV2W4YVSBYJLWDYUWBYCA: transaction rejected by ApprovalProgram
```
As expected according the contract logic the transaction has been rejected.

