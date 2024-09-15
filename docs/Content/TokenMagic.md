# SandboxieDrv use of undocumented kernel exports to do its token magic

Sandboxie implements isolation by running sandboxed processes with a heavily restricted primary token. As most applications cannot function this way, it hooks all NTDLL.dll calls redirecting them through an interface in the SbieDrv. The driver then can inspect the call arguments, makes the calling thread impersonate the original unrestricted token, execute the system call, and de-impersonate the thread before returning control to user mode.

This way, a process running under the supervision of Sandboxie cannot issue syscalls with the original token, even if it would undo the ntdll.dll hooks.

For this mechanism to work, Sandboxie utilizes a couple of undocumented operations:

1. To create the restricted token, it uses currently the unexported function SepFilterToken as well as a couple of offsets (RestrictedSidCount, RestrictedSids, UserAndGroups, UserAndGroupCount).
This mechanism could be replaced by calling CreateToken or CreateTokenEx, however these functions are not exported in the kernel either.

To eliminate the dependencies on unexported symbols, for this part of the process ZwCreateTokenEx should be exported and utilized.

2. To be able to invoke any syscall on the behalf of the sandboxed process, the driver must know the function address and argument count for each syscall index.
Sandboxie currently obtains those by finding the address of the unexported syscall table by analyzing the KeAddSystemServiceTable function.

To eliminate the dependencies on unexported symbols, it is required to export KeServiceDescriptorTableShadow.

3. Due to limitations in PsImpersonateClient (starting with Windows XP SP2), it is required to call it with impersonation level SecurityIdentification and then change that in the opaque thread object to SecurityImpersonation.

To eliminate the dependencies on unexported symbols, it would be required to provide a documented mechanism for a driver to achieve any desired impersonation level.

4. To replace a sandboxed processes primary token, it is required to clear the PrimaryTokenFrozen bit in the EPROCESS structure, this operation is triggered from a callback registered with PsSetLoadImageNotifyRoutine.

I have not investigated if it would be feasible to do the token replacement before it gets officially frozen.

Other than the above essential dependencies, Sandboxie gets the Clipboard object from the window station object in order to adjust the integrity level for the stored items such that they can be accessed by the sandboxed applications.
