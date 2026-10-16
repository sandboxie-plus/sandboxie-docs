# SBIE DLL API

This page describes the callable entrypoints in the _SbieDll.dll_ dynamically-linked library (DLL). These entrypoints expose some functionality of Sandboxie that can be accessed programmatically, that is, through other programs rather than through a person interacting with Sandboxie.

There are three aspects to using Sandboxie programmatically:

*   Driving some functionality using the Start.exe program. See [Start Command Line](StartCommandLine.md).
*   Injecting custom DLLs into sandboxed programs. See [InjectDll](InjectDll.md).
*   Calling Sandboxie entrypoints from programs running (sandboxed or not). Described here.

The entrypoints described here are exported by _SbieDll.dll_. Load the DLL appropriate for the caller's architecture and resolve the exact export name with `GetProcAddress`. Use a function-pointer signature matching the installed DLL: argument count and order, scalar versus pointer types, pointer widths, and calling convention all matter. These declarations describe current source, not an ABI guarantee across arbitrary releases.

The x86 build uses `__stdcall`; its [export definitions](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/SboxDll32.def) provide undecorated public names mapped to decorated implementation symbols. Other architectures use their platform ABI and compiler exports; do not apply x86 name decoration to them. The current declarations are in [sbieapi.h](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/sbieapi.h) and [sbiedll.h](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/sbiedll.h).

This lookup fragment uses the injected DLL's supplied SbieDll handle. Application-specific target setup is omitted; the hook example below shows the four-argument call.

```c
#include <windows.h>

typedef void *(__stdcall *P_SbieDll_Hook)(
    const char *name, void *source, void *detour, HMODULE module);

__declspec(dllexport) void __stdcall InjectDllMain(
    HINSTANCE hSbieDll, ULONG_PTR UnusedParameter)
{
    P_SbieDll_Hook p_SbieDll_Hook =
        (P_SbieDll_Hook)(ULONG_PTR)GetProcAddress(hSbieDll, "SbieDll_Hook");
    (void)UnusedParameter;
    if (!p_SbieDll_Hook)
        return;

    /* After resolving the target, detour, and associated module:
       p_SbieDll_Hook(name, source, detour, module); */
}
```

Note the use of _InjectDllMain_ (see [Inject Dll](InjectDll.md)) to get a handle to the loaded instance of SbieDll. That is the recommended approach. However, using LoadLibrary or GetModuleHandle to look up SbieDll by name is also fine.

Resolving an export does not establish that it can be used in every caller context. Driver/service availability, authorization, sandbox context, and initialization requirements differ by API. Check each result; these APIs do not share a universal `GetLastError()` contract. The examples are not runtime or distributed-DLL compatibility guarantees, including on ARM64 or ARM64EC.

* * *

### Enumerate Sandbox Names

*    Prototype:
```
        typedef LONG (__stdcall *P_SbieApi_EnumBoxes)(
                LONG index,                 // initialize to -1
                WCHAR *box_name);           // pointer to WCHAR [40]
```

*    Export Name:
```
        SbieApi_EnumBoxes
```

*    Parameters:
```
        index [in] specifies which sandbox to return.  Initialize to -1.
        Eligible configured sandboxes are returned in loaded configuration-
        section order, not a permanent physical INI-file ordering contract.

        box_name [out] receives a null-terminated sandbox name on success.
        Supply storage for 40 WCHARs. Disabled or ineligible sections are
        not necessarily returned.

        Note: this is not a general box-name enumerator for sandboxed
        callers: their underlying empty-section query resolves to their
        own box rather than enumerating configuration sections.
```

*    Return Value:
```
        Returns the next value to use for the index parameter.
        Returns -1 to stop enumeration. This sentinel does not distinguish
        exhaustion from every underlying configuration-query failure.
```


*    Sample Code:

```
        WCHAR name[40];
        LONG index = -1;
        while (1) {
                index = SbieApi_EnumBoxes(index, name);
                if (index == -1)
                    break;
                SandboxNames_StringArray.add(name); // application-specific pseudocode
        }
```

* * *

### Query Sandbox Paths by Sandbox Name

*    Prototype:
```
        typedef LONG (__stdcall *P_SbieApi_QueryBoxPath)(
                const WCHAR *box_name,      // padded WCHAR [40] input
                WCHAR *file_path,
                WCHAR *key_path,
                WCHAR *ipc_path,
                ULONG *file_path_len,
                ULONG *key_path_len,
                ULONG *ipc_path_len);
```

