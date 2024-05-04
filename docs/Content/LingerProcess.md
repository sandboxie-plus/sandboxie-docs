# Linger Process

_LingerProcess_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies names of programs that will be automatically terminated, when they are the last programs that remain in execution in a particular sandbox. This is useful as some programs occasionally launch _helper programs_ to carry out a specific task, and the helper program remains in execution even after the original program has ended. For example:

```
   .
   .
   .
   [DefaultBox]
   LingerProcess=jusched.exe
```

_jusched.exe_ is part of the Sun Java framework. It is occasionally launched when Internet Explorer starts the Java framework. This _LingerProcess_ example setting specifies that if _jusched.exe_ remains the last program running in the sandbox DefaultBox, then it should be terminated.

LingerProcess will not terminate a process, if that process was the first process launched in the sandbox.

For example, the default configuration includes Adobe Acrobat Reader as a LingerProcess, because it is typically launched when viewing PDF files through the Web browser, and remains running even after the browser has closed.
```
   LingerProcess=acrord32.exe
```

However, if you manually start Adobe Acrobat Reader sandboxed, for example by running it from the Sandboxie Start Menu, then the LingerProcess setting will not apply to that process.

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings -> Program Stop -> Lingering Programs](ProgramStopSettings.md#lingering-programs)

See also: [Program Settings](ProgramSettings.md#linger).
