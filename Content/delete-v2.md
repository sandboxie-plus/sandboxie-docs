Sandboxie's new filesystem and registry virtualization scheme can be enabled by adding UseFileDeleteV2=y and UseRegDeleteV2=y to the Sandboxie.ini, which changes the mechanism of how host files/keys are marked within the sandbox as deleted.

The old scheme worked by creating a dummy file/key with a specified invalid creation date and marking the file/key as deleted. This scheme did fail when a folder/key containing “deleted” items was moved and a new folder of the same name created. Furthermore, for every path access it required the entire parent path to be scanned to see if one of the parents hasn’t been marked deleted.

The new Scheme saves this information in the FilePaths.dat/KeyPaths.dat files in the box root. Furthermore, when a folder/key is renamed within the sandbox, a redirection entry is created such that listing of the host content in the box under the new location is working.
