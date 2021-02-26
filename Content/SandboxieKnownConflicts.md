# Known Conflicts

* * *
Known conflicts can be resolved by activating application configurations in Sandbox Settings > Applications or in Sandbox Options > App Templates (Plus edition).
* * *

### Not all programs can be installed inside Sandboxie

Problem: Some applications that invoke services or drivers may not install inside Sandboxie.

Solution: Install the application on your host and then run it sandboxed.

### UWP / Modern / Microsoft Store Apps

Problem: Microsoft store apps will not work in Sandboxie Classic and Sandboxie Plus.

Solution: None at this time. See issue [#19](https://github.com/sandboxie-plus/Sandboxie/issues/19) to track any possible change about this.

### Office 2013 on up & Office 365 (C2R Versions only)

Problem: Click to Run versions of Microsoft Office 2013, 2016 and Office 365 will crash when sandboxed. This includes Outlook 2013 and up.

Solution: Use a non-Click-To-Run version of Office or Google Docs, Libre Office, OpenOffice. All support Microsoft document formats.
See issue [#428](https://github.com/sandboxie-plus/Sandboxie/issues/428) to track any possible change about this.

### TOR Web Browser

Problem: TOR is very slow in a sandbox, crashes or crashes after a certain time.

Solution: The TOR browser is not fully supported by Sandboxie. A known workaround is to install the 32-bit version of Tor Browser if you are on Windows 10.
See issue [#538](https://github.com/sandboxie-plus/Sandboxie/issues/538) for more information.
