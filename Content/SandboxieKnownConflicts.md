# Known Conflicts

* * *
Known conflicts can be resolved by activating application configurations in Sandbox Settings > Applications or in Sandbox Options > App Templates (Plus edition).
* * *

### Not all programs can be installed or run inside Sandboxie

Problem: Some applications that invoke services or drivers may not install/run inside Sandboxie.

Solution #1: You may have a conflict with a third-party security software installed on your system (see issue [#647](https://github.com/sandboxie-plus/Sandboxie/issues/647), [#619](https://github.com/sandboxie-plus/Sandboxie/issues/619), [#293](https://github.com/sandboxie-plus/Sandboxie/issues/293)). If you want to know more about which security suite could be involved, take a look at the [archived forums](https://sandboxie-website-archive.github.io/www.sandboxie.com/old-forums/viewtopica726a726.html?f=11&t=21539).

Solution #2: If you have already tried to install your application in a new empty sandbox, then install it on your host and run it sandboxed.

If problems persist, especially with applications working on previous Sandboxie versions, please let us know the details by posting on the official Github repository [here](https://github.com/sandboxie-plus/Sandboxie/issues).

### UWP / Modern / Microsoft Store Apps

Problem: Microsoft store apps will not work in Sandboxie Classic and Sandboxie Plus.

Solution: None at this time. See issue [#19](https://github.com/sandboxie-plus/Sandboxie/issues/19) to track any possible change about this.

### Office 2013 on up & Office 365 (C2R Versions only)

Problem: Click to Run versions of Microsoft Office 2013, 2016 and Office 365 will crash when sandboxed. This includes Outlook 2013 and up.

Solution: A fix was included on [v0.9.7 / 5.52.1](https://github.com/sandboxie-plus/Sandboxie/releases/tag/0.9.7). It can be applied manually with most recent Sandboxie versions, see [#428](https://github.com/sandboxie-plus/Sandboxie/issues/428#issuecomment-932708577).

### Tor Browser

Problem: Tor Browser is very slow in a sandbox, crashes or crashes after a certain time.

Solution: Tor Browser is not fully supported by Sandboxie. A known workaround is to install the 32-bit version of Tor Browser if you are on Windows 10.
See issue [#538](https://github.com/sandboxie-plus/Sandboxie/issues/538) for more information.

### HP Universal Print Driver

Problem: The HP Universal Printer Status Monitor pop-up component is failing when printing from a sandboxed Web browser.

Solution: Open Sandbox Settings > Resource Access > COM Access, click Add and enter this resource name:
{D713F357-7920-4B91-9EB6-49054709EC7A}

### Autodelete feature on Microsoft Edge

Problem: Autodelete feature no longer works on Microsoft Edge.

Solution: Microsoft Edge was updated with a new setting (under System) called "Start up boost", which is enabled by default. It prevents Edge from fully shutting down, so we suggest to disable the option.

### Steam games

Problem: Not all Steam games will function while Sandboxed.

Solution: Install the games on your computer, not in a sandbox. Most games can work. However, there are [known reports](https://github.com/sandboxie-plus/Sandboxie/labels/game%20issue) that some simply may not. If you run into a problem with a Steam game, you should make sure Steam client is updated on your host machine. Run Steam not sandboxed, download and install the game on your host computer and then "right click" on the game shortcut and select "Run Sandboxed" as a workaround. If problems persist, please let us know the details by posting on the official Github repository [here](https://github.com/sandboxie-plus/Sandboxie/issues).
