from pyteal import *

def approval_program():
    on_creation = Seq([
        App.globalPut(Bytes("Creator"), Txn.sender()),
        Assert(Txn.application_args.length() == Int(4)),
        App.globalPut(Bytes("N"), Int(3)),
        App.globalPut(Bytes("V"), Btoi(Txn.application_args[0])),
        App.globalPut(Bytes("D0"), Btoi(Txn.application_args[1])),
        App.globalPut(Bytes("D1"), Btoi(Txn.application_args[2])),
        App.globalPut(Bytes("D2"), Btoi(Txn.application_args[3])),
        App.globalPut(Bytes("Join"), Int(3)),
        App.globalPut(Bytes("Reveal"), Int(3)),
        App.globalPut(Bytes("Count_id"), Int(3)),
        Return(Int(1))
    ])

    is_creator = Txn.sender() == App.globalGet(Bytes("Creator"))

    d0 = App.globalGet(Bytes("D0"))

    on_update = Seq([
        If(And(is_creator, Global.round() <= d0),
            Seq([
                App.globalPut(Bytes("Stateless_app"), Txn.application_args[0]),
                Return(Int(1))
            ])
        ),
        Return(Int(0))
    ])

    count_id = App.globalGet(Bytes("Count_id"))

    on_optin = If(And(count_id > Int(0), Global.round() <= d0),
        Seq([
            App.globalPut(Bytes("Count_id"), count_id - Int(1)),
            App.localPut(Int(0), Bytes("Id"), count_id),
            App.localPut(Int(0), Bytes("Hash"), Bytes("")),
            Return(Int(1))
        ]),
        Return(Int(0))
    )

    s = Txn.application_args[1]
    h = Sha256(s)
    N = App.globalGet(Bytes("N"))
    V = App.globalGet(Bytes("V"))
    join = App.globalGet(Bytes("Join"))

    check_group_1 = And(
        Global.group_size() == Int(2),
        Gtxn[1].type_enum() == TxnType.Payment,
        Gtxn[1].sender() == Txn.sender(),
        Gtxn[1].receiver() == App.globalGet(Bytes("Stateless_app")),
        Gtxn[1].amount() == ((Int(1) + ((N * (N - Int(1))) * V)) + Int(500000))
    )

    id = App.localGet(Int(0), Bytes("Id"))
    
    addit_account_hash_1 = App.localGetEx(Int(1), App.id(), Bytes("Hash"))
    addit_account_id_1 = App.localGetEx(Int(1), App.id(), Bytes("Id"))
    addit_account_hash_2 = App.localGetEx(Int(2), App.id(), Bytes("Hash"))
    addit_account_id_2 = App.localGetEx(Int(2), App.id(), Bytes("Id"))

    check_id = And(
        id != addit_account_id_1.value(), 
        id != addit_account_id_2.value(),
    )

    check_hash = And(
        h != addit_account_hash_1.value(), 
        h != addit_account_hash_2.value(),
    )

    on_commit = Seq([
        addit_account_id_1,
        addit_account_id_2,
        addit_account_hash_1,
        addit_account_hash_2,
        If(And(Global.round() <= d0, 
            check_id,
            check_hash, 
            check_group_1),
            Seq([
                App.globalPut(Bytes("Join"), join - Int(1)),
                App.localPut(Int(0), Bytes("Hash"), h),
                Return(Int(1))
            ])         
        ),
        Return(Int(0))
    ])

    check_group_2 = And(
        Gtxn[1].type_enum() == TxnType.Payment,
        Gtxn[1].sender() == App.globalGet(Bytes("Stateless_app")),
        Gtxn[1].receiver() == Txn.sender(),
        Gtxn[1].amount() == (Int(1) + ((N * (N - Int(1))) * V)),
    )

    on_retrieve_after_commit = Return(And(join > Int(0), Global.round() > d0, check_group_2))   # check_group da definire

    d1 = App.globalGet(Bytes("D1"))
    reveal = App.globalGet(Bytes("Reveal"))
    w_tmp = App.globalGet(Bytes("W_tmp"))

    on_reveal = Seq([
        If(And(Global.round() > d0, join == Int(0), Global.round() <= d1, h == App.localGet(Int(0), Bytes("Hash"))),
            Seq([
                App.globalPut(Bytes("Reveal"), reveal - Int(1)),
                App.localPut(Int(0), Bytes("Revealed"), Int(1)),
                App.globalPut(Bytes("W_tmp"), w_tmp + Btoi(s)),
                Return(Int(1))
            ])),   
        Return(Int(0))
    ])

    check_revealed = App.localGetEx(Int(0), App.id(), Bytes("Revealed"))

    check_group_3 = And(
        Global.group_size() == Int(2),
        Gtxn[1].type_enum() == TxnType.Payment,
        Gtxn[1].sender() == App.globalGet(Bytes("Stateless_app")),
        Gtxn[1].receiver() == Txn.sender(),
        Gtxn[1].amount() == (N * V),
    )

    d2 = App.globalGet(Bytes("D2"))

    on_retrieve_after_reveal = Seq([
        check_revealed,
        Return(And(Global.round() > d1, Global.round() <= d2, reveal > Int(0), check_revealed.hasValue(), check_group_3))
    ])

    id = App.localGet(Int(0), Bytes("Id"))

    on_winner = Return(And(Global.round() > d1, Global.round() <= d2, reveal == Int(0), id == (w_tmp % N), check_group_3))

    check_group_4 = And(
        Global.round() > d1,
        Global.group_size() == Int(2),
        Gtxn[1].type_enum() == TxnType.Payment,
        Gtxn[1].sender() == App.globalGet(Bytes("Stateless_app")),
        Gtxn[1].receiver() == Txn.sender(),
        Gtxn[1].close_remainder_to() == Txn.sender(),
        Gtxn[1].amount() == Int(0),
    )

    on_delete = Return(And(is_creator, check_group_4, Global.round() > d2))

    program = Cond(
        [Txn.application_id() == Int(0), on_creation],
        [Txn.on_completion() == OnComplete.DeleteApplication, on_delete],
        [Txn.on_completion() == OnComplete.UpdateApplication, on_update],
        [Txn.on_completion() == OnComplete.CloseOut, Return(Int(1))],
        [Txn.on_completion() == OnComplete.OptIn, on_optin],
        [Txn.application_args[0] == Bytes("commit"), on_commit],
        [Txn.application_args[0] == Bytes("retrieve_after_commit"), on_retrieve_after_commit],
        [Txn.application_args[0] == Bytes("reveal"), on_reveal],
        [Txn.application_args[0] == Bytes("retrieve_after_reveal"), on_retrieve_after_reveal],
        [Txn.application_args[0] == Bytes("winner"), on_winner],
    )

    return program

def lottery_fund():
    program = Return(
        And(
            Global.group_size() == Int(2), 
            Gtxn[0].type_enum() == TxnType.ApplicationCall,
            Gtxn[0].application_id() == Int(13257393),
            Gtxn[0].rekey_to() == Global.zero_address(),
            Txn.rekey_to() == Global.zero_address()
        ))

    return program

def clear_state_program(): 
    program = Return(Int(1))

    return program

with open('lottery_approval.teal', 'w') as f:
    compiled = compileTeal(approval_program(), Mode.Application)
    f.write(compiled)

with open('lottery_clear_state.teal', 'w') as f:
    compiled = compileTeal(clear_state_program(), Mode.Application)
    f.write(compiled)

with open('lottery_fund.teal', 'w') as f:
    compiled = compileTeal(lottery_fund(), Mode.Application)
    f.write(compiled)
    