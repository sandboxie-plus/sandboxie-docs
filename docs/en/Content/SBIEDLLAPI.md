# SBIE DLL API

This page describes the callable entrypoints in the _SbieDll.dll_ dynamically-linked library (DLL). These entrypoints expose some functionality of Sandboxie that can be accessed programmatically, that is, through other programs rather than through a person interacting with Sandboxie.

There are three aspects to using Sandboxie programmatically:

*   Driving some functionality using the Start.exe program. See [Start Command Line](StartCommandLine.md).
*   Injecting custom DLLs into sandboxed programs. See [InjectDll](InjectDll.md).
*   Calling Sandboxie entrypoints from programs running (sandboxed or not). Described here.

The entrypoints described here are all exported by _SbieDll.dll_. To access an entrypoint, you should dynamically load this DLL into your program, and get the address of the desired entrypoint. For example,
```
        __declspec(dllexport) void __stdcall InjectDllMain(HINSTANCE hSbieDll, ULONG_PTR UnusedParameter)
	{
		//
	        // locate the address of SbieDll_Hook in SbieDll.dll
	        //

	        typedef void *(__stdcall *P_SbieDll_Hook)(
	                const char *ApiName, void *ApiFunc, void *NewFunc);

	        P_SbieDll_Hook p_SbieDll_Hook = GetProcAddress(hSbieDll, "SbieDll_Hook");

		//
	        // invoke SbieDll_Hook through the function pointer
	        //

	        p_SbieDll_Hook(...);
	}
```

Note the use of _InjectDllMain_ (see [Inject Dll](InjectDll.md)) to get a handle to the loaded instance of SbieDll. That is the recommended approach. However, using LoadLibrary or GetModuleHandle to look up SbieDll by name is also fine.

* * *

### Enumerate Sandbox Names

*    Prototype:
```
        typedef LONG (__stdcall *P_SbieApi_EnumBoxes)(
                LONG index,                 // initialize to -1
                WCHAR *box_name);           // pointer to WCHAR [34]
```

*    Export Name:
```
        SbieApi_EnumBoxes
```

*    Parameters:
```
        index [in] specifies which sandbox to return.  Initialize to -1.
        Sandboxes are enumerated in the order they appear in Sandboxie.ini.

        box_name [out] receives the sandbox name.

        Note:  this function cannot be used by a sandboxed program.
```

*    Return Value:
```
        Returns the next value to use for the index parameter.
        Returns -1 when there is nothing left to enumerate.
```


*    Sample Code:

```
        WCHAR name[34];
        int index = -1;
        while (1) {
                index = SbieApi_EnumBoxes(index, name);
                if (index == -1)
                    break;
                SandboxNames_StringArray.add(name);
        }
```

* * *

### Query Sandbox Paths by Sandbox Name

*    Prototype:
```
        typedef LONG (__stdcall *P_SbieApi_QueryBoxPath)(
                const WCHAR *box_name,      // pointer to WCHAR [34]
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
        to return path information.

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
```

*    Return Value:
```
        Returns zero on success, a non-zero value on error.
```

*    Sample Code:
```
        ULONG FileLen = 0;
        ULONG KeyLen  = 0;
        ULONG IpcLen  = 0;

        SbieApi_QueryBoxPath(
                NULL, NULL, NULL, NULL, &FileLen, &KeyLen, &IpcLen);

        // note that lengths are returned as the number of bytes,
        // rather than number of WCHAR characters

        WCHAR *FileBuf = malloc(FileLen);
        WCHAR *KeyBuf = malloc(KeyLen);
        WCHAR *IpcBuf = malloc(IpcLen);

        SbieApi_QueryBoxPath(
                FileBuf, KeyBuf, IpcBuf, &FileLen, &KeyLen, &IpcLen);

        // now use wcslen to count the number of characters

        FileLen = wcslen(FileBuf);
        KeyLen  = wcslen(KeyBuf);
        IpcLen  = wcslen(IpcBuf);
```

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
        process_id [in] specifies the ID of the sandboxed process to query.

        file_path [out]

        key_path [out]

        ipc_path [out]

        file_path_len [in/out]

        key_path_len [in/out]

        ipc_path_len [in/out]

        The last six parameters are similar to the last six parameters for
        the QueryBoxPath function, discussed above.  However, QueryProcessPath
        (this function) returns the sandbox paths that are in use by a running
        program, whereas QueryBoxPath returns the paths as they are recorded
        in the Sandboxie configuration.

        Or put another way:  Suppose a sandboxed program starts with PID 124,
        and then some sandbox path (for instance FileRootPath) is set to a
        new value.  At this point, QueryBoxPath will return the new value, but
        QueryProcessPath for PID 124 will return the old value.
```

*    Return Value:
```
        Returns zero on success, a non-zero value on error.
