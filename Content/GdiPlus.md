# Gdi Plus

**This page is related to Windows 2000, which is no longer supported in SBIE v4 and up.**

The Sandboxie Control program requires a Microsoft DLL called _GDIPLUS.DLL_ to be installed in the system. If you use Windows XP or a later version you need not be concerned with this, as the DLL is already present in your system.

However, this DLL is not bundled with Windows 2000\. Follow these steps to install it:

*   Visit a download page for [Platform SDK Redistributable: GDI+](https://www.google.com/search?q=gdiplus_dnld.exe).

*   Download the file _gdiplus_dnld.exe_.

*   Click _Run_ in response to the question _Do you want to run or save this file?_

*   Click _Run_ in response to the question _Do you want to run this software?_

*   Click _Yes_ to accept the terms of the end-user license agreement for GDIPLUS.DLL.

*   Enter _C:\WINNT\SYSTEM32_ into the input box labeled _Unzip to folder._ (Assuming the default case where Windows 2000 was installed in the C:\WINNT folder.)

*   Click _Unzip_.

*   Make sure that a new file _GDIPLUS.DLL_ has been created within the folder _C:\WINNT\SYSTEM32_.

*   The installation is complete and you can now install Sandboxie.
