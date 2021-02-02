## Accounts and contracts

### Context

In these experiments, we checked some behaviour of corner cases related to the accounts and the contracts. In particular, we pay more attention to these following aspects:
- Minimum balance requirement for a smart contract
- Maximum number of accounts which can opt in to the contract

Infer the Algorand behaviour in these corner cases is important especially for security. For example, we can suppose that an attacker wants to take advantage of the possibility to opt in a lot of accounts in a contract trying to made a Sybil attack. We know that Algorand is permissionless, so the attacker can create as many accounts as he wants. But at the same time, the attacker has to know:
- How many micro-Algos any account must have to opt in to the contract
- How many accounts he can opt in to the contract

For this reason, it is important to analyse the corner cases mentioned above. For the experiments [this code](./example_stateful_contract.md) has been used.

### Minimum balance requirement for a smart contract
The stateful smart contract overview mentions that there is a minimum amount of Algos that every user must have for the creation and the opt in to the contract. So, we made some experiments to infer the exact amount of Algos for both cases. 

For both the creation and the opt in to the contract we wanted to see how the minimum balance requirement changes for a different configuration of the contract. 
For both global and local state, we can have two kinds of values:

- Ints
- Byte-slices

The maximum number of states that the contract will use must be specified at the creation of the contract. 
To infer the minimum balance requirement at the change of the contract configuration, we tried to create a contract with five configurations:
- No states
- 1 global int
- 1 global byte-slice
- 1 local int
- local byte-slice

### No states
We have the following accounts with the following balance:

```
EHYTQKEFHIRPTJIBEUDCJSDKLKA322UX7PIA6E5EXJPC7N4T7UVSU2VLKI      100000 microAlgos
IMZHVPPDS3U4BGYQIGB2RKMLN22CBW26HD4TTZ3CLY4QZEOPWMWOOSHWNY      100000 microAlgos
```

EHYT... will be used as the creator of the contract and IMZH... will be the account which opts in to the contract during the experiment.

We try to create the following contract:
```
goal app create --creator EHYTQKEFHIRPTJIBEUDCJSDKLKA322UX7PIA6E5EXJPC7N4T7UVSU2VLKI --approval-prog approval_program.teal --clear-prog ./clear_state_program.teal --global-byteslices 0 --global-ints 0 --local-byteslices 0 --local-ints 0

Couldn't broadcast tx with algod: HTTP 400 Bad Request: TransactionPool.Remember: transaction WQY5VSJQ4J6QSVFIGGXN7HYMNIZHLIXTUIM33PGFXZN7NXFYVQQQ: account EHYTQKEFHIRPTJIBEUDCJSDKLKA322UX7PIA6E5EXJPC7N4T7UVSU2VLKI balance 99000 below min 200000 (0 assets)
```

As we can see by the transaction output, for creating a contract with this configuration at least 200000 micro-Algos are required. Notice that the balance reported in the transaction output is 99000 and not 100000. This because we do not take into account the minimum fee of 1000 micro-Algos that we have to pay for each transaction. 

So, we try to increase the creator balance up to 300000 micro-Algos and we try again to create the contract

```
goal app create --creator EHYTQKEFHIRPTJIBEUDCJSDKLKA322UX7PIA6E5EXJPC7N4T7UVSU2VLKI --approval-prog approval_program.teal --clear-prog ./clear_state_program.teal --global-byteslices 0 --global-ints 0 --local-byteslices 0 --local-ints 0
Attempting to create app (approval size 288, hash Q73AJHTDEYBG23P6VZ2RA2DQUDGPRB37D3BSIBVBFMECINK4HFSA; clear size 6, hash ZYI7YTWEXF6FGMRDOJNAGIID5M7OKO554TJOVU2RCA7Z2QWQEBTA)
Issued transaction from account EHYTQKEFHIRPTJIBEUDCJSDKLKA322UX7PIA6E5EXJPC7N4T7UVSU2VLKI, txid KSB3HDEF25LMUQKJD5D2FBPY72VEHIMDMDEMRSOUP2VUS5ZYMGPA (fee 1000)
Transaction KSB3HDEF25LMUQKJD5D2FBPY72VEHIMDMDEMRSOUP2VUS5ZYMGPA still pending as of round 11962283
Transaction KSB3HDEF25LMUQKJD5D2FBPY72VEHIMDMDEMRSOUP2VUS5ZYMGPA committed in round 11962285
Created app with app index 13676877
```
As expected the contract has been created.

