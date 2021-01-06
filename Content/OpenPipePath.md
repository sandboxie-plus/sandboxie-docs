# Open Pipe Path

_OpenPipePath_ is a sandbox setting in [Sandboxie Ini](SandboxieIni). It specifies path patterns for which Sandboxie will not apply sandboxing for files.

It is the same as the [OpenFilePath](OpenFilePath) setting, except that this setting is always applied, whereas _OpenFilePath_ is only applied if the application is running from a file or folder that is located outside the sandbox.

See [OpenFilePath](OpenFilePath) for general usage instructions.

The _OpenPipePath_ setting is primarily intended to allow sandboxed programs access to file communication device resources, which can be identified using the [Sandboxie Trace](SandboxieTrace).

However, it can also be used to define files and folders that should be exempt (in the way that _OpenFilePath_ exempts files) even for programs that are running from within the sandbox itself.

Example usage:
```
   .
   .
   .
   [DefaultBox]
   OpenPipePath=\Device\NamedPipe\wkssvc
   OpenPipePath=\Device\NamedPipe\srvsvc
```

Will allow the sandboxed program to manage shares and user accounts on the computer, through the resources _wkssvc_ and _srvsvc_.

**Note:** This specific example is not recommended, as it weakens the protection of the sandbox.

Related [Sandboxie Control](SandboxieControl) setting: [Sandbox Settings > Resource Access > File Access > Full Access](ResourceAccessSettings#file)
