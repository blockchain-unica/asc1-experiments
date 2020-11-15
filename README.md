# A formal model of Algorand smart contracts
**Coherence-checking experiments**

- Account
  - [Delete](https://github.com/blockchain-unica/asc1-experiments/blob/master/account/delete.md#delete_account)
  - [Recover](https://github.com/blockchain-unica/asc1-experiments/blob/master/account/recover.md#recover_account)
  - [Generate random (malformed) address](https://github.com/blockchain-unica/asc1-experiments/blob/master/account/create_random_address.md#create_malformed_address)
  - [Client - Close](https://github.com/blockchain-unica/asc1-experiments/blob/master/account/client_nodejs/close.js#close_account)
  - [Client - Create](https://github.com/blockchain-unica/asc1-experiments/blob/master/account/client_nodejs/create.js#create_account)
  - [Client - Create wallet](https://github.com/blockchain-unica/asc1-experiments/blob/master/account/client_nodejs/create_wallet.js#create_wallet)
  - [Client - Info](https://github.com/blockchain-unica/asc1-experiments/blob/master/account/client_nodejs/info.js#info_account)

- Interaction with a node
  - [Check node status](https://github.com/blockchain-unica/asc1-experiments/blob/master/node_interaction/check_node_status.md#check_node_status)
  - [Open a shell](https://github.com/blockchain-unica/asc1-experiments/blob/master/node_interaction/open_shell.md#open_shell)

- Smart contract
  - Stateless
    - [Create a Contract account](https://github.com/blockchain-unica/asc1-experiments/blob/master/smart_contract/stateless/create_contract_account.md#create_contract_account)
    - [Close a Contract account](https://github.com/blockchain-unica/asc1-experiments/blob/master/smart_contract/stateless/close_contract_account.md#close_contract_account)
    - [Creating the same Contract account](https://github.com/blockchain-unica/asc1-experiments/blob/master/smart_contract/stateless/same_contract_account.md#same_script)
    - [Re-create a Contract account](https://github.com/blockchain-unica/asc1-experiments/blob/master/smart_contract/stateless/re_create_contract_account.md#re_create_contract_account)
    - [Multisig](https://github.com/blockchain-unica/asc1-experiments/blob/master/smart_contract/stateless/multisig.md#multisig)
  - Stateful
    - [Example stateful contract](https://github.com/blockchain-unica/asc1-experiments/blob/master/smart_contract/stateful/example_stateful_contract.md)
    - [Local state](https://github.com/blockchain-unica/asc1-experiments/blob/master/smart_contract/stateful/local_state.md)
    - [Global state](https://github.com/blockchain-unica/asc1-experiments/blob/master/smart_contract/stateful/global_state.md)
    

- Transactions
  - [Single transaction](https://github.com/blockchain-unica/asc1-experiments/blob/master/transactions/single_transaction.md#single_transaction)
  - [Single transaction with no sign](https://github.com/blockchain-unica/asc1-experiments/blob/master/transactions/single_transaction_no_sign.md#send_single_transaction_no_sign)
  - [Client - Send transaction](https://github.com/blockchain-unica/asc1-experiments/blob/master/transactions/client_nodejs/send.js#send_single_transaction)
  - [Pay from a sender to itself](https://github.com/blockchain-unica/asc1-experiments/blob/master/transactions/tx-pay-snd_eq_rcv.md#pay-sender-eq-receiver)
  - [Close to another address](https://github.com/blockchain-unica/asc1-experiments/blob/master/transactions/tx-close.md#close-to-another-address)
  - [Close to the sender](https://github.com/blockchain-unica/asc1-experiments/blob/master/transactions/tx-close.md#close-to-the-sender)
  - [Asset generation](https://github.com/blockchain-unica/asc1-experiments/blob/master/transactions/tx-gen-optin-burn.md#gen)
  - [Asset opt-in](https://github.com/blockchain-unica/asc1-experiments/blob/master/transactions/tx-gen-optin-burn.md#opt-in)
  - [Asset burn (creator without all token units)](https://github.com/blockchain-unica/asc1-experiments/blob/master/transactions/tx-gen-optin-burn.md#burn-creator-without-all-token-units)
  - [Asset burn (creator is manager)](https://github.com/blockchain-unica/asc1-experiments/blob/master/transactions/tx-gen-optin-burn.md#burn-creator-is-manager)
  - [Asset burn (creator is not manager)](https://github.com/blockchain-unica/asc1-experiments/blob/master/transactions/tx-gen-optin-burn.md#burn-creator-is-not-manager)
  - [Asset delegate](https://github.com/blockchain-unica/asc1-experiments/blob/master/transactions/tx-asset-config.md#delegate)
  - [Send frozen asset](https://github.com/blockchain-unica/asc1-experiments/blob/master/transactions/tx-freeze.md#send-frozen-asset)
  - [Freeze twice](https://github.com/blockchain-unica/asc1-experiments/blob/master/transactions/tx-freeze.md#freeze-twice)
  - [Unfreezeing an asset](https://github.com/blockchain-unica/asc1-experiments/blob/master/transactions/tx-freeze.md#unfreezing-an-asset)
  - [Receive frozen asset](https://github.com/blockchain-unica/asc1-experiments/blob/master/transactions/tx-freeze.md#receive-frozen-asset)
  - [Freeze non-existing asset](https://github.com/blockchain-unica/asc1-experiments/blob/master/transactions/tx-freeze.md#freeze-non-existing-asset)
  - [Freeze non-owned asset](https://github.com/blockchain-unica/asc1-experiments/blob/master/transactions/tx-freeze.md#freeze-non-owned-asset)
  - [Freezing in the freezer manager](https://github.com/blockchain-unica/asc1-experiments/blob/master/transactions/tx-freeze.md#freezing-in-the-freezer-manager)
  - [Opt-in a frozen asset](https://github.com/blockchain-unica/asc1-experiments/blob/master/transactions/tx-freeze.md#opt-in-a-frozen-asset)
  - [Sending zero asset units](https://github.com/blockchain-unica/asc1-experiments/blob/master/transactions/tx-freeze.md#sending-zero-asset-units)

- Labels
  - [Empty label](https://github.com/blockchain-unica/asc1-experiments/blob/master/labels/empty_label.md#empty_label)

- Use cases
  - Stateless
    - [Oracle](https://github.com/blockchain-unica/asc1-experiments/blob/master/use-cases/stateless/oracle.md#oracle)