Now, we try to opt in the account IMZH... to the contract

```
goal app optin --from IMZHVPPDS3U4BGYQIGB2RKMLN22CBW26HD4TTZ3CLY4QZEOPWMWOOSHWNY --app-id 13676877
Couldn't broadcast tx with algod: HTTP 400 Bad Request: TransactionPool.Remember: transaction EBPOGPKJZDT3IQAMXJ3PO4MAEGONKHJU3BTKU5F6FYNMAPGODZSA: account IMZHVPPDS3U4BGYQIGB2RKMLN22CBW26HD4TTZ3CLY4QZEOPWMWOOSHWNY balance 99000 below min 200000 (0 assets)
```

As expected it does not work. This because the required minimum balance is 200000. So, we try to increase the balance of IMZH... to 300000 and try again the opt in.

```
goal app optin --from IMZHVPPDS3U4BGYQIGB2RKMLN22CBW26HD4TTZ3CLY4QZEOPWMWOOSHWNY --app-id 13676877

Issued transaction from account IMZHVPPDS3U4BGYQIGB2RKMLN22CBW26HD4TTZ3CLY4QZEOPWMWOOSHWNY, txid PDQ2AHTVTAJPNC4HHNIF7MCDSJV6SMGPQRAIY6NVZDUYEHR33GKA (fee 1000)
Transaction PDQ2AHTVTAJPNC4HHNIF7MCDSJV6SMGPQRAIY6NVZDUYEHR33GKA still pending as of round 11962399
Transaction PDQ2AHTVTAJPNC4HHNIF7MCDSJV6SMGPQRAIY6NVZDUYEHR33GKA committed in round 11962401
```

As expected IMZH... opts in to the contract.

To be sure that values we have found are valid not only for the first contract we created or we opted in, but also for every additional contract, we try again to create another contract with EHYT... and we opt in IMZH... to the new contract:

```
goal app create --creator EHYTQKEFHIRPTJIBEUDCJSDKLKA322UX7PIA6E5EXJPC7N4T7UVSU2VLKI --approval-prog approval_program.teal --clear-prog ./clear_state_program.teal
--global-byteslices 0 --global-ints 0 --local-byteslices 0 --local-ints 0

Couldn't broadcast tx with algod: HTTP 400 Bad Request: TransactionPool.Remember: transaction 3PBMQSLIQACWY5AF35OLJZTZSWWDKSNXP4C2PMT4BMD25HNW4U7A: account EHYTQKEFHIRPTJIBEUDCJSDKLKA322UX7PIA6E5EXJPC7N4T7UVSU2VLKI balance 298000 below min 300000 (0 assets)
```

As we can see in the transaction output, the minimum balance required is 300000 and not 400000. This because the EHYT... has already created a contract, so we can conclude that for the first contract we need 200000 and then for every additional contract we want to create we need 100000.

Now, we want to test the behaviour for the opt in. So, we add an additional amount of micro-Algos to EHYT..., we create a new contract and then we opt in IMZH... to the new contract.

