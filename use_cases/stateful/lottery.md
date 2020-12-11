## Multi-player lottery

The implementation of the Multi-player lottery written in PyTeal is reported [here](./lottery.py).
This version of the multi-player lottery is composed by 3 main phases:

- Phase 1: Commit
- Phase 2: Reveal
- Phase 3: Winner

In the first phase (Commit) every player join to the contract choosing an hashed secret and sending 1 + N(N-1)*V to a fund associated to the contract. V indicates a certain amount of ALGOs. The contract must verify if the hashed secret is different to the other hashed secrets sent by the other players. If some player does not commit to the contract in D0, the other players can retrieve the sent money. Otherwise, the player is allowed to continue with the second phase.

In the second phase (Reveal) every player must reveal the secret in D1, sending a secret whose hash is the same as the hash sent previously. If some player does not reveal its own secret, every other player can retrieve N * V from the fund. Otherwise, the player can continue with the third phase.

In the third phase (Winner) the winner is determined with the sum of all the secrets modulo N. This value indicates the id associated to the winner that can retrieve N*V from the fund. After D2 the creator of the contract can delete the contract and can retrieve the remaining money from the fund.

When we create the contract, we must handle the following cases:

- Create contract
- Create fund
- Update stateful contract
- Phase 1: Commit
- Phase 1a: Retrieve after commit
- Phase 2: Reveal
- Phase 2a: Retrieve after reveal
- Phase 3: Winner
- Delete

### Create contract

We have the following accounts:
```
GTSPG2JKER33WYCFEMRQ56ARWHKIOK554ZAMQI7OODW3YGSW4M3VWW4E4M      48868991 microAlgos     
UFN3PEU4NHD7F6WUJSR6JJWWPYN7O27IWCJ5HQYCSPBQP2CXJJHETUMJRY      22929987 microAlgos
ZYLICUCADSRXKBEKPDMGBHWOWPHS6TVPJIGTDENHY4HPD4RUFKZYE2Z4IY      60952993 microAlgos 
```

First of all, we must create the contract. This contract works with 3 players. To create it we must indicate V (as mentioned above it describes a constant amount of ALGOs), D0, D1 and D2 (expressed as number of rounds). Moreover, we must indicate the number of global byteslices, global ints, local byteslices and local ints.

```
goal app create --creator GTSPG2JKER33WYCFEMRQ56ARWHKIOK554ZAMQI7OODW3YGSW4M3VWW4E4M --approval-prog ./lottery_approval.teal --global-byteslices 2 --global-ints 9 --local-byteslices 1 --local-ints 2 --app-arg "int:$V" --app-arg "int:$D0" --app-arg "int:$D1" --app-arg "int:$D2" --clear-prog ./lottery_clear_state.teal
```

Once the contract is created, an ID will be released. In this example the app id is 13273865.

### Create fund

To create the fund, implemented as a stateless contract, firstly we need to update the app id into the stateless contract. Then, we can create the stateless contract executing the following command:
```
goal clerk compile lottery_fund.teal
```
Once the fund has been loaded into the network, an address will be released. In this example the address is QIOE2Z3Z3DELLJPG4NRICKWHOWL4ANN6M4ICXCR5VVU65QJIX7674TL4DA

### Update stateful contract

The update is necessary because we need to insert the reference to the fund into the stateful contract:

```
goal app update --from GTSPG2JKER33WYCFEMRQ56ARWHKIOK554ZAMQI7OODW3YGSW4M3VWW4E4M --app-id 13273865 --app-arg addr:QIOE2Z3Z3DELLJPG4NRICKWHOWL4ANN6M4ICXCR5VVU65QJIX7674TL4DA --approval-prog ./lottery_approval.teal --clear-prog ./lottery_clear_state.teal
```

### Phase 1: Commit

