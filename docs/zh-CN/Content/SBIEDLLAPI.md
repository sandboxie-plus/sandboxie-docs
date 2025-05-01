# SBIE DLL API

本页面描述了 _SbieDll.dll_ 动态链接库（DLL）中可调用的入口点。这些入口点暴露了沙箱工具（Sandboxie）的一些功能，这些功能可以通过编程方式访问，即通过其他程序而非用户与沙箱工具进行交互来访问。

以编程方式使用沙箱工具涉及三个方面：

* 使用 Start.exe 程序驱动某些功能。请参阅 [Start 命令行](StartCommandLine.md)。
* 将自定义 DLL 注入到沙箱程序中。请参阅 [InjectDll](InjectDll.md)。
* 从正在运行的程序（无论是否在沙箱中）调用沙箱工具的入口点。本文将对此进行描述。

本文描述的入口点均由 _SbieDll.dll_ 导出。要访问某个入口点，你应该将此 DLL 动态加载到你的程序中，并获取所需入口点的地址。例如：
```
        __declspec(dllexport) void __stdcall InjectDllMain(HINSTANCE hSbieDll, ULONG_PTR UnusedParameter)
	{
		//
	        // 定位 SbieDll.dll 中 SbieDll_Hook 的地址
	        //

	        typedef void *(__stdcall *P_SbieDll_Hook)(
	                const char *ApiName, void *ApiFunc, void *NewFunc);

	        P_SbieDll_Hook p_SbieDll_Hook = GetProcAddress(hSbieDll, "SbieDll_Hook");

		//
	        // 通过函数指针调用 SbieDll_Hook
	        //

	        p_SbieDll_Hook(...);
	}
```

请注意使用 _InjectDllMain_（请参阅 [注入 DLL](InjectDll.md)）来获取已加载的 SbieDll 实例的句柄。这是推荐的方法。不过，使用 LoadLibrary 或 GetModuleHandle 按名称查找 SbieDll 也是可行的。

* * *

### 枚举沙箱名称

* 原型：
```
        typedef LONG (__stdcall *P_SbieApi_EnumBoxes)(
                LONG index,                 // 初始化为 -1
                WCHAR *box_name);            // 指向 WCHAR [34] 的指针
```

* 导出名称：
```
        SbieApi_EnumBoxes
```

* 参数：
```
        index [in] 指定要返回的沙箱。初始化为 -1。
        沙箱按照它们在 Sandboxie.ini 中出现的顺序进行枚举。

        box_name [out] 接收沙箱名称。

        注意：此函数不能由沙箱程序使用。
```

* 返回值：
```
        返回下一次用于 index 参数的值。
        当没有更多内容需要枚举时返回 -1。
```


* 示例代码：

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

### 按沙箱名称查询沙箱路径

* 原型：
```
        typedef LONG (__stdcall *P_SbieApi_QueryBoxPath)(
                const WCHAR *box_name,      // 指向 WCHAR [34] 的指针
                WCHAR *file_path,
                WCHAR *key_path,
                WCHAR *ipc_path,
                ULONG *file_path_len,
                ULONG *key_path_len,
                ULONG *ipc_path_len);
```

* 导出名称：
```
        SbieApi_QueryBoxPath
```

* 参数：
```
        box_name [in] 指定要返回路径信息的沙箱名称。

        file_path [out] 接收沙箱根目录的路径，该路径由 FileRootPath 设置指定。
        该缓冲区最多接收 file_path_len 参数指定的字节数。传入 NULL 以忽略此参数。

        key_path [out] 接收沙箱注册表根键的路径，该路径由 KeyRootPath 设置指定。
        该缓冲区最多接收 key_path_len 参数指定的字节数。传入 NULL 以忽略此参数。

        ipc_path [out] 接收沙箱根对象目录的路径，该路径由 IpcRootPath 设置指定。
        该缓冲区最多接收 ipc_path_len 参数指定的字节数。传入 NULL 以忽略此参数。

        file_path_len [in/out] 指定 file_path 缓冲区的字节长度。返回时，接收完整缓冲区所需的字节长度。

        key_path_len [in/out] 指定 key_path 缓冲区的字节长度。返回时，接收完整缓冲区所需的字节长度。

        ipc_path_len [in/out] 指定 ipc_path 缓冲区的字节长度。返回时，接收完整缓冲区所需的字节长度。
```