```
goal app create --creator EHYTQKEFHIRPTJIBEUDCJSDKLKA322UX7PIA6E5EXJPC7N4T7UVSU2VLKI --approval-prog approval_program.teal --clear-prog ./clear_state_program.teal --global-byteslices 0 --global-ints 0 --local-byteslices 0 --local-ints 0
Attempting to create app (approval size 288, hash Q73AJHTDEYBG23P6VZ2RA2DQUDGPRB37D3BSIBVBFMECINK4HFSA; clear size 6, hash ZYI7YTWEXF6FGMRDOJNAGIID5M7OKO554TJOVU2RCA7Z2QWQEBTA)
Issued transaction from account EHYTQKEFHIRPTJIBEUDCJSDKLKA322UX7PIA6E5EXJPC7N4T7UVSU2VLKI, txid F6E6XTTJZCUNXK6MM6OLXU3Y7QUBWVLXEUXPS6MCFPWFKZUN6FFA (fee 1000)
Transaction F6E6XTTJZCUNXK6MM6OLXU3Y7QUBWVLXEUXPS6MCFPWFKZUN6FFA still pending as of round 11980910
Transaction F6E6XTTJZCUNXK6MM6OLXU3Y7QUBWVLXEUXPS6MCFPWFKZUN6FFA committed in round 11980912
Created app with app index 13688216

goal app optin --from IMZHVPPDS3U4BGYQIGB2RKMLN22CBW26HD4TTZ3CLY4QZEOPWMWOOSHWNY --app-id 13688216

Couldn't broadcast tx with algod: HTTP 400 Bad Request: TransactionPool.Remember: transaction MBF2AV2AWAV4PLBVI4D4BTT3HJIXUSUKM6SL7BY4MQS43TOUPBTA: account IMZHVPPDS3U4BGYQIGB2RKMLN22CBW26HD4TTZ3CLY4QZEOPWMWOOSHWNY balance 298000 below min 300000 (0 assets)
```

As we can see, we have the same behaviour also for the opt in. Since we are opting in to two contracts with the same account, we could expect 400000 but the maximum balance required is 300000. So we can conclude that for the first contract we need 200000 and then for every additional contract we want to opt in with the same account, we need 100000.

#### 1 global int

We have the following accounts:

```
CABQ34AQGBHUHMOXQTD6QPRGTLOBPNEGI7OSNMOCHJKESCANIPLDSL7YR4      100000 microAlgos
RUWLL36CJBGLIW6HU44MO5LB4KGYOYBQYQZNHN7FYAC5MDSLRZYBX4SRPI      100000 microAlgos
```

CABQ... will be used as the creator of the contract and RUWL... will be the account which opts in during the experiment.

First of all, we try to create the contract

```
goal app create --creator CABQ34AQGBHUHMOXQTD6QPRGTLOBPNEGI7OSNMOCHJKESCANIPLDSL7YR4 --approval-prog approval_program.teal --clear-prog ./clear_state_program.teal --global-byteslices 0 --global-ints 1 --local-byteslices 0 --local-ints 0

Couldn't broadcast tx with algod: HTTP 400 Bad Request: TransactionPool.Remember: transaction MTUL6S5OQ74KXRNGZMTFQXL4YCXMUIYJNOOSJSQ7WNR6MC6I6YUQ: account CABQ34AQGBHUHMOXQTD6QPRGTLOBPNEGI7OSNMOCHJKESCANIPLDSL7YR4 balance 99000 below min 228500 (0 assets)
```

As expected it does not work. Considering that in the configuration with no states Algorand requires 200000 micro-Algos, we can suppose that for each global int, 28500 micro-Algos are required. To prove this, we try to do another attempt in which we increase the maximum number of global-ints from 1 to 2:

```
goal app create --creator CABQ34AQGBHUHMOXQTD6QPRGTLOBPNEGI7OSNMOCHJKESCANIPLDSL7YR4 --approval-prog approval_program.teal --clear-prog ./clear_state_program.teal --global-byteslices 0 --global-ints 2 --local-byteslices 0 --local-ints 0

Couldn't broadcast tx with algod: HTTP 400 Bad Request: TransactionPool.Remember: transaction B6YQ7X3PSXQA6EWZAR5VXHFRZ6LBBKVNK3UGVOKRYN3KHR7HAAOQ: account CABQ34AQGBHUHMOXQTD6QPRGTLOBPNEGI7OSNMOCHJKESCANIPLDSL7YR4 balance 99000 below min 257000 (0 assets)
```

Considering that the additional amount required for the configuration with no states is 57000, as we can see the first assumption holds (28500 * 2 = 57000).

So increasing the balance of CABQ... we can see that, as expected, the contract will be created.

