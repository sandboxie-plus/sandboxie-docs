# Resource Access Settings

### "Resource Access" Settings Group

[Sandboxie Control](SandboxieControl.md) > [Sandbox Settings](SandboxSettings.md) > Resource Access

![](../Media/ResourceAccessSettings.png)

Programs that run in a sandbox are generally not allowed to access system resources directly. In some cases, it may be desirable to make exceptions to this rule. The settings here display and change that set of exceptions.

Examples where exceptions are convenient or necessary:

*   Allow direct access to some specific folder. For example, let the Web browser place downloads directly in a _Downloads_ folder.<br>
    See the [File Access](ResourceAccessSettings.md#file-access) category below.
*   A program may need access to some resource for correct operation. If the program is known and trusted, it is reasonable to make such an exception. See [Known Conflicts](KnownConflicts.md) for some examples.



Configuration changes do not apply to programs that are already running sandboxed at the time the configuration is changed. To keep things simple, you are advised to make configuration changes when no programs are running in the sandbox.


* * *

### General Information

Each settings page within the Resource Access group generally has the following characteristics:

![](../Media/ResourceAccessGeneral.png)

*   There is a _Title_ for the page, for example, _Direct File Acccess_ or _Read-Only Registry Access_.
*   There is a _Short Explanation_ describing what the setting does.

*   There is a _List of Resources_ that shows the resources that get a special treatment.
    *   Depending on the particular setting, it may mean that those resources will be fully accessible to sandboxed programs.
    *   Or it may mean that these resources will not be accessible at all.
    *   The _Short Explanation_ briefly describes the relationship between those resources and the programs which access them.
    *   You should also consult the documentation below for the particular setting, to fully understand what this means.
    *   The resources in the list may apply only to a particular program. Generally, however, they apply to _All Programs_.

*   There is an _Add_ button which adds a new resource entry to the list.
*   There is an _Edit/Add_ (sometimes just _Edit_) which edits a resource entry in the list, or adds a new resource entry to the list.
*   There is a _Remove_ button which removes a resource entry from the list.

*   There is a list-box labeled _The list above applies to._ This list-box associates the resources with a specific program.
    *   By default, resources apply to _All Programs_ as shown in the example above.
    *   You can select to apply resources to a specific program, by selecting that program from the list-box.
    *   You can also type the name of the specific program directly into the list-box.
    *   You can also use the _Add Pgm_ button to select a specific program by navigating to its folder.

* * *

### File Access

[Sandboxie Control](SandboxieControl.md) > [Sandbox Settings](SandboxSettings.md) > Resource Access > File Access

This category manages the following types of resources: Files, folders, drives, and other devices.

See [General Information](ResourceAccessSettings.md#general-information) above for more information about editing resources and associating resources with particular programs.

#### File Access > Direct Access

Allow direct access to some file or folder, bypassing the supervision of Sandboxie. For example, if you add a folder **C:\Downloads**, then a program running under Sandboxie will be able to create or update files in that folder.

Note that _Direct Access_ exclusions do not apply when the program itself resides in the sandbox. For example, suppose that you allow direct access to a **C:\Downloads** folder, and then you go on to install a new Web browser into the sandbox. This new sandboxed browser will _not_ have direct access to the **C:\Downloads** folder.

Related [Sandboxie Ini](SandboxieIni.md) settings: [OpenFilePath](OpenFilePath.md)

#### File Access > Full Access

Similar to _Direct Access_, but always applies, even if the sandboxed program itself resides in the sandbox. For better protection, you are advised to use _Direct Access_ rather than _Full Access_ whenever possible.

Related [Sandboxie Ini](SandboxieIni.md) settings: [OpenPipePath](OpenPipePath.md)

#### File Access > Read-Only Access

This access mode excludes the effects of sandboxing on a file (or folder) resource, while allowing a program to read, but not modify, the real resource.

Related [Sandboxie Ini](SandboxieIni.md) settings: [ReadFilePath](ReadFilePath.md)

#### File Access > Write-Only Access

This access mode hides all files and folders which are located within the selected folder outside the sandbox. However, programs in the sandbox can create new files within the corresponding folder in the sandbox.

This setting can only be used effectively on folders. If a file is selected, the effect is the same as the Blocked Access setting (see below).

Related [Sandboxie Ini](SandboxieIni.md) settings: [WriteFilePath](WriteFilePath.md)

#### File Access > Blocked Access

Deny all access to the resource, for example to a folder containing sensitive data. _Blocked Access_ settings take precedence over all other resource access rules. For example, if an exclusion for **C:\Downloads** appears in both _Direct Access_ and _Blocked Access_, the latter will apply, denying all access to the folder.

Related [Sandboxie Ini](SandboxieIni.md) settings: [ClosedFilePath](ClosedFilePath.md)

* * *

### Registry Access

[Sandboxie Control](SandboxieControl.md) > [Sandbox Settings](SandboxSettings.md) > Resource Access > Registry Access

This category manages registry key resources. The registry is a mechanism provided by Windows for programs to store configuration and settings.

See [General Information](ResourceAccessSettings.md#general-information) above for more information about editing resources and associating resources with particular programs.

#### Registry Access > Direct Access

Allow direct access to a registry key resource. Note that _Direct Access_ exclusions do not apply when the program itself resides in the sandbox. This is described in more detail in the File Access category above. Note that unlike in the File Access category, there is no _Full Access_ access mode for registry keys.

Related [Sandboxie Ini](SandboxieIni.md) settings: [OpenKeyPath](OpenKeyPath.md)

#### Registry Access > Read-Only Access

This access mode excludes the effects of sandboxing on a registry key resource, while allowing a program to read, but not modify, the real resource.

Related [Sandboxie Ini](SandboxieIni.md) settings: [ReadKeyPath](ReadKeyPath.md)

#### Registry Access > Write-Only Access

This access mode hides all registry data which is located within the selected registry key outside the sandbox. However, programs in the sandbox can create new registry data within the corresponding folder in the sandbox.

Related [Sandboxie Ini](SandboxieIni.md) settings: [WriteKeyPath](WriteKeyPath.md)

#### Registry Access > Blocked Access

Deny all access to a registry key resource, for example to a key containing Windows policy settings. _Blocked Access_ settings take precedence over all other resource access rules. For example, if an exclusion for a registry key appears in both _Direct Access_ and _Blocked Access_, the latter will apply, denying all access to the registry key.

Related [Sandboxie Ini](SandboxieIni.md) settings: [ClosedKeyPath](ClosedKeyPath.md)

* * *

### IPC Access

[Sandboxie Control](SandboxieControl.md) > [Sandbox Settings](SandboxSettings.md) > Resource Access > IPC Access

This category manages exclusions for NT IPC objects. These resources are created by programs running the system as a way to coordinate operations or otherwise communicate.

See [General Information](ResourceAccessSettings.md#general-information) above for more information about editing resources and associating resources with particular programs.

#### IPC Access > Direct Access

Allow direct access to an IPC object resource. Note that unlike in the File Access and Registry Access categories, _Direct Access_ exclusions for IPC objects always apply to all sandboxed programs.

Related [Sandboxie Ini](SandboxieIni.md) settings: [OpenIpcPath](OpenIpcPath.md)

#### IPC Access > Blocked Access

Deny all access to an IPC object resource. _Blocked Access_ settings take precedence over all other resource access rules. For example, if an exclusion for an IPC object appears in both _Direct Access_ and _Blocked Access_, the latter will apply, denying all access to the object.

This setting can be used to override default _IPC Access > Direct Access_ settings in Sandboxie, and block the access. For example, by default Sandboxie allows sandboxed programs to access the audio device. To override this and cut off audio output by sandboxed programs, add an exclusion for **\RPC Control\AudioSrv**.

Related [Sandboxie Ini](SandboxieIni.md) settings: [ClosedIpcPath](ClosedIpcPath.md)

* * *

### Window Access

[Sandboxie Control](SandboxieControl.md) > [Sandbox Settings](SandboxSettings.md) > Resource Access > Window Access

This category manages exclusions for window classes. These resources are primarily related to windows displayed on the screen, but can also be used by programs as a way to coordinate operations or otherwise communicate. You can specify which window classes, that were created outside the sandbox, will be available for use by sandboxed programs.

See [General Information](ResourceAccessSettings.md#general-information) above for more information about editing resources and associating resources with particular programs.

Related [Sandboxie Ini](SandboxieIni.md) settings: [OpenWinClass](OpenWinClass.md)

* * *

### COM Access

[Sandboxie Control](SandboxieControl.md) > [Sandbox Settings](SandboxSettings.md) > Resource Access > COM Access

This category manages exclusions for COM classes. These resources represent objects which are used as a way to coordinate operations or otherwise communicate. You can specify the COM class identifiers for those COM objects that exist outside the sandbox, and which should be accessible to sandboxed programs.

See [General Information](ResourceAccessSettings.md#general-information) above for more information about editing resources and associating resources with particular programs.

Related [Sandboxie Ini](SandboxieIni.md) settings: [OpenClsid](OpenClsid.md)