* 返回值：
```
        成功时返回零，出错时返回非零值。
```

* 示例代码：
```
        ULONG FileLen = 0;
        ULONG KeyLen  = 0;
        ULONG IpcLen  = 0;

        SbieApi_QueryBoxPath(
                NULL, NULL, NULL, NULL, &FileLen, &KeyLen, &IpcLen);

        // 注意，长度是以字节数返回的，而不是 WCHAR 字符数

        WCHAR *FileBuf = malloc(FileLen);
        WCHAR *KeyBuf = malloc(KeyLen);
        WCHAR *IpcBuf = malloc(IpcLen);

        SbieApi_QueryBoxPath(
                FileBuf, KeyBuf, IpcBuf, &FileLen, &KeyLen, &IpcLen);

        // 现在使用 wcslen 来计算字符数

        FileLen = wcslen(FileBuf);
        KeyLen  = wcslen(KeyBuf);
        IpcLen  = wcslen(IpcBuf);
```

* * *

### 按进程 ID 查询沙箱路径

* 原型：
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

* 导出名称：
```
        SbieApi_QueryProcessPath
```

* 参数：
```
        process_id [in] 指定要查询的沙箱进程的 ID。

        file_path [out]

        key_path [out]

        ipc_path [out]

        file_path_len [in/out]

        key_path_len [in/out]

        ipc_path_len [in/out]

        最后六个参数与上面讨论的 QueryBoxPath 函数的最后六个参数类似。
        然而，QueryProcessPath（此函数）返回正在运行的程序所使用的沙箱路径，而 QueryBoxPath 返回沙箱配置中记录的路径。

        换句话说：假设一个沙箱程序以 PID 124 启动，然后某个沙箱路径（例如 FileRootPath）被设置为新值。
        此时，QueryBoxPath 将返回新值，但 PID 124 的 QueryProcessPath 将返回旧值。
```

* 返回值：
```
        成功时返回零，出错时返回非零值。
```

* * *

### 枚举正在运行的进程

* 原型：
```
        typedef LONG (__stdcall *P_SbieApi_EnumProcessEx)(
                const WCHAR *box_name,      // 指向 WCHAR [34] 的指针
                BOOLEAN all_sessions,
                ULONG which_session,
                ULONG *boxed_pids,         // 指向 ULONG [] 的指针
                ULONG *boxed_count);
```

* 导出名称：
```
        SbieApi_EnumProcessEx
```

* 参数：
```
        box_name [in] 指定要枚举其中进程的沙箱名称。

        all_sessions [in] 指定为 TRUE 以枚举所有登录会话中的进程，或仅枚举特定登录会话中的进程。

        which_session [in] 指定要枚举其中进程的登录会话编号。如果 all_sessions 为 TRUE，则忽略此参数。传入值 -1 以指定当前登录会话。

        boxed_pids [out] 接收进程 ID（PID）编号。
        第一个 ULONG 接收枚举的进程数。
        第二个 ULONG 接收第一个 PID，第三个 ULONG 接收第二个 PID，依此类推。
```

* 返回值：
```
       成功时返回零，出错时返回非零值。
```

* * *

### 查询进程信息

* 原型：
```
        typedef LONG (__stdcall *P_SbieApi_QueryProcess)(
                HANDLE process_id,
                WCHAR *box_name,            // 指向 WCHAR [34] 的指针
                WCHAR *image_name,          // 指向 WCHAR [96] 的指针
                WCHAR *sid_string,         // 指向 WCHAR [96] 的指针
                ULONG *session_id);
```

* 导出名称：
```
        SbieApi_QueryProcess
```


* 参数：
```
        process_id [in] 指定要查询的沙箱进程的 ID。

        box_name [out] 接收进程正在其中运行的沙箱名称。传入 NULL 以忽略此参数。

        image_name [out] 接收进程名称。传入 NULL 以忽略此参数。

        sid_string [out] 接收进程的 SID 字符串。传入 NULL 以忽略此参数。

        session_id [out] 接收进程正在其中运行的登录会话编号。传入 NULL 以忽略此参数。
```