```
goal app create --creator CABQ34AQGBHUHMOXQTD6QPRGTLOBPNEGI7OSNMOCHJKESCANIPLDSL7YR4 --approval-prog approval_program.teal --clear-prog ./clear_state_program.teal --global-byteslices 0 --global-ints 1 --local-byteslices 0 --local-ints 0

Attempting to create app (approval size 288, hash Q73AJHTDEYBG23P6VZ2RA2DQUDGPRB37D3BSIBVBFMECINK4HFSA; clear size 6, hash ZYI7YTWEXF6FGMRDOJNAGIID5M7OKO554TJOVU2RCA7Z2QWQEBTA)
Issued transaction from account CABQ34AQGBHUHMOXQTD6QPRGTLOBPNEGI7OSNMOCHJKESCANIPLDSL7YR4, txid MW7A4TIHHRIX64DA4FWVCD6JSWG4TZFLTY3PBZGI7CL25DNJFEHA (fee 1000)
Transaction MW7A4TIHHRIX64DA4FWVCD6JSWG4TZFLTY3PBZGI7CL25DNJFEHA still pending as of round 11962664
Transaction MW7A4TIHHRIX64DA4FWVCD6JSWG4TZFLTY3PBZGI7CL25DNJFEHA committed in round 11962666
Created app with app index 13683381
```

Now we try to opt in RUWL... to the contract

```
goal app optin --from RUWLL36CJBGLIW6HU44MO5LB4KGYOYBQYQZNHN7FYAC5MDSLRZYBX4SRPI --app-id 13683381

Couldn't broadcast tx with algod: HTTP 400 Bad Request: TransactionPool.Remember: transaction IVKX2WAMN3MQYVC5347LOKNGYDYF6IK6ELUE32V54SXU6GMVKZQQ: account RUWLL36CJBGLIW6HU44MO5LB4KGYOYBQYQZNHN7FYAC5MDSLRZYBX4SRPI balance 99000 below min 200000 (0 assets)
```

As we can see the required minimum balance is the same as the configuration with no states. So we can assume that the number of global ints does not affect the minimum balance requirement for the account which wants to opt in to the contract.

#### 1 global byte-slice

We have the following accounts:

```
JQIRDX6FKVNUOSR5M7FW6EM2UAEHKNUFVGLV7TZUQABTVZEFVYV2ZCCJPA      100000 microAlgos
WT3VAHF4NOKAYDZSZBIA36TNIEV756V22PSQJ7QWUQX2EVZ67W4RVHJ4FI      100000 microAlgos
```

JQIR... will be the creator of the contract and WT3V... will be the account which opts in to the contract.

We create the contract:

```
goal app create --creator JQIRDX6FKVNUOSR5M7FW6EM2UAEHKNUFVGLV7TZUQABTVZEFVYV2ZCCJPA --approval-prog approval_program.teal --clear-prog ./clear_state_program.teal --global-byteslices 1 --global-ints 0 --local-byteslices 0 --local-ints 0

Couldn't broadcast tx with algod: HTTP 400 Bad Request: TransactionPool.Remember: transaction G3PKZHVUNDCKOI4MJDQVTM5K5A7DPJYNMW54BOD7AYA7KA7RDXOA: account JQIRDX6FKVNUOSR5M7FW6EM2UAEHKNUFVGLV7TZUQABTVZEFVYV2ZCCJPA balance 99000 below min 250000 (0 assets)
```

Considering that in the configuration with no states the transaction output reported 200000, we can assume that for each global byte-slice Algorand requires 50000 micro-Algos. To prove this, we try to increase the maximum amount of global byte-slice from 1 to 2.

```
goal app create --creator JQIRDX6FKVNUOSR5M7FW6EM2UAEHKNUFVGLV7TZUQABTVZEFVYV2ZCCJPA --approval-prog approval_program.teal --clear-prog ./clear_state_program.teal --global-byteslices 2 --global-ints 0 --local-byteslices 0 --local-ints 0

Couldn't broadcast tx with algod: HTTP 400 Bad Request: TransactionPool.Remember: transaction ART7CLSBRZNNIZUYHT47PIUIFH3OECD2VVMN5FCBNTK6CCB7NFOA: account JQIRDX6FKVNUOSR5M7FW6EM2UAEHKNUFVGLV7TZUQABTVZEFVYV2ZCCJPA balance 99000 below min 300000 (0 assets)
```

Considering that the additional amount required for the configuration with no states is 100000, as we can see the first assumption holds (50000 * 2 = 100000).

