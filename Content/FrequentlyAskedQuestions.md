# Frequently Asked Questions


### Overview <a name="Overview" href="#Overview"></a>

*   [What is Sandboxie and how is it different than other solutions?](#WhatIsSandboxie)
*   [How safe would I be, by using Sandboxie?](#HowSafe)
*   [Do I need other solutions if I use Sandboxie?](#NeedOtherSolutions)
*   [What kinds of programs can I run using Sandboxie?](#SandboxablePrograms)
*   [What are the technical requirements to run Sandboxie?](#Requirements)

### Technical <a name="Technical" href="#Technical"></a>

*   [How does Sandboxie protect me, technically?](#HowItWorks)
*   [Will Sandboxie protect me from malicious key-loggers?](#KeyLoggers)
*   [Some competing products require a reboot to initiate sandboxing, why?](#RebootNeeded)
*   [Why am I getting some Messages from Sandbox Driver?](#CommonMessages)
*   [Why are so many files copied into the sandbox?](#TooManyFiles)
*   [What are SandboxieRpcSs and SandboxieDcomLaunch?](#SandboxieRpcss)
*   [How can I use Sandboxie to protect myself from viruses in email?](#EmailProtection)
*   [How to configure Sandboxie for only an occasional use?](#OccasionalUse)

### Problems <a name="Problems" href="#Problems"></a>

*   [How do I make Quick Recovery show my saved favorites and downloads?](#QuickRecovery)
*   [I saved a downloaded file, a document or an email inside the sandbox, how do I get it out?](#SavedInSandbox)
*   [Why does the wrong program start when I run my default Web browser sandboxed?](#WrongBrowser)
*   If you have a program that doesn't work properly sandboxed, please look it up on the [Known Conflicts](SandboxieKnownConflicts.md) page before posting a problem report.

* * *

Back to [HelpTopics](HelpTopics.md)

* * *

**What is Sandboxie and how is it different than other solutions?** <a name="WhatIsSandboxie" href="#WhatIsSandboxie">#</a>

Think of your PC as a piece of paper. Every program you run writes on the paper. When you run your browser, it writes on the paper about every site you visited. And any malware you come across will usually try to write itself into the paper.

Traditional privacy and anti-malware software try to locate and erase any writings they think you wouldn't want on the paper. Most of the times they get it right. But first the makers of these solutions must teach the solution what to look for on the paper, and also how to erase it safely.

On the other hand, the Sandboxie sandbox works like a transparency layer placed over the paper. Programs write on the transparency layer and to them it looks like the real paper. When you delete the sandbox, it's like removing the transparency layer, the unchanged, real paper is revealed.

![](../Media/PaperAnimation.gif)

Thanks to _esalkin_ for the paper metaphore. Thanks to _warwagon_ for the graphics.

**Back to [Table of Contents](#Overview)**

* * *

**How safe would I be, by using Sandboxie?** <a name="HowSafe" href="#HowSafe">#</a>

You would be quite safe using Sandboxie. It should be noted that, from time to time, people are able to find some vulnerability in Sandboxie, an open hole through which malicious software can still infiltrate the system.

This is extremely rare and is quickly resolved by closing the hole that is the attack vector.

Thus it's a good idea to have more traditional anti-malware software. This is is the subject of the following question.

**Back to [Table of Contents](#Overview)**

* * *

**Do I need other solutions if I use Sandboxie?** <a name="NeedOtherSolutions" href="#NeedOtherSolutions">#</a>

Sandboxie may be your first line of defense, but it should certainly be complemented by the more traditional anti-virus and anti-malware solutions. These solutions can let you know if your system does become infected in any way.

Typically, those other solutions employ various forms of pattern matching to discover malicious software and other threats. Sandboxie, on the other hand, quite simply does not trust any software code enough to let it out of the sandbox.

The combination of the two approaches should keep malicious software -- which is serving the interest of other unknown parties -- out of your computer.

**Back to [Table of Contents](#Overview)**

* * *

**What kinds of programs can I run using Sandboxie?** <a name="SandboxablePrograms" href="#SandboxablePrograms">#</a>

You should be able to run most applications sandboxed.

*   Major Web browsers (Microsoft Edge is not supported at this time)
*   Mail and news readers
*   instant messengers and chat clients
*   peer-to-peer networking
*   Office Suites (Libre Office, OpenOffice) (Support for MS Office 2016/Office365 is offered for the paid version)
*   Most games
    *   in particular, online games which download extension software code

In all cases on this list, your client-side program is exposed to remote software code, which could use the program as a channel to infiltrate your system. By running the program sandboxed, you greatly increase the control you have over that channel.

And in addition, you can even _install_ some applications into the sandbox.

**Back to [Table of Contents](#Overview)**

* * *

**What are the requirements to run Sandboxie?** <a name="Requirements" href="#Requirements">#</a>

Sandboxie works on

*   Windows XP SP3 (Up until Sandboxie 5.22 and solely in [v5.40](https://github.com/sandboxie-plus/Sandboxie/releases/tag/v5.40))
*   Windows 7 (32/64)
*   Windows 8.1 (32/64)
*   Windows 10 (32/64)(Metro(tile) Apps not supported)

See [the download page](https://github.com/sandboxie-plus/Sandboxie/releases).

Supported Web Browsers (32 & 64 bit supported)

*   Internet Explorer 8, 9, 10 & 11
*   Microsoft Edge (Chromium)
*   Google Chrome
*   Firefox
*   Opera
*   PaleMoon
*   SeaMonkey
*   Vivaldi
*   Waterfox
*   Brave Browser
*   And many others!

Sandboxie does not work on...

*   Windows XP x64 bit
*   Windows 95, 98 or ME
*   Mac or Linux operating systems.

Sandboxie should not be installed on Microsoft Server Operating Systems as it's not directly supported. However, we have many users that have deployed it successfully.

You can run Sandboxie in a VM Environment (VMWare, VirtualBox, Apple BootCamp, etc.)

There are no particular hardware requirements to run Sandboxie. However, we do no test on touchscreen devices (many users have successfully installed Sandboxie on Surface pro and similar devices).

Sandboxie needs only a small amount of memory and should have a very small impact on performance.

**Back to [Table of Contents](#Overview)**

* * *

**How does Sandboxie protect me, technically?** <a name="HowItWorks" href="#HowItWorks">#</a>

Sandboxie extends the operating system (OS) with sandboxing capabilities by blending into it. Applications can never access hardware such as disk storage directly, they have to ask the OS to do it for them. Since Sandboxie integrates into the OS, it can do what it does without risk of being circumvented.

The following classes of system objects are supervised by Sandboxie: Files, Disk Devices, Registry Keys, Process and Thread objects, Driver objects, and objects used for Inter-process communication: Named Pipes and Mailbox Objects, Events, Mutexs (Mutants in NT speak), Semaphores, Sections and LPC Ports. For some more information on this, see [Sandbox Hierarchy](SandboxHierarchy.md).

Sandboxie also takes measures to prevent programs executing inside the sandbox from hijacking non-sandboxed programs and using them as a vehicle to operate outside the sandbox.

Sandboxie also prevents programs executing inside the sandbox from loading drivers directly. It also prevents programs from asking a central system component, known as the Service Control Manager, to load drivers on their behalf. In this way, drivers, and more importantly, rootkits, cannot be installed by a sandboxed program.

It should be noted, however, that Sandboxie does not typically stop sandboxed programs from reading your sensitive data. However, by careful configuration of the [ClosedFilePath](ClosedFilePath.md) and [ClosedKeyPath](ClosedKeyPath.md) settings, you can achieve this goal as well.

**Back to [Table of Contents](#Technical)**

* * *

**Will Sandboxie protect me from malicious key-loggers?** <a name="KeyLoggers" href="#KeyLoggers">#</a>

Yes, to some extent. First of all, your system (outside the sandbox) must not have been already compromised by an installed key-logger. Sandboxie can not protect against key-loggers that are already running outside the sandbox.

You may want to consider always browsing sandboxed, so you don't accidentally get any key-loggers into your system.

It is very difficult to reliably detect a key-logger. For a lengthy explanation, see [Detecting Key Loggers](DetectingKeyLoggers.md). So the most important tool Sandboxie offers you for protection against key-loggers, is to delete the sandbox.

When you stop all sandboxed activity (in all sandboxes), then proceed to delete the sandbox you're about to use, you can be fairly certain that all key-loggers are dead.

**Back to [Table of Contents](#Technical)**

* * *

**Some competing products require a reboot to initiate sandboxing, why?** <a name="RebootNeeded" href="#RebootNeeded">#</a>

Changes to the computing environment must eventually make their way to disk storage, if they are to be permanent. This obviously applies to files. But it also applies to things like settings and preferences saved in the system registry.

Some competing products require a reboot before each use, because they sandbox disk storage as a whole. They provide the operating system and everything in it with a single virtual disk, which is used to trap those permanent changes.

The operating system is not designed to use one disk for some tasks, and another disk for other tasks. Therefore a reboot is required to switch to and from the virtual disk.

Sandboxie does not require a reboot because it sandboxes access to files, rather than to the disk as a whole. It also sandboxes access to registry keys. It also sandboxes access to many other classes of system components, in order to trick the sandboxed program into believing that it isn't being tricked.

This low-level sandboxing in some competing products makes it possible to install a wider range of applications and system tools -- including system drivers -- into the sandbox. Sandboxie can install most applications into the sandbox, but not system software nor drivers.

It becomes apparent that, like most other things, each tool has its advantages and disadvantages, and one must choose the best tool for the task at hand.

**Back to [Table of Contents](#Technical)**

* * *

**Why am I getting some Messages from Sandbox Driver?** <a name="CommonMessages" href="#CommonMessages">#</a>

Not all messages are errors, some simply inform you of an event that has occurred. For more information, see [SBIE Messages](SBIEMessages.md).

**Back to [Table of Contents](#Technical)**

* * *

**Why are so many files copied into the sandbox?** <a name="TooManyFiles" href="#TooManyFiles">#</a>

When a program accesses a file, it declares what operations it plans to do on the file: if it plans to read from the file, to write the file, to change its attributes, and so on. Whenever a program declares any kind of write access to a file, Sandboxie copies it into the sandbox. In some cases, programs declare they intend to write to the file when in fact they do not, but nevertheless Sandboxie must copy the file into the sandbox.

**Back to [Table of Contents](#Technical)**

* * *

**What are SandboxieRpcSs and SandboxieDcomLaunch?** <a name="SandboxieRpcss" href="#SandboxieRpcss">#</a>

See [Service Programs](ServicePrograms.md).

**Back to [Table of Contents](#Technical)**

* * *

**How can I use Sandboxie to protect myself from viruses in email?** <a name="EmailProtection" href="#EmailProtection">#</a>

See full article: [Email Protection](EmailProtection.md).

**Back to [Table of Contents](#Technical)**

* * *

**How to configure Sandboxie for only an occasional use?** <a name="OccasionalUse" href="#OccasionalUse">#</a>

By default Sandboxie is configured to load and start automatically. To have Sandboxie load only when you need it, make the following changes.

*   In [Sandboxie Control](SandboxieControl.md), open the _Configure -> Shell Integration_ window, and clear the checkbox _When Windows starts_ to stop Sandboxie Control from starting.

*   Open the Windows Services configuration window: _Start menu -> Control Panel -> Administrative Tools -> Services_. Then locate the Sandboxie Service. Double click to bring up its properties window. Set its _Startup type_ to _Manual_ rather than automatic.

*   The driver component of Sandboxie is started by the Sandboxie Service. Therefore, setting the service to start manually, indirectly also sets the driver to start manually.

Starting Sandboxie Control will also start the service. (But note that Administrative rights are required to start a service.)

**Back to [Table of Contents](#Technical)**

* * *

**How do I make Quick Recovery show my saved favorites and downloads?** <a name="QuickRecovery" href="#QuickRecovery">#</a>

You may not see all your folders in Quick Recovery, as only a few are configured by default in the initial installation. See also QuickRecovery.

**Back to [Table of Contents](#Problems)**

* * *

**I saved a downloaded file, a document or an email inside the sandbox, how do I get it out?** <a name="SavedInSandbox" href="#SavedInSandbox">#</a>

If you read [What is Sandboxie](#WhatIsSandboxie) then you know Sandboxie is like a transparency layer placed over the paper. (The paper is your computer.) When you save files (downloads, documents, emails, or anything else) through a sandboxed program, these files go into the transparency layer that is the sandbox.

You can use QuickRecovery to get these files out. Unless configured otherwise, QuickRecovery looks in your My Documents folder, and Desktop folder. If you save the files to either of these folders, then you can use QuickRecovery to easily get them out.

Another approach is configuring one or more folders as an OpenFilePath. Saving files into such folders bypasses the sandbox mechanism, and goes directly to the real folders. Setting this is more complicated, but may also prove useful, in some cases.

**Back to [Table of Contents](#Problems)**

* * *

**Why does the wrong program start when I run my default Web browser sandboxed?** <a name="WrongBrowser" href="#WrongBrowser">#</a>

This happens for some people.

In Windows 7, open Control Panel in Icon view and select Default Programs > Set your default programs. You can then select the browser you want as default.

In Windows 8/8.1, point to (but do not click) the lower-right or top-right corner of the screen, and then click the Settings icon. In the lower-right corner, click Change PC Settings > Search and apps > Defaults. You can then select the browser you want as default.

If using Windows 10, ensure that your default Web Browser for Windows is set correctly (click on the Start menu, type "default app settings" and Choose your default apps).

**Back to [Table of Contents](#Problems)**