* 返回值：
```
        成功时返回零，出错时返回非零值。
```


* * *

### 终止单个沙箱进程

* 原型：
```
        typedef BOOLEAN (__stdcall *P_SbieDll_KillOne)(
                HANDLE process_id);
```


* 导出名称：
```
        SbieDll_KillOne
```


* 参数：
```
        process_id [in] 指定应终止的沙箱进程的进程 ID。
```


*    返回值：
```
        成功时返回 TRUE，失败时返回 FALSE。

        目标进程由沙箱服务 (SbieSvc) 通过调用 Windows API TerminateProcess (ProcessId, 1) 以退出代码 1 终止。
```


* * *

### 终止所有沙箱进程

*    原型：
```
        typedef BOOLEAN (__stdcall *P_SbieDll_KillAll)(
                ULONG session_id,
                const WCHAR *box_name);
```


*    导出名称：
```
        SbieDll_KillAll
```


*    参数：
```
        session_id [in] 指定应终止沙箱程序的登录会话编号。

        box_name [in] 指定应终止沙箱程序的沙箱名称。指定 -1 表示当前登录会话。
```


*    返回值：
```
        成功时返回 TRUE，失败时返回 FALSE。

        目标进程以上述方式终止；请参阅 SbieDll_KillOne。
```


* * *

### 从 Sandboxie.ini 查询配置

*    原型：
```
        typedef LONG (__stdcall *P_SbieApi_QueryConf)(
                const WCHAR *section_name,  // 指向 WCHAR [34] 的指针
                const WCHAR *setting_name,  // 指向 WCHAR [66] 的指针
                ULONG setting_index,
                WCHAR *value,
                ULONG value_len)
```

*    导出名称：
```
        SbieApi_QueryConf
```

*    参数：
```
        section_name [in] 指定包含要查询的设置的节名称。

        setting_name [in] 指定要查询的设置名称。

        setting_index [in] 指定可能多次出现的设置的从零开始的索引编号。该索引编号可以与以下特殊值进行逻辑或运算：

        0x40000000 - 如果指定的设置名称未出现在指定节中，则不扫描 [GlobalSettings] 节。

        0x20000000 - 不展开结果中的任何变量。

        0x10000000 - 忽略源自模板（通常在 Templates.ini 文件中定义）的任何设置。仅查询明确出现在 Sandboxie.ini 文件中的设置。

        value [out] 接收指定设置的值。

        value_len [in] 指定 value 参数指向的缓冲区的最大字节长度。
```

*    返回值：
```
        成功时返回零。如果未找到设置，则返回 0xC000008B。任何其他返回值表示其他错误。
```


* * *

### 更新 Sandboxie.ini 中的配置

*    原型：
```
        typedef LONG (__stdcall *P_SbieDll_UpdateConf)(
        	WCHAR operation_code,
        	const WCHAR *password,      // 限制为 64 个字符
                const WCHAR *section_name,  // 限制为 32 个字符
                const WCHAR *setting_name,  // 限制为 64 个字符
                const WCHAR *value)         // 限制为 2000 个字符
```


*    导出名称：
```
        SbieDll_UpdateConf
```


*    参数：
```
        operation_code [in] 指定如何更新请求的设置：
        's' 表示设置（覆盖），替换任何现有值
        'a' 表示将新值追加到值列表的底部（如果还没有值，则简单设置新值）
        'i' 表示将新值插入到值列表的顶部（如果还没有值，则简单设置新值）
        'd' 表示删除值列表中的现有值

        password [in] 指定如果需要则使用的密码，否则为 NULL 或空字符串。

        section_name [in] 是一个必需参数，指定包含要设置的设置的节名称。

        setting_name [in] 是一个必需参数，指定要设置的设置名称。

        value [ini] 是一个可选参数，指定新值。

        如果 operation_code 为's' 且省略了 value，则指定节中的相应设置将被删除。

        如果 operation_code 为's' 且 setting_name 为 "*"（通配符星号）且省略了 value，则此函数将从配置文件中删除完整的节。
```


*    返回值：
```
        成功时返回零。
```


* * *

### 从 Sandboxie.ini 重新加载配置