First of all every N player has to opt in to the stateful contract:
```
goal app optin --from GTSPG2JKER33WYCFEMRQ56ARWHKIOK554ZAMQI7OODW3YGSW4M3VWW4E4M --app-id 13273865

goal app optin --from UFN3PEU4NHD7F6WUJSR6JJWWPYN7O27IWCJ5HQYCSPBQP2CXJJHETUMJRY --app-id 13273865

goal app optin --from ZYLICUCADSRXKBEKPDMGBHWOWPHS6TVPJIGTDENHY4HPD4RUFKZYE2Z4IY --app-id 13273865
```

Every N player has to commit to the stateful smart contract:
- a secret (that will be hashed by the contract with SHA256)
- a specific amount: 1+(N*((N-1)*V)). 

Indeed, every player has to add a fee to handle the fund. In this case every player will add 500000 as fee. 
If the hashed secret is equal to the hash of another player, the transaction will be rejected.
The application call and the transaction who sends ALGOs to the fund must be grouped.

```
goal app call --from GTSPG2JKER33WYCFEMRQ56ARWHKIOK554ZAMQI7OODW3YGSW4M3VWW4E4M --app-id 13273865 --app-arg str:commit --app-arg int:52 --app-account UFN3PEU4NHD7F6WUJSR6JJWWPYN7O27IWCJ5HQYCSPBQP2CXJJHETUMJRY --app-account ZYLICUCADSRXKBEKPDMGBHWOWPHS6TVPJIGTDENHY4HPD4RUFKZYE2Z4IY --out=unsignedtransaction1.tx

goal clerk send --from=GTSPG2JKER33WYCFEMRQ56ARWHKIOK554ZAMQI7OODW3YGSW4M3VWW4E4M --to=QIOE2Z3Z3DELLJPG4NRICKWHOWL4ANN6M4ICXCR5VVU65QJIX7674TL4DA --amount=6500001 --fee=1000 --out=unsignedtransaction2.tx

cat unsignedtransaction1.tx unsignedtransaction2.tx > combinedtransactions.tx

goal clerk group -i combinedtransactions.tx -o groupedtransactions.tx

goal clerk sign -i groupedtransactions.tx -o signout.tx

goal clerk rawsend -f signout.tx
```

This operation must be repeated for every N player.

### Phase 1a: Retrieve after commit

If after D0 there is at least one player who did not commit the secret to the contract, every other player can retrieve the money sent (1 + (N * ((N-1) * V))).

Every user must create a transaction group in which the first transaction is the application call and the second transaction in the transaction who sends the money from the fund to the player.

```
goal app call --from GTSPG2JKER33WYCFEMRQ56ARWHKIOK554ZAMQI7OODW3YGSW4M3VWW4E4M --app-id 13273865 --app-arg "str:retrieve_after_commit" --out=unsignedtransaction1.tx

goal clerk send --from-program ./lottery_fund.teal --to=GTSPG2JKER33WYCFEMRQ56ARWHKIOK554ZAMQI7OODW3YGSW4M3VWW4E4M --amount=6000001 --fee=1000 --out=unsignedtransaction2.tx

cat unsignedtransaction1.tx unsignedtransaction2.tx > combinedtransactions.tx

goal clerk group -i combinedtransactions.tx -o groupedtransactions.tx

goal clerk split -i groupedtransactions.tx -o split.tx 

goal clerk sign -i split-0.tx -o signout-0.tx

cat signout-0.tx split-1.tx > signout.tx

goal clerk rawsend -f signout.tx
```

### Phase 2: Reveal

If after D0 every N player has committed the secret to the contract, we can proceed with the phase 2. 

Every player must reveal its own secret.

This is an example with the first address.
```
goal app call --from GTSPG2JKER33WYCFEMRQ56ARWHKIOK554ZAMQI7OODW3YGSW4M3VWW4E4M --app-id 13273865 --app-arg str:reveal --app-arg int:52 --out=unsignedtransaction1.tx

goal clerk sign -i unsignedtransaction1.tx -o unsignedtransaction1.tx

goal clerk rawsend -f unsignedtransaction1.tx
```

