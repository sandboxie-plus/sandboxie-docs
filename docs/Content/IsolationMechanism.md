# Isolation Mechanism

Processes in normal security-isolation boxes generally run with heavily restricted Windows primary tokens. This limits what they can access under Windows security checks, while Sandboxie's other mechanisms provide the virtualization and compatibility behavior needed by applications. The exact token handling depends on configuration; Application Compartment mode bypasses normal primary-token replacement.

Sandboxie supports multiple token-construction and filtering paths. The normal current path constructs a new, heavily restricted primary token, while a historical filtering path remains available and uses implementation-specific Windows kernel handling. See [Access Token Isolation](AccessTokenIsolation.md) and the [token internals](TokenMagic.md) for details.

Sandboxie also intercepts selected native syscall stubs and routes those calls through SbieDrv. For applicable mediated operations, the driver can use the retained source-token or thread-token context while processing the call. Independent driver filters enforce resource-access restrictions according to the effective policy, including configured direct-access exceptions. Native Windows permissions remain applicable.

If an application bypasses a patched user-mode syscall stub by issuing a direct syscall, it does not recover Sandboxie's retained source-token context. The call normally continues under the sandbox token and remains subject to applicable Windows access checks and independent Sandboxie enforcement.

Not all functionality can be restored this way, so Sandboxie also hooks a myriad of other functions in standard Windows DLLs, providing workarounds and redirects through the helper service SbieSvc, although sometimes it opts for disabling some functionality outright.

File-system and Registry virtualization is implemented primarily in user mode by SbieDll. It maps supported operations to sandbox-backed storage and combines eligible host and sandbox data in merged views. Virtualization is distinct from driver-enforced restrictions and native Windows authorization: if a virtualization path is unavailable or bypassed, the result depends on the operation, effective token, resource rules, and remaining enforcement. Neither access denial nor successful host access is guaranteed.
