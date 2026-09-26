# Breakout Execution

Breakout is an intentional exception to sandbox containment for selected future operations. [Breakout Process](BreakoutProcess.md) and [Breakout Folder](BreakoutFolder.md) can affect a new process creation attempt from inside a sandbox. [Breakout Document](BreakoutDocument.md) instead applies to a supported Shell request to open a matching path. None of these settings moves an already-running process out of its box, grants elevation, or makes arbitrary file access unsandboxed.

## Process breakout

When a sandboxed program tries to start a new process, Sandboxie first checks whether the target is a breakout candidate. The sandboxed process then asks the Sandboxie service to create it outside the source box. The service independently checks the breakout rule before creating the process; the initial candidate check alone does not authorize the escape.

If the service rejects the breakout request with `ERROR_NOT_SUPPORTED`, Sandboxie continues through the normal sandboxed process-creation path. Other creation errors do not necessarily have that fallback. For `BreakoutProcess`, the service additionally requires the target executable to resolve to a host file outside the source sandbox's file root. That specific host-file check is not applied to `BreakoutFolder`.

A successful breakout does not necessarily leave the process unsandboxed. The service checks enabled boxes for matching [Force Process](ForceProcess.md) or [Force Folder](ForceFolder.md) rules, so another box can capture the launch. For example, if viewing a PDF from an Email box starts `browser.exe`, `BreakoutProcess=browser.exe` in Email and `ForceProcess=browser.exe` in a Browser box can route that browser launch to Browser. This is not a configurable priority between boxes: when several boxes match, do not rely on a particular destination being selected. `ForceChildren` does not participate in this explicit destination check.

If that force check resolves back to the source box, the service rejects the breakout request with `ERROR_NOT_SUPPORTED`, and normal sandboxed creation resumes. For a host breakout, the service creates the process using the token appropriate to the request and returns limited-access process and thread handles to the sandboxed caller, not full-control handles. Breakout is not an elevation mechanism.

## Document breakout

`BreakoutDocument` is a separate Shell-open mechanism, not a folder-based process rule. On an intercepted `ShellExecuteExW` path, Sandboxie compares the supplied file/path text with the configured patterns. A match is sent through the user-session proxy, which validates the sandboxed caller and session and checks the rule again. It then asks the host Shell to open the matched path with the `open` verb.

The host request contains the path, not an unchanged copy of the original Shell request: the original verb, parameters, and working directory are not forwarded. This does not cover every way an application might open a document. A host-side open can start an application or execute content outside the originating box's file and registry virtualization.

> **Security warning:** Use narrow paths and intended document types. A broad rule such as `BreakoutDocument=C:\path\*` can allow executable or script content to run outside the source sandbox. SandMan warns about broad or risky document patterns, but its extension checks are UI safeguards, not a runtime allowlist. Manually edited configuration can contain broader patterns.

## Explorer compatibility bridge

`BreakoutDocumentProcess` is an image-aware Boolean compatibility setting, disabled by default. The Windows Explorer template sets `BreakoutDocumentProcess=explorer.exe,y` because Explorer can initiate the relevant document launch through process creation rather than the usual intercepted `ShellExecuteExW` route. For that image, Sandboxie checks the command-line remainder against `BreakoutDocument` rules during a future process creation attempt. This is an Explorer compatibility bridge, not another general-purpose breakout list; normally it does not need manual configuration. It was added in Sandboxie Plus 1.15.1 / Classic 5.70.1.

## Configuration and applying changes

Active breakout entries can come from the box configuration or applicable templates. In SandMan, open **Sandbox Options > Program Control > Breakout Programs** to use **Breakout Program**, **Breakout Folder**, **Breakout Document**, **Show Templates**, and **Remove**. An unchecked entry remains available in the interface under a corresponding `BreakoutProcessDisabled`, `BreakoutFolderDisabled`, or `BreakoutDocumentDisabled` setting; these saved entries are not active breakout rules. There is no single global breakout switch in this interface.

The process rules are evaluated for future relevant process creation attempts, and document rules for future supported Shell-open requests. Changes do not relocate existing processes or alter completed document opens. After the effective configuration is updated, subsequently evaluated operations can use the new rules without restarting Windows, the service, or an already-running sandboxed application solely for breakout.

## Version history

`BreakoutProcess` and `BreakoutFolder` appeared in Sandboxie Plus 1.0.8 / Classic 5.55.8. In 1.0.9 / 5.55.9, process breakout was reworked around service-created processes. `BreakoutDocument` was introduced in 1.15.0 / 5.70.0, followed by the Explorer-related `BreakoutDocumentProcess` bridge in 1.15.1 / 5.70.1.

## Related pages

- [Breakout Process](BreakoutProcess.md)
- [Breakout Folder](BreakoutFolder.md)
- [Breakout Document](BreakoutDocument.md)
- [Force Process](ForceProcess.md)
- [Force Folder](ForceFolder.md)
