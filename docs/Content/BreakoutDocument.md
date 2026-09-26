# Breakout Document

_BreakoutDocument_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md), available since Sandboxie Plus 1.15.0 / Classic 5.70.0. It can route a matching path from a supported Shell document-open request to the host Shell, so the document may open outside the source sandbox. It is separate from process-directory [Breakout Folder](BreakoutFolder.md) rules.

```ini
[DefaultBox]
BreakoutDocument=C:\Documents\*.pdf
BreakoutDocument=C:\Pictures\*.jpg
```

The rule is matched case-insensitively against the file/path text supplied to an intercepted `ShellExecuteExW` request, using Sandboxie's pattern syntax for this path. It does not inspect the file's contents, verify its MIME type, or cover every way an application can open a document. A matching request is revalidated by the user-session proxy, which asks the host Shell to open that path with the `open` verb. The original Shell verb, parameters, and working directory are not forwarded unchanged.

> **Security warning:** A host-side open can start an application or execute content outside the source sandbox. Restrict rules to intended paths and document types. A broad rule such as `BreakoutDocument=C:\path\*` can allow scripts or executables to run outside the sandbox.

SandMan's **Breakout Document** workflow asks for a folder and extension and warns about broad or risky selections. Those checks apply when creating entries in the interface; they are not a runtime extension allowlist. A manually edited INI can contain broader patterns.

The rule affects future supported Shell-open requests, not completed opens or arbitrary file access. See [Breakout Execution](BreakoutExecution.md) for the architecture, Explorer compatibility bridge, other breakout settings, and SandMan controls.