*    Export Name:
```
        SbieApi_QueryBoxPath
```

*    Parameters:
```
        box_name [in] specifies the name of the sandbox for which
        to construct path information for an unsandboxed caller. Supply
        an explicit name in a padded WCHAR [40] buffer. A sandboxed caller
        uses its existing box, irrespective of this argument; NULL is not
        a universally valid current-box selector.

        file_path [out] receives the path to the root directory of
        the sandbox, as set by the FileRootPath setting.
        The buffer receives at most the number of bytes specified
        by the file_path_len parameter.  Pass NULL to ignore this
        parameter.

        key_path [out] receives the path to the root key of the
        sandbox registry, as set by the KeyRootPath setting.
        The buffer receives at most the number of bytes specified
        by the key_path_len parameter.  Pass NULL to ignore this
        parameter.

        ipc_path [out] receives the path to the root object directory
        of the sandbox, as set by the IpcRootPath setting.
        The buffer receives at most the number of bytes specified
        by the ipc_path_len parameter.  Pass NULL to ignore this
        parameter.

        file_path_len [in/out] specifies the length in bytes of the
        file_path buffer.  On return, receives the length in bytes
        needed to receive a complete buffer.

        key_path_len [in/out] specifies the length in bytes of the
        key_path buffer.  On return, receives the length in bytes
        needed to receive a complete buffer.

        ipc_path_len [in/out] specifies the length in bytes of the
        ipc_path buffer.  On return, receives the length in bytes
        needed to receive a complete buffer.

        Required lengths include the null terminator. Each supplied output
        buffer requires its corresponding length pointer. With an output
        omitted, its length pointer can request the required size; both
        may be NULL when that path is not needed.

        Output capacities pass through USHORT (16-bit byte) fields.
        Paths are expanded native filesystem, Registry, and object paths,
        not necessarily DOS paths or the literal INI setting text.
```

*    Return Value:
```
        Returns zero on success, a non-zero value on error.
```

