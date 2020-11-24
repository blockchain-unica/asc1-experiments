## Permissioned voting

We wrote the code of the permissioned voting in Pyteal version, starting from the [permissionless example](https://developer.algorand.org/articles/creating-stateful-algorand-smart-contracts-python-pyteal/)

The logic of this contract is fully explained [here](https://developer.algorand.org/solutions/example-permissioned-voting-stateful-smart-contract-application/).

To build this contract we have to handle this 5 parts:
- Create asset
- Create the voting smart contract
- Register to vote
- Vote
- Closeout

### Create asset

First of all, we need to create an asset to handle and decide which account is able to vote.

We have the following accounts:

```
goal account list

CPOZRLW5POOJOAMYRD6W6YXD4FOEYUP45NHMHOPCHOIWZEOKDU6VGKUALA	100000000 microAlgos
PKKZSQH5VQY2MB7HWL2KF6C4M2N42URIEFSLZUFV2UZBMHR5FEQDMLTXRE	100000000 microAlgos
```

We must create an asset:
```
goal asset create --creator CPOZRLW5POOJOAMYRD6W6YXD4FOEYUP45NHMHOPCHOIWZEOKDU6VGKUALA --total 1000 --unitname votetkn --decimals 0   

Issued transaction from account CPOZRLW5POOJOAMYRD6W6YXD4FOEYUP45NHMHOPCHOIWZEOKDU6VGKUALA, txid IYGEKP7D2HZSA73VHKLPPW73UJHSUYHNPEXYEJ7PYHXKKCBTPYKA (fee 1000)
Transaction IYGEKP7D2HZSA73VHKLPPW73UJHSUYHNPEXYEJ7PYHXKKCBTPYKA still pending as of round 10525734
Transaction IYGEKP7D2HZSA73VHKLPPW73UJHSUYHNPEXYEJ7PYHXKKCBTPYKA committed in round 10525736
Created asset with asset index 13138879

```

Then, we have to opt in the voter into the voting token, and send the voting token to the voter

```
goal asset send -a 0 -f PKKZSQH5VQY2MB7HWL2KF6C4M2N42URIEFSLZUFV2UZBMHR5FEQDMLTXRE -t PKKZSQH5VQY2MB7HWL2KF6C4M2N42URIEFSLZUFV2UZBMHR5FEQDMLTXRE --creator CPOZRLW5POOJOAMYRD6W6YXD4FOEYUP45NHMHOPCHOIWZEOKDU6VGKUALA --assetid 13138879 

Issued transaction from account PKKZSQH5VQY2MB7HWL2KF6C4M2N42URIEFSLZUFV2UZBMHR5FEQDMLTXRE, txid BD4CJC3Z3TNKYVERG3K6DGSOS7OBMDEURBA4TIU7QM4JQOCKR4YA (fee 1000)
Transaction BD4CJC3Z3TNKYVERG3K6DGSOS7OBMDEURBA4TIU7QM4JQOCKR4YA still pending as of round 10525765
Transaction BD4CJC3Z3TNKYVERG3K6DGSOS7OBMDEURBA4TIU7QM4JQOCKR4YA committed in round 10525767


goal asset send -a 1 -f CPOZRLW5POOJOAMYRD6W6YXD4FOEYUP45NHMHOPCHOIWZEOKDU6VGKUALA -t PKKZSQH5VQY2MB7HWL2KF6C4M2N42URIEFSLZUFV2UZBMHR5FEQDMLTXRE --creator CPOZRLW5POOJOAMYRD6W6YXD4FOEYUP45NHMHOPCHOIWZEOKDU6VGKUALA --assetid 13138879

Issued transaction from account CPOZRLW5POOJOAMYRD6W6YXD4FOEYUP45NHMHOPCHOIWZEOKDU6VGKUALA, txid NKV6DRZWHGRNVMUPPO235NJRUOQWU7Y2VOIOYVE2IGEOQWELVZSQ (fee 1000)
Transaction NKV6DRZWHGRNVMUPPO235NJRUOQWU7Y2VOIOYVE2IGEOQWELVZSQ still pending as of round 10538895
Transaction NKV6DRZWHGRNVMUPPO235NJRUOQWU7Y2VOIOYVE2IGEOQWELVZSQ committed in round 10538897

```
### Create the voting smart contract

We have to create the voting smart contract. 

This is the code written in PyTeal that handles the voting:

```
from pyteal import *

def approval_program():
    on_creation = Seq([
        App.globalPut(Bytes("Creator"), Txn.sender()),
        Assert(Txn.application_args.length() == Int(5)),
        App.globalPut(Bytes("RegBegin"), Btoi(Txn.application_args[0])),
        App.globalPut(Bytes("RegEnd"), Btoi(Txn.application_args[1])),
        App.globalPut(Bytes("VoteBegin"), Btoi(Txn.application_args[2])),
        App.globalPut(Bytes("VoteEnd"), Btoi(Txn.application_args[3])),
        App.globalPut(Bytes("AssetId"), Btoi(Txn.application_args[4])),
        Return(Int(1))
    ])

    is_creator = Txn.sender() == App.globalGet(Bytes("Creator"))

    get_vote_of_sender = App.localGetEx(Int(0), App.id(), Bytes("voted"))

    asset_balance = AssetHolding.balance(Int(0), App.globalGet(Bytes("AssetId")))

    on_closeout = Seq([
        get_vote_of_sender,
        If(And(Global.round() <= App.globalGet(Bytes("VoteEnd")), get_vote_of_sender.hasValue()),
            App.globalPut(get_vote_of_sender.value(), App.globalGet(get_vote_of_sender.value()) - Int(1))
        ),
        Return(Int(1))
    ])

    on_register = Return(And(
        Global.round() >= App.globalGet(Bytes("RegBegin")),
        Global.round() <= App.globalGet(Bytes("RegEnd"))
    ))

    choice = Txn.application_args[1]
    choice_tally = App.globalGet(choice)

    check_group = And(
        asset_balance.value() >= Int(1),
        Global.group_size() == Int(2),
        Gtxn[1].type_enum() == TxnType.AssetTransfer,
        Gtxn[1].xfer_asset() == App.globalGet(Bytes("AssetId")),
        Gtxn[1].asset_receiver() == App.globalGet(Bytes("Creator")),
        Gtxn[1].asset_amount() == Int(1)
    )

    on_vote = Seq([
        Assert(And(
            Global.round() >= App.globalGet(Bytes("VoteBegin")),
            Global.round() <= App.globalGet(Bytes("VoteEnd"))
        )),
        Assert(App.optedIn(Int(0), Txn.application_id())),
        asset_balance,
        If(check_group, 
            Seq([
                If(get_vote_of_sender.hasValue(), 
                    Return(Int(0))
                ),
                If(Or(choice == Bytes("candidateA"), choice == Bytes("candidateB")), 
                    Seq([
                        App.globalPut(choice, choice_tally + Int(1)),
                        App.localPut(Int(0), Bytes("voted"), choice),
                        Return(Int(1))]), 
                    Return(Int(0)))
            ]),
            Return(Int(0))
        )
    ])

    program = Cond(
        [Txn.application_id() == Int(0), on_creation],
        [Txn.on_completion() == OnComplete.DeleteApplication, Return(is_creator)],
        [Txn.on_completion() == OnComplete.UpdateApplication, Return(is_creator)],
        [Txn.on_completion() == OnComplete.CloseOut, on_closeout],
        [Txn.on_completion() == OnComplete.OptIn, on_register],
        [Txn.application_args[0] == Bytes("vote"), on_vote]
    )

    return program

def clear_state_program():
    get_vote_of_sender = App.localGetEx(Int(0), App.id(), Bytes("voted"))
    program = Seq([
        get_vote_of_sender,
        If(And(Global.round() <= App.globalGet(Bytes("VoteEnd")), get_vote_of_sender.hasValue()),
            App.globalPut(get_vote_of_sender.value(), App.globalGet(get_vote_of_sender.value()) - Int(1))
        ),
        Return(Int(1))
    ])

    return program

with open('vote_approval.teal', 'w') as f:
    compiled = compileTeal(approval_program(), Mode.Application)
    f.write(compiled)

with open('vote_clear_state.teal', 'w') as f:
    compiled = compileTeal(clear_state_program(), Mode.Application)
    f.write(compiled)
```

The arguments represent the round range for registering and voting, and the asset id. In the creation call we also need to set up the amount of space that this contract will use. 

```
goal app create --creator CPOZRLW5POOJOAMYRD6W6YXD4FOEYUP45NHMHOPCHOIWZEOKDU6VGKUALA --approval-prog ./vote_approval.teal --global-byteslices 1 --global-ints 6 --local-byteslices 1 --local-ints 0 --app-arg "int:10000000" --app-arg "int:10550000" --app-arg "int:10000000" --app-arg "int:10550000" --app-arg "int:13138879" --clear-prog ./vote_clear_state.teal 

Attempting to create app (approval size 383, hash TXE2CB76B2DVBB4D3VIJLW4CN2CTOWLSIA2ZHD2PB64HQWZQK25A; clear size 51, hash 7BF7UDFEXCBEQJRMELOWO5DL3W3KLDZCVQ7EIYAWJ7PIRRCCEKVQ)
Issued transaction from account CPOZRLW5POOJOAMYRD6W6YXD4FOEYUP45NHMHOPCHOIWZEOKDU6VGKUALA, txid ERXMWOXJBTPUXNPNB2EHDBAAQ2AV75SRSQBPFSCYW62QVPXPDTKQ (fee 1000)
Transaction ERXMWOXJBTPUXNPNB2EHDBAAQ2AV75SRSQBPFSCYW62QVPXPDTKQ still pending as of round 10538905
Transaction ERXMWOXJBTPUXNPNB2EHDBAAQ2AV75SRSQBPFSCYW62QVPXPDTKQ committed in round 10538907
Created app with app index 13159860
```

### Register to vote

Voters must be optin to the contract. This because the contract need to writes the vote into the voter local state.

```
goal app optin --app-id 13159860 --from PKKZSQH5VQY2MB7HWL2KF6C4M2N42URIEFSLZUFV2UZBMHR5FEQDMLTXRE 

Issued transaction from account PKKZSQH5VQY2MB7HWL2KF6C4M2N42URIEFSLZUFV2UZBMHR5FEQDMLTXRE, txid L75BIK47PW372FXUAIXWYZ5O2EVN7HFMRLS2P56VBB42ZV5IHCKQ (fee 1000)
Transaction L75BIK47PW372FXUAIXWYZ5O2EVN7HFMRLS2P56VBB42ZV5IHCKQ still pending as of round 10538915
Transaction L75BIK47PW372FXUAIXWYZ5O2EVN7HFMRLS2P56VBB42ZV5IHCKQ committed in round 10538917
```

### Vote

If users want to vote, they must create two transaction:
- A transactionCall to the contract
- A transaction that sends the token value to the central authority

The vote is admitted only if the current range belongs to the range specified at the contract creation. The user is obliged to choose a candidate between "candidateA" and "candidateB".
 
So, we need to create two transactions that must be grouped and signed before sending them.

```
goal app call --app-id 13159860 --app-arg "str:vote" --app-arg "str:candidateA" --from PKKZSQH5VQY2MB7HWL2KF6C4M2N42URIEFSLZUFV2UZBMHR5FEQDMLTXRE --out=txn1.tx

goal asset send --from PKKZSQH5VQY2MB7HWL2KF6C4M2N42URIEFSLZUFV2UZBMHR5FEQDMLTXRE --to CPOZRLW5POOJOAMYRD6W6YXD4FOEYUP45NHMHOPCHOIWZEOKDU6VGKUALA --creator CPOZRLW5POOJOAMYRD6W6YXD4FOEYUP45NHMHOPCHOIWZEOKDU6VGKUALA --assetid 13138879 --fee 1000 --amount 1 --out=txn2.tx

cat txn1.tx txn2.tx > txn.tx

goal clerk group -i txn.tx -o groupedtxn.tx
goal clerk sign -i groupedtxn.tx -o signedtxn.tx
goal clerk rawsend -f signedtxn.tx

Raw transaction ID IYIQKPKD54XPA5RD36LENBLTPOUV4WL6CSDK2SZGU7LDOQH6LESA issued
Raw transaction ID 45BJH5EPEQ56RS75FCIAVZPDLIROYNPI5OZV3NYMXTO4XDIWEMFA issued
Transaction IYIQKPKD54XPA5RD36LENBLTPOUV4WL6CSDK2SZGU7LDOQH6LESA still pending as of round 10538939
Transaction IYIQKPKD54XPA5RD36LENBLTPOUV4WL6CSDK2SZGU7LDOQH6LESA committed in round 10538941
Transaction 45BJH5EPEQ56RS75FCIAVZPDLIROYNPI5OZV3NYMXTO4XDIWEMFA committed in round 10538941
```

We can check how the global and local state has been modified. In fact, we can see that in the global state we have the current vote for candidateA, and in the local state we can see that the address PKKZ.. has just voted.

```
goal app read --global --app-id 13159860

{
  .
  .
  .
  "candidateA": {
    "tt": 2,
    "ui": 1
  }
}


goal app read --local --from PKKZSQH5VQY2MB7HWL2KF6C4M2N42URIEFSLZUFV2UZBMHR5FEQDMLTXRE --app-id 13159860

{
  "voted": {
    "tb": "candidateA",
    "tt": 1
  }
}
```
### Closeout

If the voter decided to closeout before the end of the voting, his vote must be removed. 

```
goal app closeout --from PKKZSQH5VQY2MB7HWL2KF6C4M2N42URIEFSLZUFV2UZBMHR5FEQDMLTXRE --app-id 13159860

Issued transaction from account PKKZSQH5VQY2MB7HWL2KF6C4M2N42URIEFSLZUFV2UZBMHR5FEQDMLTXRE, txid QBDHBR3T6QWA5OOGWPDJJHTLABJFDLZF2MJKONCMRRQKBPP77NWQ (fee 1000)
Transaction QBDHBR3T6QWA5OOGWPDJJHTLABJFDLZF2MJKONCMRRQKBPP77NWQ still pending as of round 10539167
Transaction QBDHBR3T6QWA5OOGWPDJJHTLABJFDLZF2MJKONCMRRQKBPP77NWQ committed in round 10539169
```