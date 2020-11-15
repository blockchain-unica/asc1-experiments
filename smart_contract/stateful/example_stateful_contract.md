## Example stateful smart contract

### Create a stateful smart contract
This smart contract has been used as example for some experiments related to stateful smart contract and to test some cases that can occur in stateful smart contracts.

It is composed by two files: approval_program.teal and clear_state_program.teal

We create the following file called approval_program.teal that is responsible for processing all application calls to the contract, with the exception of the clear call.

```
#pragma version 2

int 0
txn ApplicationID
==
bnz creation

int DeleteApplication
txn OnCompletion
==
bnz deletion

int UpdateApplication
txn OnCompletion
==
bnz update

int CloseOut
txn OnCompletion
==
bnz close_out

int OptIn
txn OnCompletion
==
bnz optin

txna ApplicationArgs 0
byte "put_value_to_local"
==
bnz put_value_to_local

txna ApplicationArgs 0
byte "get_value_from_local"
==
bnz get_value_from_local

txna ApplicationArgs 0
byte "get_value_from_local_other"
==
bnz get_value_from_local_other

txna ApplicationArgs 0
byte "put_value_to_global"
==
bnz put_value_to_global

txna ApplicationArgs 0
byte "get_value_from_global"
==
bnz get_value_from_global

creation:
b finish

deletion:
b finish

update:
b finish

close_out:
b finish

optin:
b finish

put_value_to_local:
txna ApplicationArgs 1
btoi    //address
byte "local"
int 1   // put 1 to local
app_local_put
b finish

get_value_from_local:
txna ApplicationArgs 1
btoi    //address
txn ApplicationID
byte "local"
app_local_get_ex
bz failed
return

get_value_from_local_other:
txna ApplicationArgs 1
btoi    //address
txna ApplicationArgs 2
btoi    //application ID
byte "local"
app_local_get_ex
bz failed
return

put_value_to_global:
byte "global"
int 1   //put 1 to global
app_global_put
b finish

get_value_from_global:
txna ApplicationArgs 1
btoi    //application ID
byte "global"
app_global_get_ex
bz failed
return

finish:
int 1
return

failed:
int 0
return
```

Then we create a file called clear_state_program.teal that handles clear calls to remove the smart contract from their balance record

```
#pragma version 2

int 1 
return
```

We can create the contract in this way:
```
goal app create --creator DQKKD4CKN7UNSUNDNFK7VJMPWUSRPN2DZJALNFXTG5KLQESYAXT64M5M4M --approval-prog approval_program.teal --clear-prog ./clear_state_program.teal --global-byteslices 1 --global-ints 1 --local-byteslices 1 --local-ints 1 -d /opt/algorand/node/data

Attempting to create app (approval size 288, hash Q73AJHTDEYBG23P6VZ2RA2DQUDGPRB37D3BSIBVBFMECINK4HFSA; clear size 6, hash ZYI7YTWEXF6FGMRDOJNAGIID5M7OKO554TJOVU2RCA7Z2QWQEBTA)
Issued transaction from account DQKKD4CKN7UNSUNDNFK7VJMPWUSRPN2DZJALNFXTG5KLQESYAXT64M5M4M, txid BXJUBLW2E3SZPMTBQ2DD2D5ANB26R3CYFIUVWW3VR6S5PK3ANVGA (fee 1000)
Transaction BXJUBLW2E3SZPMTBQ2DD2D5ANB26R3CYFIUVWW3VR6S5PK3ANVGA still pending as of round 10425183
Transaction BXJUBLW2E3SZPMTBQ2DD2D5ANB26R3CYFIUVWW3VR6S5PK3ANVGA committed in round 10425185 Created app with app index 13114568
```
"--global-byteslices", "--global-ints", "--local-byteslices" and "--local-ints" values must be provided and represent the amount of space that the smart contract will use.

Once the contract has been created, an ID will be generated. It could be used to make ApplicationCalls transactions to the smart contract.