If we increase the balance of JQIR..., as expected, the contract is created.
```
goal app create --creator JQIRDX6FKVNUOSR5M7FW6EM2UAEHKNUFVGLV7TZUQABTVZEFVYV2ZCCJPA --approval-prog approval_program.teal --clear-prog ./clear_state_program.teal --global-byteslices 1 --global-ints 0 --local-byteslices 0 --local-ints 0

Attempting to create app (approval size 288, hash Q73AJHTDEYBG23P6VZ2RA2DQUDGPRB37D3BSIBVBFMECINK4HFSA; clear size 6, hash ZYI7YTWEXF6FGMRDOJNAGIID5M7OKO554TJOVU2RCA7Z2QWQEBTA)
Issued transaction from account JQIRDX6FKVNUOSR5M7FW6EM2UAEHKNUFVGLV7TZUQABTVZEFVYV2ZCCJPA, txid OZHCL2SIS4EVYIBMH2FSLVNGXVFG2WNL5KYOUAAULZCOXNLH6LUA (fee 1000)
Transaction OZHCL2SIS4EVYIBMH2FSLVNGXVFG2WNL5KYOUAAULZCOXNLH6LUA still pending as of round 11962921
Transaction OZHCL2SIS4EVYIBMH2FSLVNGXVFG2WNL5KYOUAAULZCOXNLH6LUA committed in round 11962923
Created app with app index 13685321
```

Now we try to opt in WT3V... to the contract.

```
goal app optin --from RUWLL36CJBGLIW6HU44MO5LB4KGYOYBQYQZNHN7FYAC5MDSLRZYBX4SRPI --app-id 13685321 --from WT3VAHF4NOKAYDZSZBIA36TNIEV756V22PSQJ7QWUQX2EVZ67W4RVHJ4FI

Couldn't broadcast tx with algod: HTTP 400 Bad Request: TransactionPool.Remember: transaction QR22FWRGIE3XOJUVXQH3OTROKPXXXLP6PGE7QBAEXQZKNTDPO63Q: account WT3VAHF4NOKAYDZSZBIA36TNIEV756V22PSQJ7QWUQX2EVZ67W4RVHJ4FI balance 99000 below min 200000 (0 assets)
```

As we can see in the transaction output, the minimum balance requirement is the same indicates in the configuration with no states. So, for this reason, we can conclude that the number of global byte-slices does not affect the minimum balance requirement for the account which wants to opt in to the contract.

#### 1 local int

We have the following accounts:

```
goal account list

BJUHSASXWPTQDEZLFQKTA5WGE2PSJ3RWPPRWP7GY2SVPJRYWZ4C5E6TDJA      100000 microAlgos
EDINFIS2B635LTIIWBE3WNTSNHJXS2JNXCIP53VMV36UYD6TZNKPZDQIJE      100000 microAlgos
```
BJUH... will be the creator of the contract and EDIN... will be the account which opts in to the contract.
We create the contract:

```
goal app create --creator BJUHSASXWPTQDEZLFQKTA5WGE2PSJ3RWPPRWP7GY2SVPJRYWZ4C5E6TDJA --approval-prog approval_program.teal --clear-prog ./clear_state_program.teal --global-byteslices 0 --global-ints 0 --local-byteslices 0 --local-ints 1

Couldn't broadcast tx with algod: HTTP 400 Bad Request: TransactionPool.Remember: transaction 7ZZECG5FGZIJTFTCGIMFOA6GRHKMEYPW562HGV7J3H6UVFQODVPA: account BJUHSASXWPTQDEZLFQKTA5WGE2PSJ3RWPPRWP7GY2SVPJRYWZ4C5E6TDJA balance 99000 below min 200000 (0 assets)
```

As we can see by the transaction output, the minimum amount required is the same that we have found in the configuration with no states. So we can conclude that the number of local ints does not affect the minimum balance requirement related to the creator of the contract.

We increase the balance of BJUH... and then we create the contract:


