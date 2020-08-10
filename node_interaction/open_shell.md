## Node interaction

#### Open a shell

Open a shell in sandbox and basic interaction with the node

```
./sandbox enter
```

You can now interact with the node and run commands from within the container.

Type the ```ls``` command to see the list of files.

```
$ ./sandbox enter
Entering /bin/bash session in the sandbox container...
algorand@1238443847f0:/opt/algorand/node$ ls
COPYING  algoh                       backup      data         find-nodes.sh  kmd            sudoers.template  updater
algocfg  algokey                     carpenter   ddconfig.sh  genesisfiles   msgpacktool    systemd-setup.sh
algod    algorand@.service.template  catchupsrv  diagcfg      goal           node_exporter  update.sh
```

------