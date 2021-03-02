# Known Conflicts

* * *
Known conflicts can be resolved by activating application configurations in Sandbox Settings > Applications or in Sandbox Options > App Templates (Plus edition).
* * *

### Not all programs can be installed or run inside Sandboxie

Problem: Some applications that invoke services or drivers may not install/run inside Sandboxie.

Solution #1: You may have a conflict with a third-party security software installed on your system. For more information, see issue [#619](https://github.com/sandboxie-plus/Sandboxie/issues/619) and issue [#293](https://github.com/sandboxie-plus/Sandboxie/issues/293). 

If you want to know more about which one could be involved, take a look at the [archived forums](https://sandboxie-website-archive.github.io/www.sandboxie.com/old-forums/viewtopica726a726.html?f=11&t=21539).

Solution #2: If you have already tried to install your application in a new empty sandbox, then install it on your host and run it sandboxed.

If problems persist, especially with applications working on previous Sandboxie versions, please let us know the details by posting on the official Github repository [here](https://github.com/sandboxie-plus/Sandboxie/issues).

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

### HP Universal Print Driver

Problem: The HP Universal Printer Status Monitor pop-up component is failing when printing from a sandboxed Web browser.

Solution: Open Sandbox Settings > Resource Access > COM Access, click Add and enter this resource name:
{D713F357-7920-4B91-9EB6-49054709EC7A}