```
goal app create --creator BJUHSASXWPTQDEZLFQKTA5WGE2PSJ3RWPPRWP7GY2SVPJRYWZ4C5E6TDJA --approval-prog approval_program.teal --clear-prog ./clear_state_program.teal --global-byteslices 0 --global-ints 0 --local-byteslices 0 --local-ints 1

Attempting to create app (approval size 288, hash Q73AJHTDEYBG23P6VZ2RA2DQUDGPRB37D3BSIBVBFMECINK4HFSA; clear size 6, hash ZYI7YTWEXF6FGMRDOJNAGIID5M7OKO554TJOVU2RCA7Z2QWQEBTA)
Issued transaction from account BJUHSASXWPTQDEZLFQKTA5WGE2PSJ3RWPPRWP7GY2SVPJRYWZ4C5E6TDJA, txid YHIXVOXXLQFGAKWJPRUBWV774XBP5H3RJCX3AK4VO36OAK3CSE4Q (fee 1000)
Transaction YHIXVOXXLQFGAKWJPRUBWV774XBP5H3RJCX3AK4VO36OAK3CSE4Q still pending as of round 11980399
Transaction YHIXVOXXLQFGAKWJPRUBWV774XBP5H3RJCX3AK4VO36OAK3CSE4Q committed in round 11980401
Created app with app index 13688148
```

Once we created the contract, we can opt in EDIN...

```
goal app optin --from EDINFIS2B635LTIIWBE3WNTSNHJXS2JNXCIP53VMV36UYD6TZNKPZDQIJE --app-id 13688148

```

As we can see by the transaction output, 228500 micro-Algos are required. Considering that in the configuration with no states the minimum balance requirement was 200000, we can assume that for each local ints we need at least 28500 micro-Algos. To prove this we consider increasing the maximum amount of local ints from 1 to 2. So, we create again the contract and then we attempt again the opt in.

```
goal app create --creator BJUHSASXWPTQDEZLFQKTA5WGE2PSJ3RWPPRWP7GY2SVPJRYWZ4C5E6TDJA --approval-prog approval_program.teal --clear-prog ./clear_state_program.teal --global-byteslices 0 --global-ints 0 --local-byteslices 0 --local-ints 2

Attempting to create app (approval size 288, hash Q73AJHTDEYBG23P6VZ2RA2DQUDGPRB37D3BSIBVBFMECINK4HFSA; clear size 6, hash ZYI7YTWEXF6FGMRDOJNAGIID5M7OKO554TJOVU2RCA7Z2QWQEBTA)
Issued transaction from account BJUHSASXWPTQDEZLFQKTA5WGE2PSJ3RWPPRWP7GY2SVPJRYWZ4C5E6TDJA, txid D5WPMBPIB3YTHCE4EHJEPY4ZIQ65GDFNU5CCOTEELFIBQH6CFSMQ (fee 1000)
Transaction D5WPMBPIB3YTHCE4EHJEPY4ZIQ65GDFNU5CCOTEELFIBQH6CFSMQ still pending as of round 11980447
Transaction D5WPMBPIB3YTHCE4EHJEPY4ZIQ65GDFNU5CCOTEELFIBQH6CFSMQ committed in round 11980449
Created app with app index 13688155

goal app optin --from EDINFIS2B635LTIIWBE3WNTSNHJXS2JNXCIP53VMV36UYD6TZNKPZDQIJE --app-id 13688155

Couldn't broadcast tx with algod: HTTP 400 Bad Request: TransactionPool.Remember: transaction MVESMTVKTD3CIJQUJOKQ5HP3257Y2UH6NP4PBZHUJMRPSXV7UIUQ: account EDINFIS2B635LTIIWBE3WNTSNHJXS2JNXCIP53VMV36UYD6TZNKPZDQIJE balance 99000 below min 257000 (0 assets)
```

Considering that the additional amount required for the configuration with no states is 57000, as we can see from the transaction output, the first assumption holds (28500 * 2 = 57000).

#### 1 local byte-slice

We have the following accounts:

```
goal account list

OMTTRFE2HTONSJ66WFNVUX5BJN3IKZJJWIBLS5AQC4QCR7WY5OYRQUNKBI      100000 microAlgos
FEJCCWAPCUL7QTMG2MTRYJRWSABEHYJ442UAVPEBHS7SMKP2IVALBL4VMY      100000 microAlgos
```

OMTT... will be the creator of the contract and FEJC... will be the account which opts in to the contract.

We create the contract with the current configuration:

