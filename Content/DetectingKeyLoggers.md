# Detecting Key Loggers

For more detailed information, please refer to [Help Topics](HelpTopics.md) and [Usage Tips](UsageTips.md).

---

## Overview

Detecting all classes of key-loggers poses a significant challenge. This section categorizes key-loggers into various classes and explores potential defenses against them.

### External Key-Loggers

External (hardware) key-loggers, such as devices connected to the computer, are beyond the reach of software running within Windows. Sandboxie cannot detect or protect against these devices.

### Rootkit Key-Loggers

Rootkit key-loggers operate at a low software level, often as secondary keyboard hardware drivers. Sandboxie effectively blocks their installation, as they require explicit help from the operating system.

### Windows Hook Key-Loggers

These key-loggers request the operating system to load or "hook" them into every program executing on the desktop. Sandboxie partially honors these requests, applying the hook only to applications in the same sandbox.

### Windows Message Key-Loggers

Operating within the same process space as the logged program, these key-loggers intercept keyboard input messages sent by the operating system to the program. Detecting them is challenging for a supervisory program like Sandboxie.

### Scripted Key-Loggers

Scripted key-loggers target and compromise websites, reacting to keystrokes using languages like JavaScript or VBScript. They are challenging to distinguish from legitimate scripts on the site.

## Defending Against Key-Loggers

Sandboxie is not designed to detect or disable key-loggers but ensures sandboxed software stays within the sandbox. By confining untrusted activities to the sandbox, users can delete the sandbox to undo any potential effects and restore their system to a trusted state.

1. **Pre-Sandboxie Steps:**
   - Scan your system with an anti-virus or anti-malware tool to ensure it's not infected by key-loggers.

2. **Sandboxed Activity:**
   - Perform untrusted activities (e.g., browsing, email, testing unknown programs) only in the sandbox.

3. **Termination and Deletion:**
   - Stop all sandboxed activity using the **Terminate All Programs** command.
   - Delete the sandbox to discard traces of key-loggers' program code.

4. **Internet Access Restriction:**
   - Configure Sandboxie to deny internet access for anything other than your web browser. This aims to prevent key-loggers from sending out recorded information.

**Important Notes:**
- Internet access restriction is not a replacement for a firewall and was not designed as a primary defense against key-loggers.
- Some key-loggers may attempt to bypass internet access restrictions by exploiting the web browser to transmit recorded information.

For additional details, refer to [Help Topics](HelpTopics.md) and [Usage Tips](UsageTips.md).
