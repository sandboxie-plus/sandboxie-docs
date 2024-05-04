# Detecting Key Loggers

Go to [Help Topics](HelpTopics.md), [Usage Tips](UsageTips.md).

* * *

### Overview

It is very difficult to reliably detect all classes of key-loggers. This section first explains why this is so, and concludes by offering a possible defense against them.

First, a distinction must be made between several classes of key-loggers:

*   external key-loggers
*   rootkit key-loggers
*   windows hook key-loggers
*   windows message key-loggers
*   scripted key-loggers

### External Key-Loggers

External (or hardware) key-loggers are devices that connect to your computer in some way. Two examples are a small device plugged between the keyboard and the computer, or a device that snoops on radio signals transmitted by a wireless keyboard.

The common principle of key-loggers in this class is that they are _external_ to the Windows system on which they are spying. Software running within Windows cannot detect, remove or protect against external key-loggers.

The other classes of key-loggers described here are software key-loggers which do operate within Windows.

### Rootkit Key-Loggers

Rootkit key-loggers record keystrokes at the lowest software level, typically by positioning themselves as a second keyboard hardware driver (a _filter_ driver, in Windows terminology).

Once installed, this class of key-loggers may provide the best logging facilities, and may be difficult to get rid of. But to be installed in the first place, this key-logger needs the explicit help of the operating system, and so is easily blocked by Sandboxie.

~~If such a key-logger attempts to install, Sandboxie should report an informational message [SBIE2103](SBIE2103.md), unless the [BlockDrivers](BlockDrivers.md) setting (see also [Sandbox Settings > Restrictions > Low-Level Access](RestrictionsSettings.md#low-level-access--removed)) was explicitly used to disable this protection.~~

### Windows Hook Key-Loggers

These key-loggers don't masquerade as hardware drivers, but they still have to ask the operating system to load them (or _hook them_) into every program executing on the desktop.

It is not uncommon for applications to install such hooks as part of normal operation, and blocking all of them would prevent some programs from running successfully inside the sandbox.

~~**Removed From Sandboxie - Block Hooks Command**~~

~~The approach Sandboxie takes is to honor the hook request partially, by applying the hook only to applications in the same sandbox as the requesting application.~~

~~The [BlockWinHooks](BlockWinHooks.md) setting (see also [Sandbox Settings > Restrictions > Low-Level Access](RestrictionsSettings.md#low-level-access--removed)) may be used to explicitly disable this protection.~~

### Windows Message Key-Loggers

This class of key-loggers doesn't need any assistance from the operating system, and can only reliably record activity within one program. However, from the point of view of a supervisory program like Sandboxie, they don't do anything suspicious, and so cannot be stopped.

In order for a program running on the desktop to actually process the keyboard input, the operating system sends that program a message describing the input. The message key-logger, which is likely running in the same process space as the program being logged, can snoop on these messages in a variety of ways, which don't raise suspicion.

Typically this key-logger will be a secret Web browser plugin (or a secret component of a plugin), so it can easily record keyboard activity related to the Web browser.

### Scripted Key-Loggers

This class of key-loggers target and compromise the Web site you will be visiting. This is in contrast to the three other forms of key-loggers discussed here, which target and compromise your own computer.

The JavaScript and VBScript languages offer facilities for a Web page to react to keystrokes. Legitimate uses of these facilities enable the creation of sophisticated Web pages. For example, consider how Google and Yahoo! searches react to the keys you type in order to suggest a possible search string.

Exploiting security weaknesses in a Web site, a spy embeds a scripted key-logger into one of the pages in the site. These key-logger are practically indistinguishable from other scripts on the same site, and can use the same script facilities to react to your keystrokes, record them or transmit them to a third-party site.

### Defending Against Key-Logger

Sandboxie is not designed to detect or disable key-loggers, but it is designed to make sure that sandboxed software stays in the sandbox, that such software can't integrate into Windows, and that it can be completely discarded when you delete the sandbox.

This means that if you take care to carry out all untrusted activity in the sandbox, you can always delete the sandbox to undo the effects of that activity, and restore your computer to a trusted state.

The first step is to make sure your system is not infected by malicious key-loggers, prior to using Sandboxie. A system scan by an anti-virus or anti-malware tool should help here.

Then carry out all untrusted activity -- such as browsing the Web, reading email, and testing unknown programs -- only in the restricted area of the sandbox. This doesn't mean you won't be infected by key-loggers, but it does mean you can get rid of them:

*   You can make sure you stop all of them, by telling Sandboxie to stop all activity in all sandboxes.
    *   See also the **Terminate All Programs** command in the [File Menu](FileMenu.md#terminate-all-programs) and the [Tray Icon Menu](TrayIconMenu.md#terminate-all-programs).
*   Once stopped, you can discard the traces of their program code, by deleting the contents of the sandbox.
    *   See also [Delete Sandbox](DeleteSandbox.md).

Once discarded, they can no longer record your keyboard activity, and you are safe to browse to trusted sites and enter your passwords.

Note that if you don't like to regularly delete your sandbox, you can set aside one sandbox for trusted browsing, and delete just that sandbox before carrying out the trusted activity. But it is still important to first stop all sandboxed activity in all sandboxes, for maximum protection.

* * *

Another protection measure against a key-logger is to configure Sandboxie to deny access to the Internet for anything other than your Web browser, in an attempt to prevent the key-logger from sending out the recorded information. See the setting for "the only program that can access the Internet" in [Program Settings](ProgramSettings.md#internet).

Note two caveats:

*   The Internet access feature is neither a replacement for a proper firewall, nor was it designed as a mechanism to counter or hinder key-loggers.

*   Some key-loggers could possibly circumvent the Internet access restriction by hijacking the Web browser to be used as a vehicle through which to send out the recorded information.

* * *

Go to [Help Topics](HelpTopics.md), [Usage Tips](UsageTips.md).
