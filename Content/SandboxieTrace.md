# Sandboxie Trace Logging

---

### Overview

In some cases, a program may not function correctly within the sandbox, because it needs access to a system resource which is, by default, protected by Sandboxie, and access to that resource is denied.

Note that in this case, the sandboxed program is not creating the resource itself; rather, it expects the resource to already be available for access and use.

The trace displays access attempts and makes it possible to somewhat easily identify which resources that are needed for correct operation, have been blocked.

### UI Configuration

This page covers the trace settings and understanding the trace output, for the graphical configuration and interface please see the correct [Sandboxie Agent](SandboxieAgent.md) page:

- **[Trace Logging](TraceLog.md) for Sandboxie Plus.**

- **[Resource Access Monitor](ResourceAccessMonitor.md) for Sandboxie Classic.**

### Default Tracing

Sandboxie can automatically trace the commonly problematic api's for you and displays the output in a simpler format.  It only shows a subset of all the resource calls made, but is a good place to start for most issues.   By default if you do not enable additional tracing this is what will show in the trace log.  If you cannot seem to find the entry of what is causing the problem with the default tracing you can enable the [Advanced Trace Options](#Advanced Trace Options) below.

#### Start Trace Logging

This can be done in the [Sandboxie Plus](SandboxiePlus.md) app menu under "Options -> Trace Logging" (or in Sandboxie Classic the [File Menu](SBPlusFileMenu.md) -> Resource Access Monitor).  Before enabling trace logging you will normally want to go as far as possible before triggering the problem.  Then you want to enable trace logging, trigger the problem, and then turn it back off.  This will minimize the logs you need to review.

#### Advanced Trace Options

Advanced trace options provide a higher level of detail than standard tracing. The trace options can be activated through the the Sandbox options (Advanced Options->Tracing) in Plus or different [Sandboxie Ini](SandboxieIni.md) settings:

- **FileTrace** logs access to files, folders, and filesystem volumes;
- **KeyTrace** logs access to registry keys (but not values within keys);
- **PipeTrace** logs access to named pipes and mail slot objects which are used for inter-process communication;
- **IpcTrace** logs access to other objects used for inter-process communication, and also logs access attempts by one process to another process;
- **GuiTrace** logs window-to-window communications;
- **ClsidTrace** logs COM communications;
- **NetFwTrace** traces the actions of the firewall components (since version 0.9.0 / 5.51.0) (will only show in kernel debug output, see section below);
- **DebugTrace** (Log Debug Output to Trace Log) some applications emit messages to the Windows debug log by default.  Checking this option (or setting it to *y* in the ini) will redirect application debug messages to show up in the Sandboxie Trace Log.
- **ErrorTrace** (Log all SetError's to Trace log) when a Win32 API call is executed it often doesn't return the exact error it runs into, instead it calls SetError with the error code.  The application making the call would normally call GetLastError to return the last error set.  Checking this option (or setting it to 'y' in the ini) will log all SetError calls to the Sandboxie Trace Log.  Note: Many calls log plenty errors that are expected or handled, and there are a large number of Win32 calls made by most programs.  Enabling this option will result in a lot of output.
- **LogAPI** library to get additional trace output (see [this thread](https://forum.xanasoft.com/viewtopic.php?f=12&t=143) for more information).
- **DisableResourceMonitor** this does not actually enable any logging but instead turns off the default trace options that are enabled any time trace logging is turned on.  This can be useful if you explicitly only want to see the output from the trace options you enable.  To enable this check the box or set it to *y* in the ini.

If you configure these options using the [Sandboxie Agent](SandboxieAgent.md) they will be configured to log all requests (both successful and failed request).  If you want to only log one result you can edit the setting in the ini.  In the ini each setting accepts a sequence of characters which specifies what to log. The wildcard character \* logs all requests;  the character *a* logs requests which were allowed; the character *d* logs requests which were denied. For the **FileTrace** and **PipeTrace** settings, the character *i* logs requests which were allowed because they access a device which is ignored by Sandboxie, such as a CD-ROM.   For **DisableResourceMonitor**, **ErrorTrace** and **DebugTrace** the only valid value is *y* for enabled.  For **LogAPI** it requires specific DLL Inject lines to enable, see the thread above (or use the UI Agent).

The settings **PipeTrace**, **IpcTrace** and **GuiTrace** are often able to highlight the issues an application my fail. **FileTrace** and **KeyTrace** will usually not be able to provide insight as to why a sandboxed program is malfunctioning.

Manually setup logging in [Sandboxie Ini](SandboxieIni.md) looks like:

```
   [GlobalSettings]
   IpcTrace=ad
   PipeTrace=ad
   GuiTrace=ad
```

Then use Sandboxie to reload the configuration (if you edited the ini in the [Sandboxie Plus](SandboxiePlus.md) Agent you do not need to reload):

- **Configure** menu -> **Reload Configuration** on Sandboxie Classic
- **Options** menu -> **Reload ini file** on Sandboxie Plus

Trace options can be set on a per sandbox basis such that only the boxes you need will generate trace logs.

You can also adjust the buffer size by adding `TraceBufferPages=2560` that will increase it tenfold.

#### Kernel Debug Output Only

While most trace logs are viewable directly in the app, certain traces only show up in the kernel log. Right now that is only the kernel level NewFwTrace module. For kernel only output you need to use an app like [DbgView.exe](https://docs.microsoft.com/en-us/sysinternals/downloads/debugview) to view the logs.

On Windows Vista and later, output from the system debugger log is disabled by default. [This blog post](https://web.archive.org/web/20080731211018/http://blogs.msdn.com:80/doronh/archive/2006/11/14/where-did-my-debug-output-go-in-vista.aspx) and [this StackOverflow thread](https://stackoverflow.com/questions/65015739/outputdebugstring-not-showing-message-in-debugview-windows-10-x64) explain how to enable it.

### Understanding the Trace Log Output

A trace will display output in the following format:

```
...  
(001404) SBIE (FA) 00120116.01.00000000 \Device\NamedPipe\ShimViewer  
...  
(001404) SBIE (IA) 001F0001 \ThemeApiPort  
...  
(001404) SBIE (PD) 00000040 001136  
(001404) SBIE (PA) 00020400 001136  
...  
(001404) SBIE (FA) 00000001.0F.FFFFFFFF \Device\Afd\Endpoint  
(001404) SBIE (FA) 00000001.0F.FFFFFFFF \Device\Afd  
...  
(001404) SBIE (ID) 001F0001 \RPC Control\protected_storage  
...  
```

The breakdown is this:

```(pid) SBIE (ca) (access) (resource)```

where _pid_ identifies the process attempting the access;  
_c_ indicates the Sandboxie class for the resource (see Resource Class section lower);  
_a_ indicates if the access was allowed (A) or denied (D);  
access indicates the access requested to the object, and is typically not interesting or important;  
_resource_ identifies the resource to which access is desired; in the case of process-to-process access, where _ca_ is (PA) or (PD), the resource name is the process id of the process being accessed.

Some examples:

```(001404) SBIE (IA) 001F0001 \ThemeApiPort```

Here the process making the request is process id 1404, and was allowed to access the resource named _ThemeApiPort_. The resource class is I, so this is an inter-process object. The access was allowed because by default, Sandboxie allows this specific access.

```(001404) SBIE (ID) 001F0001 \RPC Control\protected_storage```

Here the access to the resource _protected_storage_ was denied. By default Sandboxie does not allow this access; however the OpenProtectedStorage setting changes this behavior.

```(001404) SBIE (FA) 00000001.0F.FFFFFFFF \Device\Afd\Endpoint```

Here the access is allowed to the resource _Endpoint_. The resource class is F, so this is a named pipe or a mail slot resource. The access is allowed by default, because the _\Device\Afd_ prefix names resources needed for Internet access.

#### Resource Class

The trace record shows the Sandboxie resource class of the object. This indicates which OpenXxxPath setting is needed to allow access to the object.

* When resource class is F, as in (FA) or (FD), the relevant settings are [OpenFilePath](OpenFilePath.md) and [ClosedFilePath](ClosedFilePath.md).
* When resource class is K, as in (KA) or (KD), the relevant settings are [OpenKeyPath](OpenKeyPath.md) and [ClosedKeyPath](ClosedKeyPath.md).
* When resource class is I, as in (IA) or (ID), the relevant settings are [OpenIpcPath](OpenIpcPath.md) and [ClosedIpcPath](ClosedIpcPath.md).
* When resource class is G, as in (GA) or (GD), the relevant setting is [OpenWinClass](OpenWinClass.md).
* For COM objects displayed by ClsidTrace, the relevant setting is [OpenClsid](OpenClsid.md).

#### **GuiTrace** Log Entries

When **GuiTrace** is enabled, the trace also produces entries like the following:

```
...  
(001404) SBIE (GA) WinHook 0002 on tid=001484 pid=001960  
(001404) SBIE (GA) AccHook on tid=000000 pid=000000  
...  
(001404) SBIE (GD) PostMessage 01224 (04C8) to hwnd=00050060 pid=001324 DDEMLMom  
(001404) SBIE (GD) SendMessage 49376 (C0E0) to hwnd=00010014 pid=000804 #32769  
...  
(001404) SBIE (GD) SendInput  
(001404) SBIE (GA) SendInput  
```

These entries have a few formats. The first word after (GA) or (GD) identifies the type of the entry.

When the first word is _WinHook_ or _AccHook_, the entry indicates installation of a hook. Its installation is permitted for (GA) entries, and denied for (GD) entries. _WinHook_ is a standard Windows hook, followed by the type of the hook (see [SetWidowsHookEx in MSDN](https://www.google.com/search?hl=en&q=setwindowshookex+msdn)). _AccHook_ is an accessability hook (see [SetWinEventHook in MSDN](https://www.google.com/search?hl=en&q=setwineventhook+msdn)).

Both entries identify the thread number (tid) process number (pid) into which the hook was to be installed.

When the first word is _PostMessage_, _SendMessage_ or _ThrdMessage_, the entry shows denied window communication. The following two numbers indicate the window message number, in decimal and hexadecimal. The entry also indicates the window handle (hwnd) of the target window, the process number (pid) which owns this window, and finally, the internal window class name for the window.

### Analyze the Trace

The point of using the trace is usually to identify the resource that is keeping the sandboxed program from functioning correctly.

Consider for example the following trace record:

```(001404) SBIE (ID) 001F0001 \BaseNamedObjects\Xyzzy```

This shows that access to some _Xyzzy_ resource was denied. Sandboxie does not know this resource, and by default, it denies access to unknown resources.

If a sandboxed programs begins to malfunction (it may lock up, or it may end abruptly, or just complain about something) soon after this record appears in the trace, it stands to reason that the program was expecting the resource to be accessible.

The next step is to add an [OpenIpcPath](OpenIpcPath.md) setting for this resource:  

```OpenIpcPath=\BaseNamedObjects\Xyzzy```

This setting tells Sandboxie that access to the _Xyzzy_ resource should not be blocked.

Then reload the Sandboxie configuration, clear the old contents of the trace display, and restart the sandboxed program. If the program now performs better, _Xyzzy_ was indeed the problematic resource.

But if the program still fails, the trace log can be inspected again for later (or possibly earlier) failed access attempts.

### Trace Performance Impact

By default even having trace options enabled under a sandbox will have very minimal impact when the "Trace Logging" option in the [SB Agent](SandboxieAgent.md) is not enabled.  When there are large amount of log entries being made this can cause considerable performance impact.   This is why it is suggested to only enable tracing right before the problem happens and disable it once it does.   If this is not possible, or the problem is sporadic, consider limiting the trace options enabled to reduce the log output.
