## Crowdfunding

This example is fully explained [here](https://developer.algorand.org/solutions/example-crowdfunding-stateful-smart-contract-application/). The code that refers this document is available [here](https://github.com/algorand/smart-contracts/tree/master/devrel/crowdfunding)

We have the following accounts:

```
goal account list

CPOZRLW5POOJOAMYRD6W6YXD4FOEYUP45NHMHOPCHOIWZEOKDU6VGKUALA	99993000 microAlgos	
PKKZSQH5VQY2MB7HWL2KF6C4M2N42URIEFSLZUFV2UZBMHR5FEQDMLTXRE	99990000 microAlgos
```

To handle the crowdfunding we need:
- a stateful contract that handles all the logic of the crowdfunding
- a stateless contract that works like an escrow account in which all the money is temporarily escrowed.

The crowdfunding contract must handle 5 cases:
- Create the fund
- Update the contract
- Donate
- Withdraw funds
- Recover donations
- Delete fund

### Create the fund

First of all, we must create the fund. We need to pass as parameters the range (in timestamp) in which we can donate money, the goal that must be reached to allow the receiver to retrieve the money from the contract and the end timestamp that indicates when the accounts can retrieve money from the contract.

```
goal app create --creator CPOZRLW5POOJOAMYRD6W6YXD4FOEYUP45NHMHOPCHOIWZEOKDU6VGKUALA --approval-prog ./crowd_fund.teal --global-byteslices 3 --global-ints 5 --local-byteslices 0 --local-ints 1 --app-arg "int:1605627674" --app-arg "int:1605636000" --app-arg "int:1000000" --app-arg "addr:CPOZRLW5POOJOAMYRD6W6YXD4FOEYUP45NHMHOPCHOIWZEOKDU6VGKUALA" --app-arg "int:1605636000" --clear-prog ./crowd_fund_close.teal

Attempting to create app (approval size 551, hash ZXOJN6BG5MBI7PH5HDK3AXLVKOVGEPTYGPIL4P236IQMOWXMADUQ; clear size 6, hash ZYI7YTWEXF6FGMRDOJNAGIID5M7OKO554TJOVU2RCA7Z2QWQEBTA)
Issued transaction from account CPOZRLW5POOJOAMYRD6W6YXD4FOEYUP45NHMHOPCHOIWZEOKDU6VGKUALA, txid MDS4RIVTOAO7C5XAHMB4LT5IOTLU7DGHRT4XNFE7DXLBSTWQYIAQ (fee 1000)
Transaction MDS4RIVTOAO7C5XAHMB4LT5IOTLU7DGHRT4XNFE7DXLBSTWQYIAQ still pending as of round 10544636
Transaction MDS4RIVTOAO7C5XAHMB4LT5IOTLU7DGHRT4XNFE7DXLBSTWQYIAQ committed in round 10544638
Created app with app index 13164266
```

Once the stateful contract has been created, we need to create the Escrow account using a stateless contract. We must wait to the creation of the stateful contract because we need to hardcode the app id of the stateful contract inside the stateless code.

```
goal clerk compile crowd_fund_escrow.teal 

crowd_fund_escrow.teal: V7MY24WJAMXRQ6GVQQJUILEORADJMWBKGFJNKHTKBXKXHKNG4X2UELGXRE
```

### Update the contract

We must update the stateful contract with the stateless contract's address.

```
goal app update --app-id=13164266 --from CPOZRLW5POOJOAMYRD6W6YXD4FOEYUP45NHMHOPCHOIWZEOKDU6VGKUALA  --approval-prog ./crowd_fund.teal --clear-prog ./crowd_fund_close.teal --app-arg "addr:V7MY24WJAMXRQ6GVQQJUILEORADJMWBKGFJNKHTKBXKXHKNG4X2UELGXRE"

Attempting to update app (approval size 551, hash ZXOJN6BG5MBI7PH5HDK3AXLVKOVGEPTYGPIL4P236IQMOWXMADUQ; clear size 6, hash ZYI7YTWEXF6FGMRDOJNAGIID5M7OKO554TJOVU2RCA7Z2QWQEBTA)
Issued transaction from account CPOZRLW5POOJOAMYRD6W6YXD4FOEYUP45NHMHOPCHOIWZEOKDU6VGKUALA, txid FXLTYSIKCCX4S2MOHURRLC5LWYIG57H7CIEMSQJHGYRRZY4YEM3Q (fee 1000)
Transaction FXLTYSIKCCX4S2MOHURRLC5LWYIG57H7CIEMSQJHGYRRZY4YEM3Q still pending as of round 10544704
Transaction FXLTYSIKCCX4S2MOHURRLC5LWYIG57H7CIEMSQJHGYRRZY4YEM3Q committed in round 10544706
```

The donator must be opt in to the app because the stateful contract has to write to the donator local state.

```
goal app optin --app-id 13164266 --from PKKZSQH5VQY2MB7HWL2KF6C4M2N42URIEFSLZUFV2UZBMHR5FEQDMLTXRE

Issued transaction from account PKKZSQH5VQY2MB7HWL2KF6C4M2N42URIEFSLZUFV2UZBMHR5FEQDMLTXRE, txid WYEOWL5JLIVJ6FZRFMB4U5F6GRK3WTUIUPJYP6PMTAPTMQRTWW3A (fee 1000)
Transaction WYEOWL5JLIVJ6FZRFMB4U5F6GRK3WTUIUPJYP6PMTAPTMQRTWW3A still pending as of round 10544830
Transaction WYEOWL5JLIVJ6FZRFMB4U5F6GRK3WTUIUPJYP6PMTAPTMQRTWW3A committed in round 10544832
```

### Donate

The donator have to group 2 transaction to donate:
- An App call that tells the stateful app the intention to donate
- A transaction that sends the amount to the escrow account.

```
goal app call --app-id 13164266 --app-arg "str:donate" --from=PKKZSQH5VQY2MB7HWL2KF6C4M2N42URIEFSLZUFV2UZBMHR5FEQDMLTXRE --out=unsignedtransaction1.tx

goal clerk send --from=PKKZSQH5VQY2MB7HWL2KF6C4M2N42URIEFSLZUFV2UZBMHR5FEQDMLTXRE --to=V7MY24WJAMXRQ6GVQQJUILEORADJMWBKGFJNKHTKBXKXHKNG4X2UELGXRE --amount=100000 --out=unsignedtransaction2.tx

cat unsignedtransaction1.tx unsignedtransaction2.tx > combinedtransactions.tx

goal clerk group -i combinedtransactions.tx -o groupedtransactions.tx

goal clerk sign -i groupedtransactions.tx -o signout.tx

goal clerk rawsend -f signout.tx

Raw transaction ID IOXRZQTCWFPB6GOAFNNBXXN22C7VWO4O3NRXFMNC6UD3LGSSDR5A issued
Raw transaction ID CUL6Z4P2QXRKGKE5LTW225NF5M6M74G4RRNNKZEV2JVOSJ2R3QUA issued
Transaction CUL6Z4P2QXRKGKE5LTW225NF5M6M74G4RRNNKZEV2JVOSJ2R3QUA still pending as of round 10544928
Transaction CUL6Z4P2QXRKGKE5LTW225NF5M6M74G4RRNNKZEV2JVOSJ2R3QUA committed in round 10544930
Transaction IOXRZQTCWFPB6GOAFNNBXXN22C7VWO4O3NRXFMNC6UD3LGSSDR5A committed in round 10544930
```

We can see what happens to the local state of PKKZ.. and to the global state of the contract.

```
goal app read --local --app-id 13164266 --from=PKKZSQH5VQY2MB7HWL2KF6C4M2N42URIEFSLZUFV2UZBMHR5FEQDMLTXRE

{
  "MyAmountGiven": {
    "tt": 2,
    "ui": 500000
  }
}

goal app read --global --app-id 13164266

{
.
.
.
  "Total": {
    "tt": 2,
    "ui": 500000
  }
}
```

### Withdraw funds

Once the timestamp specified as parameter at the creation of the contract has been passed and the goal has been reached, the receiver can withdraw the funds. 
To do this it has to group two transactions:
- An App call that tells the stateful app that the receiver wants to withdraw funds
- A transaction that sends money from the escrow contract to the receiver

```
goal app call --app-id 13164266 --app-arg "str:claim"  --from CPOZRLW5POOJOAMYRD6W6YXD4FOEYUP45NHMHOPCHOIWZEOKDU6VGKUALA  --out=unsignedtransaction1.tx

goal clerk send --to=CPOZRLW5POOJOAMYRD6W6YXD4FOEYUP45NHMHOPCHOIWZEOKDU6VGKUALA --close-to=CPOZRLW5POOJOAMYRD6W6YXD4FOEYUP45NHMHOPCHOIWZEOKDU6VGKUALA --from-program=./crowd_fund_escrow.teal --amount=0 --out=unsignedtransaction2.tx

cat unsignedtransaction1.tx unsignedtransaction2.tx > combinedtransactions.tx

goal clerk group -i combinedtransactions.tx -o groupedtransactions.tx

goal clerk split -i groupedtransactions.tx -o split.tx 

goal clerk sign -i split-0.tx -o signout-0.tx

cat signout-0.tx split-1.tx > signout.tx

goal clerk rawsend -f signout.tx
```

### Recover donations

If the goal hasn't been reached and the timestamp limit has been reached, who sended donations can retrieve the money. To do this they have to group two transactions:
- An App call that tells the stateful app that donators want to recover funds
- A transaction that sends money from the escrow contract to the donators

Notice that in the second transaction we have to take into account the fee, so for this reason the amount retrieved is less than the sended amount.

```
goal app call --app-id 13164266 --app-arg "str:reclaim"  --from PKKZSQH5VQY2MB7HWL2KF6C4M2N42URIEFSLZUFV2UZBMHR5FEQDMLTXRE --out=unsignedtransaction1.tx

goal clerk send --to=PKKZSQH5VQY2MB7HWL2KF6C4M2N42URIEFSLZUFV2UZBMHR5FEQDMLTXRE --close-to=PKKZSQH5VQY2MB7HWL2KF6C4M2N42URIEFSLZUFV2UZBMHR5FEQDMLTXRE --from-program=./crowd_fund_escrow.teal --amount=499000 --out=unsignedtransaction2.tx

cat unsignedtransaction1.tx unsignedtransaction2.tx > combinedtransactions.tx

goal clerk group -i combinedtransactions.tx -o groupedtransactions.tx

goal clerk split -i groupedtransactions.tx -o split.tx 

goal clerk sign -i split-0.tx -o signout-0.tx

cat signout-0.tx split-1.tx > signout.tx

goal clerk rawsend -f signout.tx
```

### Delete fund

If the timestamp limit has been reached, the creator can delete the contract. But first the escrow account must be close out as well.

```
goal app delete --app-id 13164266 --from CPOZRLW5POOJOAMYRD6W6YXD4FOEYUP45NHMHOPCHOIWZEOKDU6VGKUALA --app-account V7MY24WJAMXRQ6GVQQJUILEORADJMWBKGFJNKHTKBXKXHKNG4X2UELGXRE --out=unsignedtransaction1.tx

goal clerk send --from-program=./crowd_fund_escrow.teal --to=CPOZRLW5POOJOAMYRD6W6YXD4FOEYUP45NHMHOPCHOIWZEOKDU6VGKUALA --amount=0 -c CPOZRLW5POOJOAMYRD6W6YXD4FOEYUP45NHMHOPCHOIWZEOKDU6VGKUALA --out=unsignedtransaction2.tx

cat unsignedtransaction1.tx unsignedtransaction2.tx > combinedtransactions.tx

goal clerk group -i combinedtransactions.tx -o groupedtransactions.tx

goal clerk split -i groupedtransactions.tx -o split.tx 

goal clerk sign -i split-0.tx -o signout-0.tx

cat signout-0.tx split-1.tx > signout.tx

goal clerk rawsend -f signout.tx
```









