## Account

#### Delete an account

This is the process to delete an account.

We have two non-empty accounts. Use the command ```./goal account list``` to list all accounts


```
algorand@1238443847f0:/opt/algorand/node$ ./goal account list
Please enter the password for wallet 'myWallet':
[offline]       Unnamed-0       GKQFFBB74PQY7KS5T5A73NPNGQKWOO2GHVRXKS2NEGXYKLANAOP74U3EE4      98999000 microAlgos     *Default
[offline]       Unnamed-1       HUUQGQ3MTIZLRNCANCPWJGD2VJAGKCLDJFVRYWQSTIJILQ6HEZUOJNWUW4      1000000 microAlgos
```

Type the command ```./goal account delete -a HUUQGQ3MTIZLRNCANCPWJGD2VJAGKCLDJFVRYWQSTIJILQ6HEZUOJNWUW4``` to delete the account.

```
algorand@1238443847f0:/opt/algorand/node$ ./goal account delete -a HUUQGQ3MTIZLRNCANCPWJGD2VJAGKCLDJFVRYWQSTIJILQ6HEZUOJNWUW4
Please enter the password for wallet 'myWallet':
algorand@1238443847f0:/opt/algorand/node$ ./goal account list
[offline]       Unnamed-0       GKQFFBB74PQY7KS5T5A73NPNGQKWOO2GHVRXKS2NEGXYKLANAOP74U3EE4      98999000 microAlgos     *Default
```

The account was deleted. This will not remove money from your account. You can always recover your account as shown [here](https://github.com/blockchain-unica/asc1-experiments/blob/master/account/recover.md#recover_account).

[Algorand's Doc - goal account delete](https://developer.algorand.org/docs/reference/cli/goal/account/delete/) 

------