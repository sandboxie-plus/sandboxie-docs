# Process Limit 1

**ProcessLimit1 and ProcessLimit2 were removed since Sandboxie v0.7.1 / 5.48.5 in favour of [ProcessLimit](ProcessLimit.md).**

_ProcessLimit1_ and _ProcessLimit2_ were sandbox settings in [Sandboxie Ini](SandboxieIni.md). They limited the maximum number of processes that Sandboxie allowed in the sandbox at the same time.
```
   .
   .
   .
   [DefaultBox]
   ProcessLimit1=100
   ProcessLimit2=200
```

ProcessLimit1: Once the sandbox has more than X programs at the same time, each new program will be delayed for ten seconds before it starts to run. X is the number specified in ProcessLimit1\. The length of the delay, ten seconds, is not configurable.

ProcessLimit2: Once the sandbox has more than Y programs at the same time, each new program will be immediately terminated. Y is the number specified in ProcessLimit2\.

The default numbers are 100 and 200 as mentioned above. ProcessLimit2 cannot be smaller than ProcessLimit1\.

Creative values can turn off one or both modes. For example,
```
	ProcessLimit2=999999
```

will effectively disable the termination feature. On the other hand,
```
	ProcessLimit1=50
	ProcessLimit2=50
```

will effectively disable the delaying feature.