If someone does not reveal its secret, after D1 we can proceed with the phase 2a. Otherwise, we can proceed with the phase 3 (Winner).

### Phase 2a: Retrieve after reveal

If after D1 there is at least one player who did not reveal his secret, every other player can retrieve N * V money from the fund. To do so, every player must create a transaction group in which the first one is a application call to the contract, and the second one is the transaction who sends money from the found to the player.

This is an example with the first player. Obviously, the same operation must be repeated for every player who committed the secret to the contract:

```
goal app call --from GTSPG2JKER33WYCFEMRQ56ARWHKIOK554ZAMQI7OODW3YGSW4M3VWW4E4M --app-id 13273865 --app-arg "str:retrieve_after_reveal" --out=unsignedtransaction1.tx

goal clerk send --from-program ./lottery_fund.teal --to=GTSPG2JKER33WYCFEMRQ56ARWHKIOK554ZAMQI7OODW3YGSW4M3VWW4E4M --amount= --fee=3000000 --out=unsignedtransaction2.tx

cat unsignedtransaction1.tx unsignedtransaction2.tx > combinedtransactions.tx

goal clerk group -i combinedtransactions.tx -o groupedtransactions.tx

goal clerk split -i groupedtransactions.tx -o split.tx 

goal clerk sign -i split-0.tx -o signout-0.tx

cat signout-0.tx split-1.tx > signout.tx

goal clerk rawsend -f signout.tx
```

### Phase 3: Winner

Once every N player has revealed his secret, a winner must be chosen. To do so, the id associated to the winner is calculated by the sum of all the revealed secrets modulo N.

The winner will retrieve N * V from the fund.

To get the winner, a transaction call to the contract and a transaction who sends N * V ALGOs from the fund to the contract must be grouped in a group transaction that will be sent to the network. The user whose transaction group will not be rejected, will be the winner.

```
goal app call --from GTSPG2JKER33WYCFEMRQ56ARWHKIOK554ZAMQI7OODW3YGSW4M3VWW4E4M --app-id 13273865 --app-arg str:winner --out=unsignedtransaction1.tx

goal clerk send --to=GTSPG2JKER33WYCFEMRQ56ARWHKIOK554ZAMQI7OODW3YGSW4M3VWW4E4M --amount=3000000 --from-program ./lottery_fund.teal --out=unsignedtransaction2.tx

cat unsignedtransaction1.tx unsignedtransaction2.tx > combinedtransaction.tx

goal clerk group -i combinedtransactions.tx -o groupedtransactions.tx

goal clerk split -i groupedtransactions.tx -o split.tx

goal clerk sign -i split-0.tx -o signout-0.tx

cat signout-0.tx split-1.tx > signout.tx

goal clerk rawsend -f signout.tx
```

### Delete

After D2, the creator of the contract can delete the contract and retrieve the remaining money from the fund:

```
goal app delete --from GTSPG2JKER33WYCFEMRQ56ARWHKIOK554ZAMQI7OODW3YGSW4M3VWW4E4M --app-id 13273865 --out=unsignedtransaction1.tx

goal clerk send --from-program ./lottery_fund.teal --to=GTSPG2JKER33WYCFEMRQ56ARWHKIOK554ZAMQI7OODW3YGSW4M3VWW4E4M -c GTSPG2JKER33WYCFEMRQ56ARWHKIOK554ZAMQI7OODW3YGSW4M3VWW4E4M --amount=0 --fee=1000 --out=unsignedtransaction2.tx

cat unsignedtransaction1.tx unsignedtransaction2.tx > combinedtransactions.tx

goal clerk group -i combinedtransactions.tx -o groupedtransactions.tx

goal clerk split -i groupedtransactions.tx -o split.tx 

goal clerk sign -i split-0.tx -o signout-0.tx

cat signout-0.tx split-1.tx > signout.tx

goal clerk rawsend -f signout.tx
```