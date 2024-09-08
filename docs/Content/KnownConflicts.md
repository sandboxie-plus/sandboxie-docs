# Known Conflicts

* * *
Known conflicts can be resolved by activating application configurations in Sandbox Settings > Applications or in Sandbox Options > App Templates (Plus edition).
* * *

### Not all programs can be installed or run inside Sandboxie

Problem: Some applications that invoke services or drivers may not install/run inside Sandboxie.

Solution #1: You may have a conflict with a third-party security software installed on your system (see issue [#647](https://github.com/sandboxie-plus/Sandboxie/issues/647) and [#293](https://github.com/sandboxie-plus/Sandboxie/issues/293)). If you want to know more about which security suite could be involved, take a look at the [archived forums](https://sandboxie-website-archive.github.io/www.sandboxie.com/old-forums/viewtopica726a726.html?f=11&t=21539).

Solution #2: If you have already tried to install your application in a new empty sandbox, then install it on your host and run it sandboxed.

If problems persist, especially with applications working on previous Sandboxie versions, please let us know the details by posting on the [GitHub repository](https://github.com/sandboxie-plus/Sandboxie/issues).

### Microsoft Store apps

Problem: Microsoft store apps will not work in Sandboxie Classic and Sandboxie Plus.

Solution: None at this time. See issue [#19](https://github.com/sandboxie-plus/Sandboxie/issues/19) to track any possible change about this.

### Office 2013/2016/2019 & Office 365 (C2R versions only)

Problem: Click to Run versions of Microsoft Office 2013, 2016, 2019 and Office 365 will crash when sandboxed. This includes Outlook 2013 and up.

Solution: A fix was included on [v0.9.7 / 5.52.1](https://github.com/sandboxie-plus/Sandboxie/releases/tag/0.9.7).

### Office 2021

Problem: Office 2021 cannot be installed inside a sandbox.

Solution: None at this time. See issue [#1675](https://github.com/sandboxie-plus/Sandboxie/issues/1675) or [#1900](https://github.com/sandboxie-plus/Sandboxie/issues/1900) to track any possible change about this.

### Tor Browser

Problem: Tor Browser is very slow in a sandbox, crashes or crashes after a certain time.

Solution:  A fix was included on [v1.0.21 / 5.55.21](https://github.com/sandboxie-plus/Sandboxie/releases/tag/1.0.21).

### HP Universal Print Driver

Problem: The HP Universal Printer Status Monitor pop-up component is failing when printing from a sandboxed Web browser.

Solution: Open Sandbox Settings > Resource Access > COM Access, click Add and enter this resource name:
`{D713F357-7920-4B91-9EB6-49054709EC7A}`

### Autodelete feature on Microsoft Edge

Problem: Autodelete feature no longer works on Microsoft Edge.

Solution: Microsoft Edge was updated with a new setting (under System) called "Startup boost", which is enabled by default. It prevents Edge from fully shutting down, so we suggest to disable the option or install [v1.1.2 / 5.56.2](https://github.com/sandboxie-plus/Sandboxie/releases/tag/v1.1.2) or newer versions which include the fix.

### Steam games

Problem: Not all Steam games will function while Sandboxed.

Solution: Install the games on your computer, not in a sandbox. Most games can work. However, there are [known reports](https://github.com/sandboxie-plus/Sandboxie/labels/game%20issue) that some simply may not. If you run into a problem with a Steam game, you should make sure Steam client is updated on your host machine. Run Steam not sandboxed, download and install the game on your host computer and then "right click" on the game shortcut and select "Run Sandboxed" as a workaround. If problems persist, please let us know the details by posting on the [GitHub repository](https://github.com/sandboxie-plus/Sandboxie/issues).

### GOG Games and Galaxy Beta

Problem: Games from GOG Galaxy may not run while sandboxed.

Solution: A partial workaround is available in [#1246](https://github.com/sandboxie-plus/Sandboxie/issues/1246). You can "force" GOG Program folder so that it works correctly within a sandbox. See also: [ForceFolder](ForceFolder.md).

### No access to microphone or camera on any sandbox in Windows 11

Problem: There is no access to microphone/camera on any sandbox in Windows 11 systems.

Solution: A workaround is available in [#1669](https://github.com/sandboxie-plus/Sandboxie/issues/1669), but no permanent fix.

### Tabs sessions on Chromium browsers are sometimes not restored correctly in Sandboxie

Problem: Tabs sessions are lost when a Chromium browser is running outside of the sandbox.

Solution: No fix yet, but some workarounds are available in [#558](https://github.com/sandboxie-plus/Sandboxie/issues/558).

### Windows Explorer takes a long time to open folders, drives or context menus

Problem: Windows Explorer can take a long time to open while sandboxed on Windows 10 and 11.

Solution: No fix yet, see [#69](https://github.com/sandboxie-plus/Sandboxie/issues/69).

### "Open With" dialog does not work in a sandboxed File Explorer instance

Problem: "Open with" functionality is not working with Sandboxie.

Solution: A fix was included on [v1.0.6 / 5.55.6](https://github.com/sandboxie-plus/Sandboxie/releases/tag/1.0.6).

### Can't use the search box in File Explorer

Problem: The search box in File Explorer doesn't get focused while sandboxed, and you can't input anything.

Solution: A fix was included on [v0.9.8c / 5.53.2](https://github.com/sandboxie-plus/Sandboxie/releases/tag/0.9.8c).

###  "Sandboxed service failed to start: BITS" or "Request to start service bits was denied" can appear while a program is sandboxed

Problem: BITS service seems to be broken since a few Windows 10 releases, as it's using some parts of WMI which is blocked in Sandboxie.

Solution: A workaround was directly included on [v1.0.1 / 5.55.1](https://github.com/sandboxie-plus/Sandboxie/releases/tag/1.0.1).

### I can't find my issue in this list

If you would like to search for further issues, please refer to the [GitHub repository](https://github.com/sandboxie-plus/Sandboxie).