```

* * *

### Enumerate Running Processes

*    Prototype:
```
        typedef LONG (__stdcall *P_SbieApi_EnumProcessEx)(
                const WCHAR *box_name,      // pointer to WCHAR [34]
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
        processes will be enumerated.

        all_sessions [in] specifies TRUE to enumerate processes in all
        logon sessions or only in a particular logon session

        which_session [in] specifies the logon session number in which
        processes will be enumerated.  Ignored if all_sessions if TRUE.
        Pass the value -1 to specify the current logon session.

        boxed_pids [out] receives the process ID (PID) numbers.
        The first ULONG receives the number of processes enumerated.
        The second ULONG receives the first PID, the third ULONG receives
        the second PID, and so on.
```

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
                WCHAR *box_name,            // pointer to WCHAR [34]
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
        process_id [in] specifies the ID of the sandboxed process to query.

        box_name [out] receives the name of the sandbox in which the
        process is running.  Pass NULL to ignore this parameter.

        image_name [out] receives the process name.  Pass NULL to ignore
        this parameter.

        sid_string [out] receives the SID string for the process.
        Pass NULL to ignore this parameter.

        session_id [out] receives the logon session number in which
        the process is running.  Pass NULL to ignore this parameter.
```


*    Return Value:
```
        Returns zero on success, a non-zero value on error.
```


* * *

### Terminate a Single Sandboxed Process

*    Prototype:
```
        typedef BOOLEAN (__stdcall *P_SbieDll_KillOne)(
                HANDLE process_id);
```


*    Export Name:
```
        SbieDll_KillOne
```


*    Parameters:
```
        process_id [in] specifies the process ID for the sandboxed
        process that should be terminated.
```


*    Return Value:
```
        Returns TRUE on success, FALSE on failure.

        The target process is terminated by the Sandboxie service
        (SbieSvc) with exit code 1 through a call to the Windows API
        TerminateProcess (ProcessId, 1).
```


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
        sandboxed programs should be terminated.

        box_name [in] specifies the sandbox name in which sandboxed
        programs should be terminated.  Specify -1 to indicate the
        current logon session.
```


*    Return Value:
```
        Returns TRUE on success, FALSE on failure.

        The target processes are terminated in the fashion described
        above; see SbieDll_KillOne.
```


* * *

### Query Configuration from Sandboxie.ini

*    Prototype:
```
        typedef LONG (__stdcall *P_SbieApi_QueryConf)(
                const WCHAR *section_name,  // pointer to WCHAR [34]
                const WCHAR *setting_name,  // pointer to WCHAR [66]
                ULONG setting_index,
                WCHAR *value,
                ULONG value_len)
```


*    Export Name:
```
        SbieApi_QueryConf
```


*    Parameters:
```
        section_name [in] specifies the section name that contains
        the setting to query.

        setting_name [in] specifies the setting name to query.

        setting_index [in] specifies the zero-based index number
        for a setting that may appear multiple times.  The index
        number can be logically OR'ed with these special values:

            0x40000000 - do not scan the [GlobalSettings] section
            if the specified setting name does appear in the
            specified section.

            0x20000000 - do not expand any variables in the result.

            0x10000000 - ignore any settings that originate from
            a template (typically defined in the Templates.ini file).
            only query those settings that appear explicitly in the
            Sandboxie.ini file.

        value [out] receives the value of the specified setting.

        value_len [in] specifies the maximum length in bytes of
        the buffer pointed to by the value parameter.
```


*    Return Value:
```
        Returns zero on success.  Returns 0xC000008B if the setting
        was not found.  Any other return value indicates some other error.
```


* * *

### Update Configuration in Sandboxie.ini

*    Prototype:
```
        typedef LONG (__stdcall *P_SbieDll_UpdateConf)(
        	WCHAR operation_code,
        	const WCHAR *password,      // limited to 64 chars
                const WCHAR *section_name,  // limited to 32 chars
                const WCHAR *setting_name,  // limited to 64 chars
                const WCHAR *value)         // limited to 2000 chars
```


*    Export Name:
```
        SbieDll_UpdateConf
```


*    Parameters:
```
        operation_code [in] specifies how to update the request setting:
        's' to set (overwrite), replacing any existing values
        'a' to append the new value at the bottom of a list of values
            (or simply set the new value if there isn't one already)
        'i' to insert the new value at the top of a list of values
            (or simply set the new value if there isn't one already)
        'd' to delete an existing value in a list of values

        password [in] specifies the password to use if one is required,
        or NULL or an empty string otherwise.

        section_name [in] is a required parameter which specifies the
        section name that contains the setting to set.

        setting_name [in] is a required parameter which specifies the
        setting name to set.

        value [ini] is an optional parameter specifies the new value.

        If operation_code is 's' and value is omitted, the corresponding
        setting in the specified section will be deleted.

        If operation_code is 's' and setting_name is "*" (wildcard star)
        and value is omitted, this function deletes a complete section
        from the configuration file.
```


*    Return Value:
```
        Returns zero on success.
```


* * *

### Reload Configuration from Sandboxie.ini

*    Prototype:
```
        typedef LONG (__stdcall *P_SbieApi_ReloadConf)(
                ULONG session_id);
```


*    Export Name:
```
        SbieApi_ReloadConf
```


*    Parameters:
```
        session_id [in] specifies the logon session number to which
        Sandboxie will log any error messages.  Pass -1 for the current
        logon session.
```


*    Return Value:
```
        Returns zero on success, a non-zero value on error.
```


* * *

### Hook a User-Mode Entrypoint

*    Prototype:
```
        typedef void *(__stdcall *P_SbieDll_Hook)(
                const char *name,
                void *source_func,
                void *detour_func);
```


*    Export Name:
```
        SbieDll_Hook
```


*    Parameters:
```
        name [in] specifies an ASCII-string naming the entrypoint to
        be hooked.  In case of error, SbieDll_Hook logs a Sandboxie
        error message which includes this descriptive name.

        source_func [in] pointer to the function to hook.

        detour_func [in] pointer to the hook code.

        This function will cause the source function to invoke the detour
        function.  In other words, the detour function will intercept all
        calls to the source function.
```


*    Return Value:
```
        Returns a function pointer which can be used by the detour
        function to invoke the source function.
```


*    Sample Code:
```
       typedef BOOL (__stdcall *P_DeleteFileW)(const WCHAR *Path);

       P_DeleteFileW pDeleteFileW = NULL;

       BOOL __stdcall MyDeleteFileW(const WCHAR *Path)
        {
            if (Path[0] == L'C') {

                // silently ignore requests to delete any file on drive C

                SetLastError(0);
                return TRUE;

            } else {

                // otherwise invoke the original DeleteFileW function

                return pDeleteFileW(Path);
            }
        }

        main()
        {
            pDeleteFileW = GetProcAddress(kernel32dll, "DeleteFileW");
            pDeleteFileW = SbieDll_Hook("DeleteFile",
                                        pDeleteFileW,
                                        MyDeleteFileW);
        }
```


* * *

### Register for DLL Load/Unload Callbacks

*    Prototype:
```
       typedef void (__stdcall *P_DllCallback)(const WCHAR *ImageName, HMODULE ImageBase);
```

```
       typedef BOOLEAN *(__stdcall *P_SbieDll_RegisterDllCallback)(
		       P_DllCallback pCallback);
```


*    Export Name:
```
       SbieDll_RegisterDllCallback

       This API is available starting with version 3.46 of Sandboxie.
```


*    Parameters:
```
       pCallback specifies a callback function to be invoked whenever
       any DLL is loaded or unloaded in the process.  The callback
       function cannot be unregistered.
```

```
       The ImageName (first) parameter to the callback function
       specifies the UNICODE name string for the DLL that was loaded
       or unloaded.  The name string does not include a path.
```

```
       The ImageBase (second) parameter to the callback function
       specifies the load base address for the DLL, when the callback
       function is invoked to notify of a DLL load.  When the callback
       function is invoked to notify of a DLL unload, this parameter
       is set to zero.
```


*    Return Value:
```
       Returns TRUE on success, FALSE if the callback cannot be registered.
       As of version 3.46, Sandboxie supports up to 8 registrations within
       a single process.
```


* * *

### Get Sandboxie Home Folder

*    Prototype:
```
       typedef LONG *(__stdcall *P_SbieApi_GetHomePath)(
               WCHAR *NtPath,
               ULONG NtPathMaxLen,
               WCHAR *DosPath,
               ULONG DosPathMaxLen);
```


*    Export Name:
```
       SbieApi_GetHomePath

       This API is available starting with version 3.52 of Sandboxie.
```


*    Parameters:
```
       NtPath specifies a pointer to a buffer which will receive the
       full path of the Sandboxie installation folder in NT-path syntax.

       NtPathMaxLen specifies the size of the NtPath buffer.  Specify
       NULL for NtPath and zero for NtPathMaxLen to not receive the
       NT path.

       DosPath specifies a pointer to a buffer which will receive the
       full path of the Sandboxie installation folder in DOS-path syntax.

       DosPathMaxLen specifies the size of the DosPath buffer.  Specify
       NULL for DosPath and zero for DosPathMaxLen to not receive the
       NT path.
```


*    Return Value:
```
       Returns zero on success, a non-zero value on error.

       STATUS_BUFFER_TOO_SMALL (0xC0000023) indicates either NtPathMaxLen
       or DosPathMaxLen specifies a buffer that is too small.  Increase
       the size of the input buffer and retry the call.
```
