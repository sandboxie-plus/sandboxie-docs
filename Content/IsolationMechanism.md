# Isolation Mechanism

Processes started under sandboxie's supervision are created with a very restricted user token, such that they basically don't have the right to access almost anything. In this state they would be pretty much useless and would crash right away.

This token manipulation is done using half a dozen [undocumented](TokenMagic.md) symbols in the windows kernel.

In a next step sandboxie tries to repair that by hooking most ntdll.dll syscalls and replacing them with a redirection to the own SbieDrv driver. The driver then evaluates the calls and enforces the sandboxing rules, for example, no write access outside the sandbox and no read access to closed resources.

When a malicious application would unhook ntdll.dll, for example, by trying to use direct syscalls to the windows kernel, the kernel would see the restricted user token and operations would fail with an access denied.

Not all functionality can be restored this way so sandboxie also hooks a myriad of other functions in standard windows dlls providing workarounds, and redirects through the helper service SbieSvc, although sometimes it also just opts for disabling some functionality outright.

The file system and registry virtualization is implemented on the user level in SbieDll, which is responsible for combining the data from the real system with the ones from the sandbox and for properly redirecting all access attempts. If that mechanism is improperly bypassed it results in a access denied error.

