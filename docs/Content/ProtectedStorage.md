# Protected Storage

Windows Protected Storage (PStore) is a legacy interface that let applications store user data intended to be protected, such as passwords or other sensitive values, through `PStoreCreateInstance` and the `IPStore` API. It is distinct from the Windows Credential APIs (WinCred) described in [Open Credentials](OpenCredentials.md). These facilities should not be treated as interchangeable names for a modern Windows password store.

In an ordinary sandbox, Sandboxie normally replaces `PStoreCreateInstance` with its own `IPStoreImpl` compatibility implementation. Its data uses sandbox-local backing storage. Current code constructs a `SbiePst.dat` filename under the Windows directory by default, but a build-time filename override is possible and sandbox file virtualization determines the physical location; do not rely on a fixed host path. This implementation provides compatibility for applications using the legacy PStore interface, not an assurance that all Windows credential mechanisms are isolated.

Sandboxie's default WinCred compatibility layer also uses this PStore implementation as backing storage for intercepted credential modifications. Its read and enumeration paths can still consult the native Windows credential store. See [Open Credentials](OpenCredentials.md) for that important boundary.

## Data visibility and protection

Sandboxie's replacement uses a common backing file in the sandboxed Windows path rather than a private PStore file for each application. Access to that file still depends on sandbox and host permissions, so this does not establish visibility across Windows user accounts.

The current file format applies a simple reversible transformation to stored blocks, not strong encryption. Treat sandbox data containing PStore items as sensitive. When the backing file remains inside the sandbox, deleting that sandbox's contents removes the local items with it; this does not delete host credentials or data stored through an opened host path.

## Opening the system implementation

Select the [Open Protected Storage](OpenProtectedStorage.md) template to open the relevant system endpoints. The open protected-storage IPC path causes Sandboxie to skip its replacement PStore hook and also its user-mode WinCred hooks. The old `OpenProtectedStorage=y` Boolean is not the current method.

[Application Compartment](../PlusContent/compartment-mode.md) also skips Sandboxie's PStore replacement hook. The WinCred hooks have separate checks, so compartment mode alone should not be described as automatically enabling `OpenCredentials`.

These compatibility choices do not cover every way a sandboxed application might store or access secrets. See [SBIE2205](SBIE2205.md) for unsupported PStore methods and [SBIE2213](SBIE2213.md) for failure to initialize Sandboxie's credential backing store.
