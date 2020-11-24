## Permissionless voting

The following example, written in PyTeal is reported [here](https://developer.algorand.org/articles/creating-stateful-algorand-smart-contracts-python-pyteal/). The contract logic (written in TEAL) is fully explained [here](https://developer.algorand.org/solutions/example-permissionless-voting-stateful-smart-contract-application/).

The permissionless voting allows every account to vote, but only once. 

To build this contract we have to handle 4 parts:
- Create voting smart contract
- Register to vote
- Vote
- Close out

### Create voting smart contract

First of all we must create the voting smart contract. The contract takes four parameters that represent the range (expressed in rounds) in which an account can opt in and vote to the contract. 


We have the following accounts:

```
goal account list

CPOZRLW5POOJOAMYRD6W6YXD4FOEYUP45NHMHOPCHOIWZEOKDU6VGKUALA  99488000 microAlgos
PKKZSQH5VQY2MB7HWL2KF6C4M2N42URIEFSLZUFV2UZBMHR5FEQDMLTXRE	99887000 microAlgos
```

Now, we must create the contract:

```
goal app create --creator CPOZRLW5POOJOAMYRD6W6YXD4FOEYUP45NHMHOPCHOIWZEOKDU6VGKUALA --approval-prog ./vote_approval.teal --global-byteslices 1 --global-ints 6 --local-byteslices 1 --local-ints 0 --app-arg "int:10000000" --app-arg "int:10700000" --app-arg "int:10000000" --app-arg "int:10700000" --clear-prog ./vote_clear_state.teal 

Attempting to create app (approval size 279, hash MND3Z7333YKVSRZGAYNW4GOPSPCQSIQRALCSP3SJW7TH7FEJUBBQ; clear size 51, hash 7BF7UDFEXCBEQJRMELOWO5DL3W3KLDZCVQ7EIYAWJ7PIRRCCEKVQ)
Issued transaction from account CPOZRLW5POOJOAMYRD6W6YXD4FOEYUP45NHMHOPCHOIWZEOKDU6VGKUALA, txid WAL6AQ2ZDZJ45RH7LUVOQKZWP3MVEWCUNRZV3FVV5WMAZLYG4NIQ (fee 1000)
Transaction WAL6AQ2ZDZJ45RH7LUVOQKZWP3MVEWCUNRZV3FVV5WMAZLYG4NIQ still pending as of round 10680195
Transaction WAL6AQ2ZDZJ45RH7LUVOQKZWP3MVEWCUNRZV3FVV5WMAZLYG4NIQ committed in round 10680197
Created app with app index 13203524
```

This is the code written in PyTeal that handles the creation of the smart contract:

```
    on_creation = Seq([
        App.globalPut(Bytes("Creator"), Txn.sender()),
        Assert(Txn.application_args.length() == Int(4)),
        App.globalPut(Bytes("RegBegin"), Btoi(Txn.application_args[0])),
        App.globalPut(Bytes("RegEnd"), Btoi(Txn.application_args[1])),
        App.globalPut(Bytes("VoteBegin"), Btoi(Txn.application_args[2])),
        App.globalPut(Bytes("VoteEnd"), Btoi(Txn.application_args[3])),
        Return(Int(1))
    ])
```

### Register to vote

If a user wants to vote, he must be opt in to the account. This operation, according to the contract logic, is allowed only into a specific round range.

```
goal app optin --app-id 13203524 --from PKKZSQH5VQY2MB7HWL2KF6C4M2N42URIEFSLZUFV2UZBMHR5FEQDMLTXRE

Issued transaction from account PKKZSQH5VQY2MB7HWL2KF6C4M2N42URIEFSLZUFV2UZBMHR5FEQDMLTXRE, txid ZO5ZGC2RAOGKQL62673WQGU6SLFE3GPFBSP3CQ6B2NJUXDTC2MSQ (fee 1000)
Transaction ZO5ZGC2RAOGKQL62673WQGU6SLFE3GPFBSP3CQ6B2NJUXDTC2MSQ still pending as of round 10680242
Transaction ZO5ZGC2RAOGKQL62673WQGU6SLFE3GPFBSP3CQ6B2NJUXDTC2MSQ committed in round 10680244
```

The following code handles the opt in:

```
on_register = Return(And(
        Global.round() >= App.globalGet(Bytes("RegBegin")),
        Global.round() <= App.globalGet(Bytes("RegEnd"))
    ))
```

### Vote

Once the user has opted in, he is allowed to vote. The user can vote only once, and the vote is allowed only in a specific round range. The choice is saved both in the global state and in the user local state.

```
goal app call --app-id 13203524 --from PKKZSQH5VQY2MB7HWL2KF6C4M2N42URIEFSLZUFV2UZBMHR5FEQDMLTXRE --app-arg "str:vote" --app-arg "str:candidateA" 

Issued transaction from account PKKZSQH5VQY2MB7HWL2KF6C4M2N42URIEFSLZUFV2UZBMHR5FEQDMLTXRE, txid 4ZMDCPDC5ZKXUVDPNQ4ANTJK2FODZVJTFWZUNXY7KFQYU4DJ4RNA (fee 1000)
Transaction 4ZMDCPDC5ZKXUVDPNQ4ANTJK2FODZVJTFWZUNXY7KFQYU4DJ4RNA still pending as of round 10680441
Transaction 4ZMDCPDC5ZKXUVDPNQ4ANTJK2FODZVJTFWZUNXY7KFQYU4DJ4RNA committed in round 10680443
```

We can see the vote both in the global and in the user local state:

```
goal app read --global --app-id 13203524

{
    .
    .
    .
  "candidateA": {
    "tt": 2,
    "ui": 1
  }
}


goal app read --local --app-id 13203524 --from PKKZSQH5VQY2MB7HWL2KF6C4M2N42URIEFSLZUFV2UZBMHR5FEQDMLTXRE

{
  "voted": {
    "tb": "candidateA",
    "tt": 1
  }
}
```

Here is the code that handles the voting:

```
get_vote_of_sender = App.localGetEx(Int(0), App.id(), Bytes("voted"))

choice = Txn.application_args[1]
choice_tally = App.globalGet(choice)

on_vote = Seq([
        Assert(And(
            Global.round() >= App.globalGet(Bytes("VoteBegin")),
            Global.round() <= App.globalGet(Bytes("VoteEnd"))
        )),
        Assert(App.optedIn(Int(0), Txn.application_id())),
        get_vote_of_sender,
        If(get_vote_of_sender.hasValue(), 
            Return(Int(0))
        ),
        App.globalPut(choice, choice_tally + Int(1)),
        App.localPut(Int(0), Bytes("voted"), choice),
        Return(Int(1))
    ])
```

### Closeout

If a voter decides to closeout before the end of the voting, and he has already voted, the user vote will be removed.

```
goal app closeout --app-id 13203524 --from PKKZSQH5VQY2MB7HWL2KF6C4M2N42URIEFSLZUFV2UZBMHR5FEQDMLTXRE

Issued transaction from account PKKZSQH5VQY2MB7HWL2KF6C4M2N42URIEFSLZUFV2UZBMHR5FEQDMLTXRE, txid ES52DZUOGMTSK66U3BDJ3GZOWCSLUQTFPZP4KGCLYBHPEVJM2BYA (fee 1000)
Transaction ES52DZUOGMTSK66U3BDJ3GZOWCSLUQTFPZP4KGCLYBHPEVJM2BYA still pending as of round 10680564
Transaction ES52DZUOGMTSK66U3BDJ3GZOWCSLUQTFPZP4KGCLYBHPEVJM2BYA committed in round 10680566
```

We can see the change in the global state:

```
goal app read --global --app-id 13203524

{
    .
    .
    .
"candidateA": {
    "tt": 2
  }
}
```