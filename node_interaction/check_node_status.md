## Node interaction

#### Check node status

Open a shell in sandbox and basic interaction with the node

```
./sandbox enter
```

You can now interact with the node and run commands from within the container.

Type the ```./goal node status -d data/``` command to check the details of your connection.

```
$ ./sandbox enter
Entering /bin/bash session in the sandbox container...
algorand@1238443847f0:/opt/algorand/node$ ./goal node status -d data/
Last committed block: 8524764
Time since last block: 4.2s
Sync Time: 0.0s
Last consensus protocol: https://github.com/algorandfoundation/specs/tree/e5f565421d720c6f75cdd186f7098495caf9101f
Next consensus protocol: https://github.com/algorandfoundation/specs/tree/e5f565421d720c6f75cdd186f7098495caf9101f
Round for next consensus protocol: 8524765
Next consensus protocol supported: true
Last Catchpoint: 8520000#ODGLLU76P2LIOXSOXVWMYXHAVX2UZUWNV2CA4FNFDBCHBCDJWTHQ
Genesis ID: testnet-v1.0
Genesis hash: SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI=
algorand@1238443847f0:/opt/algorand/node$
```



[Algorand's Doc - Connect to Node](https://developer.algorand.org/docs/build-apps/connect/) 

------