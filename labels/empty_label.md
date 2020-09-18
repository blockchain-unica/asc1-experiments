## Labels

#### Test 1


We wrote and compiled the following sample contained labels:

```
algorand@d414f5a29fd9:/opt/algorand/node$ cat program.teal
int 1
l0:
int 1
algorand@d414f5a29fd9:/opt/algorand/node$ goal clerk compile program.teal 
program.teal: CGAYBPJZPD4FZTRS3OIGR4KLC2LCY5PDJIFY2ZLYN5R6AGESD3CSPZAQLQ
```
We can explore the entire structure of the node typing the command: ```ls -l```.

```
algorand@d414f5a29fd9:/opt/algorand/node$ ls -l
total 322776
-rw-r--r-- 1 algorand algorand    36469 Sep 17 09:20 COPYING
-rwxr-xr-x 1 algorand algorand 18134376 Sep 17 09:20 algocfg
-rwxr-xr-x 1 algorand algorand 45176952 Sep 17 09:20 algod
-rwxr-xr-x 1 algorand algorand 35591048 Sep 17 09:20 algoh
-rwxr-xr-x 1 algorand algorand 30327280 Sep 17 09:20 algokey
-rw-r--r-- 1 algorand algorand     1389 Sep 17 09:20 algorand@.service.template
drwxr-xr-x 2 algorand algorand     4096 Sep 17 09:20 backup
-rwxr-xr-x 1 algorand algorand  3648192 Sep 17 09:20 carpenter
-rwxr-xr-x 1 algorand algorand 34118576 Sep 17 09:20 catchupsrv
drwxr-xr-x 5 algorand algorand     4096 Sep 17 09:21 data
-rwxr-xr-x 1 algorand algorand     4331 Sep 17 09:20 ddconfig.sh
-rwxr-xr-x 1 algorand algorand 25390416 Sep 17 09:20 diagcfg
-rwxr-xr-x 1 algorand algorand      249 Sep 17 09:20 find-nodes.sh
drwxr-xr-x 6 algorand algorand     4096 Sep 17 09:20 genesisfiles
-rwxr-xr-x 1 algorand algorand 42928368 Sep 17 09:20 goal
-rwxr-xr-x 1 algorand algorand 32663616 Sep 17 09:20 kmd
-rwxr-xr-x 1 algorand algorand 16172280 Sep 17 09:20 msgpacktool
-rwxr-xr-x 1 algorand algorand 16426300 Sep 17 09:20 node_exporter
-rwxrwxrwx 1 algorand algorand       16 Sep 17 11:07 program.teal
-rw-r--r-- 1 algorand algorand        6 Sep 17 11:07 program.teal.tok
-rwxr-xr-x 1 algorand algorand      582 Sep 17 09:20 sudoers.template
-rwxr-xr-x 1 algorand algorand      583 Sep 17 09:20 systemd-setup.sh
-rwxr-xr-x 1 algorand algorand    18662 Sep 17 09:20 update.sh
-rwxr-xr-x 1 algorand algorand 29816064 Sep 17 09:20 updater
```

The program produced the address: ```CGAYBPJZPD4FZTRS3OIGR4KLC2LCY5PDJIFY2ZLYN5R6AGESD3CSPZAQLQ```.

We use  tha Algorand dispenser to create a deposit.

```
algorand@d414f5a29fd9:/opt/algorand/node$ goal account balance -a CGAYBPJZPD4FZTRS3OIGR4KLC2LCY5PDJIFY2ZLYN5R6AGESD3CSPZAQLQ
100000000 microAlgos
```

We created two new accounts that will be used as sender and receiver for the transaction. To create an account we can use the tool [here](https://github.com/blockchain-unica/asc1-experiments/blob/master/account/client_nodejs/create.js).

```
Address 1: OLMPFYFQAQ2NWEUQJ4SA5IB3AGFVMYM74XMH5RVZ4AE5I65K3FZW5KCWRY
Address 2: YHRSXODWG526N4QQ6FP7RHRGP4RCNIZX53EHQWXRTFV4DHNDFMBJG76RSU
```

We prepare the transaction and send it.

```
algorand@d414f5a29fd9:/opt/algorand/node$ goal clerk send -a 7000000 --from-program program.teal -t YHRSXODWG526N4QQ6FP7RHRGP4RCNIZX53EHQWXRTFV4DHNDFMBJG76RSU -o out.txn -d data/
```

We inspect the file out.txn

```
algorand@d414f5a29fd9:/opt/algorand/node$ goal clerk inspect out.txn   
out.txn[0]
{
  "lsig": {
    "l": "// version 1\nintcblock 1\nintc_0\nintc_0\n"
  },
  "txn": {
    "amt": 7000000,
    "fee": 1000,
    "fv": 9300546,
    "gen": "testnet-v1.0",
    "gh": "SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI=",
    "lv": 9301546,
    "note": "irNpOA8nsfc=",
    "rcv": "YHRSXODWG526N4QQ6FP7RHRGP4RCNIZX53EHQWXRTFV4DHNDFMBJG76RSU",
    "snd": "CGAYBPJZPD4FZTRS3OIGR4KLC2LCY5PDJIFY2ZLYN5R6AGESD3CSPZAQLQ",
    "type": "pay"
  }
}
```

We send the transaction.

```
goal clerk rawsend -f out.txn -d data/
Warning: Couldn't broadcast tx with algod: HTTP 400 Bad Request: transaction LSQ5TBJHBINY6FXEL4NKQTXB5UMYUEJ6XUVVXMFSZ2FVFORTHEQA: rejected by logic err=stack len is 2 instead of 1
Encountered errors in sending 1 transactions:
  LSQ5TBJHBINY6FXEL4NKQTXB5UMYUEJ6XUVVXMFSZ2FVFORTHEQA: HTTP 400 Bad Request: transaction LSQ5TBJHBINY6FXEL4NKQTXB5UMYUEJ6XUVVXMFSZ2FVFORTHEQA: rejected by logic err=stack len is 2 instead of 1
Rejected transactions written to out.txn.rej
algorand@d414f5a29fd9:/opt/algorand/node$
```

```
algorand@d414f5a29fd9:/opt/algorand/node$ goal clerk dryrun -t out.txn
tx[0] cost=3 trace:
  1 intcblock => <empty stack>
  4 intc_0 => (1 0x1) 
  5 intc_0 => (1 0x1) 
end stack:
[0] 1 0x1
[1] 1 0x1

REJECT
ERROR: stack len is 2 instead of 1
```

------

#### Test 2

```
algorand@eed9a7afaba8:/opt/algorand/node$ cat program.teal 
int 1
l0:
algorand@eed9a7afaba8:/opt/algorand/node$ goal clerk compile program.teal 
program.teal: :2 label l0 is too far away

algorand@eed9a7afaba8:/opt/algorand/node$
```

------


#### Test 3

```
algorand@d414f5a29fd9:/opt/algorand/node$ cat program2.teal 
true
l0:
true
algorand@d414f5a29fd9:/opt/algorand/node$ goal clerk compile program2.teal 
program2.teal: :1 unknown opcode true

algorand@d414f5a29fd9:/opt/algorand/node$
```