```
goal app create --creator OMTTRFE2HTONSJ66WFNVUX5BJN3IKZJJWIBLS5AQC4QCR7WY5OYRQUNKBI --approval-prog approval_program.teal --clear-prog ./clear_state_program.teal --global-byteslices 0 --global-ints 0 --local-byteslices 1 --local-ints 0

Couldn't broadcast tx with algod: HTTP 400 Bad Request: TransactionPool.Remember: transaction UZ3H3LEYW52ZD6TCC7O5HJDTKF3PY2CVFH4ESUT6OYROWR36RMKA: account OMTTRFE2HTONSJ66WFNVUX5BJN3IKZJJWIBLS5AQC4QCR7WY5OYRQUNKBI balance 99000 below min 200000 (0 assets)
```

As we can see by the transaction output, the minimum amount required is the same that we have found in the configuration with no states. So we can conclude that the number of local byte-slices does not affect the minimum balance requirement related to the creator of the contract.

We increase the balance of OMTT... and then we create the contract

```
goal app create --creator OMTTRFE2HTONSJ66WFNVUX5BJN3IKZJJWIBLS5AQC4QCR7WY5OYRQUNKBI --approval-prog approval_program.teal --clear-prog ./clear_state_program.teal --global-byteslices 0 --global-ints 0 --local-byteslices 1 --local-ints 0

Attempting to create app (approval size 288, hash Q73AJHTDEYBG23P6VZ2RA2DQUDGPRB37D3BSIBVBFMECINK4HFSA; clear size 6, hash ZYI7YTWEXF6FGMRDOJNAGIID5M7OKO554TJOVU2RCA7Z2QWQEBTA)
Issued transaction from account OMTTRFE2HTONSJ66WFNVUX5BJN3IKZJJWIBLS5AQC4QCR7WY5OYRQUNKBI, txid TT4JOT5CB4O5KTT6JUOLYY6QSF3FTVG6YWWWJ3SLQ64KZAH4JS7Q (fee 1000)
Transaction TT4JOT5CB4O5KTT6JUOLYY6QSF3FTVG6YWWWJ3SLQ64KZAH4JS7Q still pending as of round 11980606
Transaction TT4JOT5CB4O5KTT6JUOLYY6QSF3FTVG6YWWWJ3SLQ64KZAH4JS7Q committed in round 11980608
Created app with app index 13688174
```

Once we created the contract, we can opt in FEJC...

```
goal app optin --from FEJCCWAPCUL7QTMG2MTRYJRWSABEHYJ442UAVPEBHS7SMKP2IVALBL4VMY --app-id 13688174

Couldn't broadcast tx with algod: HTTP 400 Bad Request: TransactionPool.Remember: transaction 44BPDEAV6OY4FEOMNSMPGENREUTJLSX6D6GD4FVKSO5WCBOWD6SA: account FEJCCWAPCUL7QTMG2MTRYJRWSABEHYJ442UAVPEBHS7SMKP2IVALBL4VMY balance 99000 below min 250000 (0 assets)
```

As we can see by the transaction output, 250000 micro-Algos are required. Considering that in the configuration with no states the minimum balance requirement was 200000, we can assume that for each local byte-slice we need at least 50000 micro-Algos. To prove this we consider increasing the maximum amount of local byte slice from 1 to 2. So, we create again the contract and then we attempt again the opt in.