*    原型：
```
        typedef LONG (__stdcall *P_SbieApi_ReloadConf)(
                ULONG session_id);
```


*    导出名称：
```
        SbieApi_ReloadConf
```


*    参数：
```
        session_id [in] 指定 Sandboxie 将记录任何错误消息的登录会话编号。传递 -1 表示当前登录会话。
```


*    返回值：
```
        成功时返回零，出错时返回非零值。
```


* * *

### 挂钩用户模式入口点

*    原型：
```
        typedef void *(__stdcall *P_SbieDll_Hook)(
                const char *name,
                void *source_func,
                void *detour_func);
```


*    导出名称：
```
        SbieDll_Hook
```


*    参数：
```
        name [in] 指定要挂钩的入口点的 ASCII 字符串名称。如果出错，SbieDll_Hook 会记录包含此描述性名称的沙箱错误消息。

        source_func [in] 指向要挂钩的函数的指针。

        detour_func [in] 指向挂钩代码的指针。

        此函数将使源函数调用绕行函数。换句话说，绕行函数将拦截对源函数的所有调用。
```


*    返回值：
```
        返回一个函数指针，绕行函数可以使用该指针调用源函数。
```


*    示例代码：
```
       typedef BOOL (__stdcall *P_DeleteFileW)(const WCHAR *Path);

       P_DeleteFileW pDeleteFileW = NULL;

       BOOL __stdcall MyDeleteFileW(const WCHAR *Path)
        {
            if (Path[0] == L'C') {

                // 静默忽略删除 C 盘上任何文件的请求

                SetLastError(0);
                return TRUE;

            } else {

                // 否则调用原始的 DeleteFileW 函数

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

### 注册 DLL 加载/卸载回调

*    原型：
```
       typedef void (__stdcall *P_DllCallback)(const WCHAR *ImageName, HMODULE ImageBase);
```

```
       typedef BOOLEAN *(__stdcall *P_SbieDll_RegisterDllCallback)(
		       P_DllCallback pCallback);
```


*    导出名称：
```
       SbieDll_RegisterDllCallback

       此 API 从 Sandboxie 3.46 版本开始可用。
```


*    参数：
```
       pCallback 指定一个回调函数，每当进程中加载或卸载任何 DLL 时都会调用该回调函数。该回调函数无法注销。
```

```
       回调函数的 ImageName（第一个）参数指定已加载或卸载的 DLL 的 UNICODE 名称字符串。该名称字符串不包含路径。
```

```
       回调函数的 ImageBase（第二个）参数指定 DLL 加载时的加载基地址。当调用回调函数通知 DLL 卸载时，此参数设置为零。
```


*    返回值：
```
       成功时返回 TRUE，如果无法注册回调则返回 FALSE。从 3.46 版本开始，Sandboxie 支持在单个进程中最多进行 8 次注册。
```


* * *

### 获取 Sandboxie 主文件夹

*    原型：
```
       typedef LONG *(__stdcall *P_SbieApi_GetHomePath)(
               WCHAR *NtPath,
               ULONG NtPathMaxLen,
               WCHAR *DosPath,
               ULONG DosPathMaxLen);
```


*    导出名称：
```
       SbieApi_GetHomePath

       此 API 从 Sandboxie 3.52 版本开始可用。
```


*    参数：
```
       NtPath 指定一个指向缓冲区的指针，该缓冲区将接收 Sandboxie 安装文件夹的完整 NT 路径语法的路径。

       NtPathMaxLen 指定 NtPath 缓冲区的大小。将 NtPath 指定为 NULL 并将 NtPathMaxLen 指定为零以不接收 NT 路径。

       DosPath 指定一个指向缓冲区的指针，该缓冲区将接收 Sandboxie 安装文件夹的完整 DOS 路径语法的路径。

       DosPathMaxLen 指定 DosPath 缓冲区的大小。将 DosPath 指定为 NULL 并将 DosPathMaxLen 指定为零以不接收 NT 路径。
```


*    返回值：
```
       成功时返回零，出错时返回非零值。

       STATUS_BUFFER_TOO_SMALL (0xC0000023) 表示 NtPathMaxLen 或 DosPathMaxLen 指定的缓冲区太小。增大输入缓冲区的大小并重新尝试调用。
```