The [path-query consumer](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/drv/process_api.c#L601-L755) writes required lengths before copying strings. Insufficient buffers fail; do not use output strings unless the call succeeds.

*    Sample Code:

This helper assumes `query` was resolved with the prototype above. Replace `DefaultBox` with the intended configured box; not every installation has that name. On success, the caller owns all three allocations and must `free` them. Configuration can change between calls, so failure may require repeating the size query.

```c
#include <windows.h>
#include <stdlib.h>
#include <limits.h>

LONG ReadBoxPaths(P_SbieApi_QueryBoxPath query,
                  WCHAR **file, WCHAR **key, WCHAR **ipc)
{
    WCHAR box[40] = L"DefaultBox";
    ULONG FileLen = 0, KeyLen = 0, IpcLen = 0;
    WCHAR *FileBuf = NULL, *KeyBuf = NULL, *IpcBuf = NULL;
    LONG status;

    if (!query || !file || !key || !ipc)
        return (LONG)0xC000000DL; /* STATUS_INVALID_PARAMETER */
    *file = NULL; *key = NULL; *ipc = NULL;

    status = query(box, NULL, NULL, NULL, &FileLen, &KeyLen, &IpcLen);
    if (status != 0)
        return status;
    if (FileLen < sizeof(WCHAR) || KeyLen < sizeof(WCHAR) ||
        IpcLen < sizeof(WCHAR) || FileLen > USHRT_MAX ||
        KeyLen > USHRT_MAX || IpcLen > USHRT_MAX ||
        FileLen % sizeof(WCHAR) || KeyLen % sizeof(WCHAR) ||
        IpcLen % sizeof(WCHAR))
        return (LONG)0xC000000DL;

    FileBuf = (WCHAR *)malloc(FileLen);
    KeyBuf = (WCHAR *)malloc(KeyLen);
    IpcBuf = (WCHAR *)malloc(IpcLen);
    if (!FileBuf || !KeyBuf || !IpcBuf) {
        status = (LONG)0xC0000017L; /* STATUS_NO_MEMORY */
        goto fail;
    }
    status = query(box, FileBuf, KeyBuf, IpcBuf, &FileLen, &KeyLen, &IpcLen);
    if (status != 0)
        goto fail;
    *file = FileBuf; *key = KeyBuf; *ipc = IpcBuf;
    return 0;

fail:
    free(FileBuf); free(KeyBuf); free(IpcBuf);
    return status;
}
```

Use `wcslen` on successful outputs if character counts are needed; keep those counts separate from the byte capacities used for API calls.

* * *

### Query Sandbox Paths by Process ID

*    Prototype:
```
        typedef LONG (__stdcall *P_SbieApi_QueryProcessPath)(
                HANDLE process_id,
                WCHAR *file_path,
                WCHAR *key_path,
                WCHAR *ipc_path,
                ULONG *file_path_len,
                ULONG *key_path_len,
                ULONG *ipc_path_len);
```

*    Export Name:
```
        SbieApi_QueryProcessPath
```

*    Parameters:
```
        process_id [in] specifies the ID of the sandboxed process to query,
        not an opened process handle. Convert a numeric PID using
        (HANDLE)(ULONG_PTR)pid. An unsandboxed caller must supply an explicit
        tracked sandboxed PID. A sandboxed caller can use NULL or
        (HANDLE)(LONG_PTR)-1 for its current process.

        file_path [out]

        key_path [out]

        ipc_path [out]

        file_path_len [in/out]

        key_path_len [in/out]

        ipc_path_len [in/out]

        The last six parameters are similar to the last six parameters for
        the QueryBoxPath function, discussed above.  However, QueryProcessPath
        (this function) returns the sandbox paths that are in use by a running
        program. An unsandboxed QueryBoxPath caller instead constructs paths
        from the currently loaded configuration and its identity/session.

        Or put another way:  Suppose a sandboxed program starts with PID 124,
        and then some sandbox path (for instance FileRootPath) is set to a
        new value and configuration is reloaded. An unsandboxed named-box
        QueryBoxPath call can return the new configured path, while
        QueryProcessPath for PID 124 returns its existing path. A sandboxed
        QueryBoxPath caller still uses its own existing box.
```

*    Return Value:
```
        Returns zero on success, a non-zero value on error.
```

The [process-path consumer](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/drv/process_api.c#L653-L698) can fail with `STATUS_INVALID_CID` for a missing, unsandboxed, or terminated target. A PID obtained through enumeration is not a process-lifetime guarantee.

* * *

### Enumerate Running Processes

*    Prototype:
```
        typedef LONG (__stdcall *P_SbieApi_EnumProcessEx)(
                const WCHAR *box_name,      // padded WCHAR [40] input, or NULL
                BOOLEAN all_sessions,
                ULONG which_session,
                ULONG *boxed_pids,         // pointer to ULONG []
                ULONG *boxed_count);
```

*    Export Name:
```
        SbieApi_EnumProcessEx
```

*    Parameters:
```
        box_name [in] specifies the name of the sandbox in which
        processes will be enumerated. An unsandboxed caller can supply NULL
        or an empty name for all boxes. A sandboxed caller is restricted
        to its own box, regardless of the supplied name.

        all_sessions [in] specifies TRUE to enumerate processes in all
        logon sessions, or FALSE for a particular logon session.

        which_session [in] specifies the logon session number in which
        processes will be enumerated. Ignored if all_sessions is TRUE.
        Pass (ULONG)-1 to specify the current logon session. These session
        arguments still apply when the caller is restricted to its own box.

        boxed_pids [out] receives the process ID (PID) numbers.
        Its layout depends on boxed_count, as shown below.

        boxed_count [in/out], when supplied with a PID array, specifies
        the array's capacity in ULONG elements and receives the number
        of PIDs written. With a NULL PID array it requests a count only.
```

| Mode | Required input | Output layout |
|---|---|---|
| `boxed_count == NULL` | Fixed `ULONG pids[512]` | `pids[0]` is count; PIDs start at `pids[1]`; at most 511 PIDs |
| Count pointer and PID array supplied | Initial `*boxed_count` is array capacity | PIDs start at `pids[0]`; returned `*boxed_count` is number written |
| Count pointer supplied, PID array `NULL` | Writable count output | Count only; not guaranteed to equal a subsequent list result |

The [driver enumeration](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/drv/process_api.c#L983-L1127) can return success after exhausting capacity; success does not prove the list is complete. Count-only and PID-list paths differ, and processes can start or terminate between calls. Supplying neither output pointer is invalid.

`SbieApi_EnumProcess(box, pids)` is a header macro wrapping `SbieApi_EnumProcessEx(box, FALSE, -1, pids, NULL)`, using the legacy layout. It is not a separate export to resolve with `GetProcAddress`.

*    Return Value:
```
       Returns zero on success, a non-zero value on error.
```

* * *

### Query Process Information

*    Prototype:
```
        typedef LONG (__stdcall *P_SbieApi_QueryProcess)(
                HANDLE process_id,
                WCHAR *box_name,            // pointer to WCHAR [40]
                WCHAR *image_name,          // pointer to WCHAR [96]
                WCHAR *sid_string,          // pointer to WCHAR [96]
                ULONG *session_id);
```

*    Export Name:
```
        SbieApi_QueryProcess
```


*    Parameters:
```
        process_id [in] is a PID represented as (HANDLE)(ULONG_PTR)pid,
        not an opened process handle. Unsandboxed callers must supply an
        explicit target. Sandboxed callers can use NULL or
        (HANDLE)(LONG_PTR)-1 for their current process.

        box_name [out] receives the name of the sandbox in which the
        process is running.  Pass NULL to ignore this parameter.

        image_name [out] receives the process image name, not a full path.
        Supply 96 WCHARs, or pass NULL to ignore this parameter. A longer
        image name can fail rather than fit this fixed buffer; newer
        QueryProcessEx variants allow an explicit image-buffer capacity.

        sid_string [out] receives the SID string for the process.
        Pass NULL to ignore this parameter.

        session_id [out] receives the logon session number in which
        the process is running.  Pass NULL to ignore this parameter.

        Successfully copied strings include a null terminator. Box-name
        and SID outputs require 40 and 96 WCHARs respectively.
```


*    Return Value:
```
        Returns zero on success, a non-zero value on error.
```


The [process query](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/drv/process_api.c#L208-L319) can fail for a missing, unsandboxed, or terminated PID, including a process that disappeared after enumeration. On ordinary failure, the DLL clears requested strings and resets a supplied session output to zero.

* * *

### Terminate a Single Sandboxed Process

*    Prototype:
```
        typedef BOOLEAN (__stdcall *P_SbieDll_KillOne)(
                ULONG process_id);
```


*    Export Name:
```
        SbieDll_KillOne
```


*    Parameters:
```
        process_id [in] specifies the process ID for the sandboxed
        process that should be terminated, as a 32-bit ULONG.
```


*    Return Value:
```
        Returns TRUE on success, FALSE on failure.

        The DLL requests termination through SbieSvc. TRUE represents a
        successful service response, not a completed process-exit wait.
```

The [service handler](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/svc/ProcessServer.cpp#L129-L239) requires a tracked sandboxed target. Cross-session requests require administrator authorization, and sandboxed callers cannot target another box through this handler. Missing or already-terminated targets can fail. No particular exit code or uniform `GetLastError()` result is promised.


* * *

### Terminate All Sandboxed Processes

*    Prototype:
```
        typedef BOOLEAN (__stdcall *P_SbieDll_KillAll)(
                ULONG session_id,
                const WCHAR *box_name);
```


*    Export Name:
```
        SbieDll_KillAll
```


*    Parameters:
```
        session_id [in] specifies the logon session number in which
        sandboxed programs should be terminated. Specify (ULONG)-1 for
        the caller's current session. An explicit different session is
        subject to administrator authorization.

        box_name [in] specifies the sandbox name in which sandboxed
        programs should be terminated. NULL uses the caller's initialized
        SbieDll box name; it does not mean all boxes. Empty names are
        rejected by the service. Sandboxed callers are restricted to
        their own box.
```


*    Return Value:
```
        Returns TRUE on success, FALSE on failure.

        The service repeatedly enumerates matching processes and attempts
        termination. TRUE reflects its response, not a guarantee that
        every process has already exited or that no new process can appear.
```

This is a concrete box/session request, not a universal all-box/all-session operation. Higher-level all-box callers iterate boxes. See the [service implementation](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/svc/ProcessServer.cpp#L248-L374).


* * *

### Query Configuration from Sandboxie.ini

*    Prototype:
```
        typedef LONG (__stdcall *P_SbieApi_QueryConf)(
                const WCHAR *section_name,  // up to 64 characters
                const WCHAR *setting_name,  // pointer to WCHAR [66]
                ULONG setting_index,
                WCHAR *value,
                ULONG value_len);
```


*    Export Name:
```
        SbieApi_QueryConf
```


*    Parameters:
```
        section_name [in] specifies the section name that contains
        the setting to query. An empty or NULL section resolves to the
        caller's box inside a sandbox. Outside a sandbox, an empty section
        with a named setting queries GlobalSettings.

        setting_name [in] specifies the setting name to query. An empty
        setting with a named section enumerates setting names; outside a
        sandbox, both names empty enumerate section names.

        setting_index [in] specifies the zero-based index number
        for a setting that may appear multiple times. The lower 24 bits
        carry the index. The index
        number can be logically OR'ed with these special values:

            0x40000000 (CONF_GET_NO_GLOBAL) - suppress GlobalSettings
            fallback.

            0x20000000 (CONF_GET_NO_EXPAND) - do not expand variables.

            0x10000000 (CONF_GET_NO_TEMPLS) - ignore template-origin
            settings.

        value [out] receives a null-terminated value on success. Supply
        writable storage; NULL does not provide a size-query mechanism.

        value_len [in] specifies the maximum length in bytes of
        the buffer pointed to by value, including terminator space.
        It passes through a USHORT capacity field; insufficient storage
        fails rather than returning a required size.
```

This queries the driver's loaded configuration. Applicable template values and global fallback can participate unless suppressed. Variable expansion uses the caller's sandbox context or, outside a sandbox, its identity/session and requested section. `SbieApi_QueryConfAsIs` is a header wrapper that suppresses expansion only; it does not inherently disable templates or global fallback. See the [configuration consumer](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/drv/conf.c#L1824-L1968).


*    Return Value:
```
        Returns zero on success.  Returns 0xC000008B if the setting
        was not found.  Any other return value indicates some other error.
```


* * *

### Update Configuration in Sandboxie.ini

*    Prototype:
```
        typedef ULONG (__stdcall *P_SbieDll_UpdateConf)(
                WCHAR operation_code,
                const WCHAR *password,
                const WCHAR *section_name,
                const WCHAR *setting_name,
                const WCHAR *value);
```


*    Export Name:
```
        SbieDll_UpdateConf
```


*    Parameters:
```
        operation_code [in] specifies how to update the requested setting:
        's' to set (overwrite), replacing any existing values
        'a' to append the new value at the bottom of a list of values
            (or simply set the new value if there isn't one already)
        'i' to insert the new value at the top of a list of values
            (or simply set the new value if there isn't one already)
        'd' to delete an existing value in a list of values

        password [in] specifies the password to use if one is required,
        or NULL or an empty string otherwise.

        section_name [in] is a required parameter which specifies the
        section name that contains the setting to set. An empty string
        selects GlobalSettings; NULL is invalid.

        setting_name [in] is a required parameter which specifies the
        setting name to set.

        value [in] is an optional parameter specifying the new value.

        With 's' or 'd', a NULL or empty value deletes all occurrences of
        the named setting. With setting_name L"*", that combination deletes
        the complete section. With 'a' or 'i', a NULL or empty value adds
        nothing.

        Keep password, section, and setting strings within 64 WCHAR
        characters excluding the terminator. The caller must ensure safe
        lengths; do not rely on rejection of oversized inputs. Values must
        also fit configuration-line and request-size constraints.
```


*    Return Value:
```
        Returns zero on success, a non-zero status on error.
```

This is the service-backed INI updater. Sandboxed callers are rejected; applicable administrator/password restrictions are checked by the service. Accepted changes request a save and configuration refresh, but this is not an atomic transaction: failures do not guarantee unchanged state, and a zero result must not be treated as independent confirmation of every disk write or running consumer's refresh. See the [DLL request](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/callsvc.c#L873-L934) and [service save/reload workflow](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/svc/sbieiniserver.cpp#L1276-L1384).

The [service mutation handlers](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/svc/sbieiniserver.cpp#L1036-L1103) distinguish deleting one nonempty value from deleting all occurrences or a section. Check NULL and empty arguments carefully before updating configuration.

Do not confuse it with `SbieApi_UpdateConf`: that separate four-argument driver-memory updater uses numeric operations and different authorization, without this INI persistence workflow. Its current wrapper requires a valid value string; the DLL updater's NULL-value behavior does not apply to it.


* * *

### Reload Configuration from Sandboxie.ini

*    Prototype:
```
        typedef LONG (__stdcall *P_SbieApi_ReloadConf)(
                ULONG session_id,
                ULONG flags);
```


*    Export Name:
```
        SbieApi_ReloadConf
```


*    Parameters:
```
        session_id [in] specifies the logon session number to which
        Sandboxie will log any error messages. Pass (ULONG)-1 for the
        current session; this does not select independent per-session
        configuration.

        flags [in] selects the operation:
        0 - ordinary configuration reload.
        SBIE_CONF_FLAG_RECONFIGURE (0x1) - also evaluate selected driver
            reconfiguration behavior.
        SBIE_CONF_FLAG_RELOAD_CERT (0x80000000) - certificate validation.
            This takes a separate early branch, not an ordinary INI reload,
            including when combined with other flags.
```


*    Return Value:
```
        Returns zero on success, a non-zero value on error.
```


Sandboxed callers receive `STATUS_NOT_IMPLEMENTED`. A missing INI file can reset the driver's configuration and return success. Ordinary reload updates driver configuration and notifies the service, but does not universally rebuild existing process/box objects, refresh process-local caches, or reinstall hooks. Consult each setting's lifecycle instead of assuming either immediate update or a universal restart requirement. See the [reload consumer](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/drv/conf.c#L1696-L1815).

For a previously resolved function pointer, an illustrative ordinary reload is:

```c
LONG status = p_SbieApi_ReloadConf((ULONG)-1, 0);
if (status != 0) {
    /* Handle the returned status. */
}
```

* * *

### Hook a User-Mode Entrypoint

*    Prototype:
```
        typedef void *(__stdcall *P_SbieDll_Hook)(
                const char *name,
                void *source_func,
                void *detour_func,
                HMODULE module);
```


*    Export Name:
```
        SbieDll_Hook
```


*    Parameters:
```
        name [in] specifies an ASCII-string naming the entrypoint to
        be hooked. It is used for diagnostics and skip-hook matching.

        source_func [in] pointer to the function to hook.

        detour_func [in] pointer to the hook code.

        module [in] is the associated module handle, used for tracing and
        module-associated hook/resource management. It is not unused.

        When installed, a detour intercepts calls through the hooked
        entrypoint. Hook installation is not guaranteed for every Windows
        entrypoint, caller context, instruction sequence, or architecture.
```


*    Return Value:
```
        Returns a function pointer which can be used by the detour
        function to invoke the source function, or NULL on failure.
        The skip-hook path returns source_func unchanged, so a non-NULL
        result does not universally prove that a detour was installed.
```

Keep detour code and associated modules alive while the hook is in use. Sandboxie manages module-associated trampoline resources; do not free them manually or use them after their module/resource lifetime. See the [hook implementation](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/dllhook.c#L1308-L1472) and [module cleanup](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/dllhook.c#L1577-L1613).


*    Sample Code:

This uses `P_SbieDll_Hook` above and an already loaded SbieDll handle. The drive-prefix test is illustrative, not a complete filesystem security policy. The application must arrange an appropriate initialization context and control concurrent calls during hook setup.

```c
#include <windows.h>

typedef BOOL (__stdcall *P_DeleteFileW)(const WCHAR *Path);
static P_DeleteFileW pDeleteFileW = NULL;

BOOL __stdcall MyDeleteFileW(const WCHAR *Path)
{
    if (!pDeleteFileW) {
        SetLastError(ERROR_INVALID_FUNCTION);
        return FALSE;
    }
    if (Path && (Path[0] == L'C' || Path[0] == L'c') && Path[1] == L':') {
        SetLastError(0);
        return TRUE; /* Illustrative suppression of this spelling only. */
    }
    return pDeleteFileW(Path);
}

BOOL InstallDeleteFileHook(HMODULE hSbieDll)
{
    HMODULE module = GetModuleHandleW(L"kernel32.dll");
    P_SbieDll_Hook hook;
    void *source, *original;
    if (!hSbieDll || !module)
        return FALSE;
    hook = (P_SbieDll_Hook)(ULONG_PTR)GetProcAddress(hSbieDll, "SbieDll_Hook");
    source = (void *)(ULONG_PTR)GetProcAddress(module, "DeleteFileW");
    if (!hook || !source)
        return FALSE;
    original = hook("DeleteFileW", source, (void *)(ULONG_PTR)MyDeleteFileW, module);
    if (!original)
        return FALSE;
    pDeleteFileW = (P_DeleteFileW)(ULONG_PTR)original;
    return TRUE; /* A skip-hook result does not mean the detour is active. */
}
```


* * *

### Register for DLL Load/Unload Callbacks

*    Prototype:
```
       typedef BOOLEAN (__stdcall *P_SbieDll_RegisterDllCallback)(
               void *Callback);
```

The legacy Vista-and-later dispatcher uses this callback shape; the historical XP dispatcher instead uses `const WCHAR *` for the first argument:

```
       typedef void (__stdcall *P_DllCallback)(
               const UCHAR *ImageName,
               HMODULE ImageBase,
               BOOL LoadState);
```


*    Export Name:
```
       SbieDll_RegisterDllCallback

       Historical documentation identifies Sandboxie 3.46 as its first
       availability; that attribution does not guarantee current delivery.
```


*    Parameters:
```
       Callback specifies a process-local callback for the legacy dispatcher.
       Appropriate Sandboxie loader initialization is required; simply
       loading SbieDll in an unsandboxed program is not equivalent.
       No unregister API is established. Keep the callback code alive.
```

```
       The ImageName (first) parameter to the callback function
       specifies an ANSI DLL basename for the legacy Vista-and-later
       dispatcher, not a full path. XP used a wide-character name.
       Treat the name as borrowed data for the duration of the callback.
```

```
       The ImageBase (second) parameter to the callback function
       specifies the module base. Legacy unload notifications retain the
       old module base; do not use zero as the event discriminator.

       LoadState (third) is TRUE for load and FALSE for unload.
```


*    Return Value:
```
       Returns TRUE on success, FALSE if the callback cannot be registered.
       Registration does not replay already loaded modules. Capacity is
       limited: the current eight-slot table includes Sandboxie's own
       callback, and duplicate registrations consume additional slots.
```

On Windows 8.1 and later, the current loader-notification path does not normally dispatch through this legacy registration table. Registration success therefore does not guarantee DLL-event notifications on modern Windows. Do not treat this as a universal loader-notification facility. See [loader initialization](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/ldr.c#L387-L475), [registration and legacy dispatch](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/ldr.c#L535-L608), and [modern notification handling](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/ldr.c#L283-L295).


* * *

### Get Sandboxie Home Folder

*    Prototype:
```
       typedef LONG (__stdcall *P_SbieApi_GetHomePath)(
               WCHAR *NtPath,
               ULONG NtPathMaxLen,
               WCHAR *DosPath,
               ULONG DosPathMaxLen);
```


*    Export Name:
```
       SbieApi_GetHomePath

       Historical documentation identifies Sandboxie 3.52 as its first
       availability.
```


*    Parameters:
```
       NtPath specifies a pointer to a buffer which will receive the
       full path of the Sandboxie installation folder in NT-path syntax.

       NtPathMaxLen specifies capacity in WCHAR elements, including space
       for the null terminator, not bytes. Specify
       NULL for NtPath and zero for NtPathMaxLen to not receive the
       NT path.

       DosPath specifies a pointer to a buffer which will receive the
       full path of the Sandboxie installation folder in DOS-path syntax.

       DosPathMaxLen likewise specifies capacity in WCHAR elements. Specify
       NULL for DosPath and zero for DosPathMaxLen to not receive the
       DOS path.
```


*    Return Value:
```
       Returns zero on success, a non-zero value on error.

       STATUS_BUFFER_TOO_SMALL (0xC0000023) indicates either NtPathMaxLen
       or DosPathMaxLen specifies a buffer that is too small.  Increase
       the size of the input buffer and retry the call.
```

The outputs are independently optional, but omitted outputs do not return required lengths. The [wrapper](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/sbieapi.c#L484-L516) converts WCHAR capacities through 16-bit byte fields; do not supply arbitrary oversized maxima. Do not assume every installation path fits a chosen fixed array.