```
goal app create --creator OMTTRFE2HTONSJ66WFNVUX5BJN3IKZJJWIBLS5AQC4QCR7WY5OYRQUNKBI --approval-prog approval_program.teal --clear-prog ./clear_state_program.teal --global-byteslices 0 --global-ints 0 --local-byteslices 2 --local-ints 0

Attempting to create app (approval size 288, hash Q73AJHTDEYBG23P6VZ2RA2DQUDGPRB37D3BSIBVBFMECINK4HFSA; clear size 6, hash ZYI7YTWEXF6FGMRDOJNAGIID5M7OKO554TJOVU2RCA7Z2QWQEBTA)
Issued transaction from account OMTTRFE2HTONSJ66WFNVUX5BJN3IKZJJWIBLS5AQC4QCR7WY5OYRQUNKBI, txid FAQQ3YSFKSEI2IR35KVSS7B4N6HIXZIWAGIHXXLU4XC7CJRK3MWQ (fee 1000)
Transaction FAQQ3YSFKSEI2IR35KVSS7B4N6HIXZIWAGIHXXLU4XC7CJRK3MWQ still pending as of round 11980672
Transaction FAQQ3YSFKSEI2IR35KVSS7B4N6HIXZIWAGIHXXLU4XC7CJRK3MWQ committed in round 11980674
Created app with app index 13688184

goal app optin --from FEJCCWAPCUL7QTMG2MTRYJRWSABEHYJ442UAVPEBHS7SMKP2IVALBL4VMY --app-id 13688184

Couldn't broadcast tx with algod: HTTP 400 Bad Request: TransactionPool.Remember: transaction UFBSGGGQO7FT3REMCAIZ3DVUXI5DFWUPWNBD5E4IEYXWKOLRFXLQ: account FEJCCWAPCUL7QTMG2MTRYJRWSABEHYJ442UAVPEBHS7SMKP2IVALBL4VMY balance 99000 below min 300000 (0 assets)
```

As expected, considering that the additional amount required for the configuration with no states is 100000, as we can see from the transaction output, the first assumption holds (50000 * 2 = 100000).

#### Conclusions

With these experiments, it has been possible to infer the minimum balance requirements for every contract configuration. So, we decided to resume all the minimum balance requirements both for the creation and the opt in to the contract.

|                                   |                      Contract creator’s account                     |
|-----------------------------------|:-------------------------------------------------------------------:|
| Fixed minimum balance requirement | 200000 for the first contract - 100000 for each additional contract |
|        For each global int        |                                28500                                |
|     For each global byte-slice    |                                50000                                |
|         For each local int        |                                  -                                  |
|     For each local byte-slice     |                                  -                                  |



|                                   |            Account which wants to opt in to the contract            |
|-----------------------------------|:-------------------------------------------------------------------:|
| Fixed minimum balance requirement | 200000 for the first contract - 100000 for each additional contract |
|        For each global int        |                                  -                                  |
|     For each global byte-slice    |                                  -                                  |
|         For each local int        |                                28500                                |
|     For each local byte-slice     |                                50000                                |

### Number of accounts which can opt in to the contract

This behaviour is not described by the Algorand documentation so, for this reason, we try to infer the behaviour trying to create more accounts and trying to opt in every account to the contract. In this experiment, we use N=1000 accounts.

First of all, we create the accounts  and we initialise every account balance with a certain amount of Algos using the Algorand dispenser provided by Algorand

```
#!/bin/bash

for i in {1..1000}
do
    goal account new
done
```

Then, we create a contract example using [this code](./example_stateful_contract.md) and we try to opt in 1000 accounts to the contract 

```
goal app create --creator VNNIMUZK5VZGG45FPDIRASSTUY2ODKSTHH5Y56AWPAFZYIE7CFMRA4ADOE --approval-prog approval_program.teal --clear-prog ./clear_state_program.teal --global-byteslices 1 --global-ints 1 --local-byteslices 1 --local-ints 1
```

```
#!/bin/bash

LIST=$(goal account list|awk '{ print $3 }')

for i in $LIST
do
    echo $i
    goal app optin --from=$i --app-id 13385038
done
```

Through the script has been possible to observe that every account opted in successfully.

```
ABWNGDPWTVDCNVYXTVBSJ2VP6Q5Z65LKADBHHMCCDSK4QCC4GIN3X5ZJJM
Issued transaction from account ABWNGDPWTVDCNVYXTVBSJ2VP6Q5Z65LKADBHHMCCDSK4QCC4GIN3X5ZJJM, txid A5XJDGJFUHD7PQDGYGSQORFYITYS2RWQFQ3AWDDVBTQCMEKH2Q4A (fee 1000)
Transaction A5XJDGJFUHD7PQDGYGSQORFYITYS2RWQFQ3AWDDVBTQCMEKH2Q4A still pending as of round 11955699
Transaction A5XJDGJFUHD7PQDGYGSQORFYITYS2RWQFQ3AWDDVBTQCMEKH2Q4A committed in round 11955701
```

So, we can conclude that with N=1000 accounts, it was not possible to find an upper bound of the number of accounts which can opt in to the contract.