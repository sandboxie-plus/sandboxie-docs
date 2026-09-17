# Isolation Mechanism

Processes started under Sandboxie's supervision are created with a very restricted user token, such that they basically don't have the right to access almost anything. In this state, they would be pretty much useless and would crash right away.

This token handling uses a combination of documented APIs and [implementation-specific kernel mechanisms](TokenMagic.md). Modern token reconstruction avoids some of the internal `TOKEN`-layout dependencies retained by the legacy path.

In a next step, Sandboxie tries to repair that by redirecting selected native syscall stubs through its SbieDrv driver. The driver then evaluates the calls and enforces the sandboxing rules, for example, no write access outside the sandbox and no read access to closed resources.

If an application bypasses a patched user-mode syscall stub by issuing a direct syscall, it does not recover Sandboxie's retained source-token context. The call normally continues under the sandbox token and remains subject to applicable Windows access checks and independent Sandboxie enforcement.

Not all functionality can be restored this way, so Sandboxie also hooks a myriad of other functions in standard Windows DLLs, providing workarounds and redirects through the helper service SbieSvc, although sometimes it opts for disabling some functionality outright.

The file system and registry virtualization is implemented on the user level in SbieDll, which is responsible for combining the data from the real system with the ones from the sandbox and for properly redirecting all access attempts. If that mechanism is improperly bypassed, it results in an access denied error.
