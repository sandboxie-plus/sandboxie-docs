# FAQ Virus

Questions and answers regarding Sandboxie and viruses and malware. For brevity, the text below mentions only viruses, but it equally applies to malware.

Sandboxie protects your from viruses, malware, ransom-ware, zero day threats, etc. Sandboxie does not need to rely on virus database signature updates, heuristics, etc.

If you get a virus in your sandbox, you simply delete the contents of that sandbox and move along. Your host machine, software and browser is not touched. Nothing on your host machine is harmed.

### Q. What does malicious software do?

A. Malicious software is typically designed to infect your computer. This infection is accomplished by the integration with, or the taking over of, various aspects of your Windows operating system. Following this infection, different types of malicious software have different goals. For example, a virus program might spread to more computers, and a spyware program might record your keyboard activity.

### Q. How does Sandboxie protect against computer viruses?

A. Sandboxie considers the program it supervises as potentially harmful, and keeps the programs bound within a _sandbox_, which is a kind of protective bubble. The program cannot escape the sandbox, and therefore cannot change, harm or infect your computer in any way. When you're done with the program, you delete the sandbox.

### Q. Does Sandboxie remove viruses?

A. Yes, but not in the sense that Sandboxie discards just the viruses, and leaves everything else intact. What Sandboxie does is delete the entire sandbox, which deletes any viruses trapped within the sandbox, as well as any other changes (good or bad) that were attempted by the program running under the supervision of Sandboxie.

### Q. Is Sandboxie an anti-virus?

A. No. While Sandboxie is a countermeasure against malicious software, it works differently from traditional anti-virus software. Unlike an anti-virus, Sandboxie does not attempt to identify or differentiate between "good" and "bad" (or harmful) programs. An anti-virus might not identify a new virus, and might let it slip by and infect your computer. Sandboxie, on the other hand, considers all programs as potentially harmful, and does not let any program modify your computer in any way.

### Q. Should I use Sandboxie instead of anti-virus software?

A. No. Sandboxie can prevent a virus in the sandbox from escaping into your real computer. However, common sense dictates that it is preferable to prevent the virus from running in the first place. Therefore it is a good idea to use anti-virus software to prevent known threats, while relying on Sandboxie to be your first line of defense against threats that are not yet known to the anti-virus.

### Q. Is Sandboxie 100% fool-proof?

A. No, but it tries to be as close as possible to 100%. At the same time, it is important to remember that Sandboxie is never the only software in your computer. Your other software, including your Windows operating system, might have security holes that could be abused by viruses in ways that no security software can prevent. Therefore it is always important to keep up with software updates. As the saying goes: "The only truly secure computer is one buried in concrete, with the power turned off and the network cable cut."

### Q. Can the anti-virus detect a virus in the sandbox?

A. Yes. Files contained in the sandbox are stored in the hard disk, typically in the folder SANDBOX in drive C. Programs under the supervision of Sandboxie can only operate within this folder, but there is nothing special about the folder itself. The anti-virus software may detect viruses as they arrive into this folder, or at any later time.

### Q. How should I respond to the anti-virus detecting a virus

A. Your anti-virus should tell you where the virus was identified. If the virus was identified within the sandbox (typically, in the SANDBOX folder in drive C), there is little cause for alarm. You can immediately invoke the [Delete Sandbox](DeleteSandbox.md) command, or you may direct the anti-virus to delete the virus file, or move it to quarantine.

### Q. When the anti-virus moves a virus file out of the sandbox and into quarantine, does it bypass Sandboxie?

A. No. The anti-virus itself is not operating under the supervision of Sandboxie, even if the virus alert seems to indicate otherwise. Operating outside the sandbox, the anti-virus can reach into the sandbox folder, pull the virus file, and move it into quarantine. The process is similar to Sandboxie [Quick Recovery](QuickRecovery.md), wherein [Sandboxie Control](SandboxieControl.md) reaches inside the sandbox to pull some file out of it.

### Q. Will viruses remain in the sandbox after I close all programs in the sandbox?

A. Yes and no:

1\. No, if your sandbox is set to [automatically](DeleteSettings.md#invocation) delete;
2\. Yes, in the configuration, but only until you [manually](DeleteSandbox.md) delete the contents of the sandbox.

It is important to note that a virus file in the sandbox is just that -- _a file_, not much different from your average text file. Unless you move the file out of the sandbox and invoke it, there is little cause for alarm.

### Q. Do I have to securely wipe the contents of the sandbox to make sure the virus is gone?

A. No. Although you can [configure](SecureDeleteSandbox.md) Sandboxie to use a third-party data wiping utility, the key point is to make the virus file itself inaccessible, and this is accomplished even with non-secure deletion. There is, however, an advantage to secure deletion, as discussed in the next answer.

### Q. Why does my anti-virus detect a virus in the _System Volume Information_ folder?

A. The System Restore component in Windows collects various files into the _System Volume Information_ when they are deleted. While the intention is to protect your system, sometimes System Restore ends up making copies of virus files. These virus files are inactive, and even if restored, will be restored into the sandbox, so there is little cause for alarm. Nevertheless, it is a good idea to let your anti-virus get rid of any such virus files.
Note that this will not occur if you securely wipe the contents of the sandbox (see previous question).

### Q. My computer is already infected with a virus, will Sandboxie protect against that virus?

A. No. Sandboxie can only protect your computer from the programs that run under the supervision of Sandboxie. The virus which has already infected your computer is running unencumbered outside the supervision of Sandboxie. It might also serve as an infection channel and assist other viruses in the sandbox to break out of the sandbox and infect your computer. It is strongly recommended that you dis-infect your computer as soon as possible, then install Sandboxie to protect against future threats.

### Q. Does Sandboxie protect against the KillDisk virus?

A. Yes. The KillDisk virus works by modifying the hard disk partition directly, bypassing any file systems. This kind of access has been blocked since Sandboxie version 2.33 (early 2006).

### Q. Can I install an anti-virus (or firewalls or other security software) into the sandbox?

A. For most security software, the answer is no. This type of software wants to integrate with Windows in order to monitor access to files and network connections. Sandboxie is designed to isolate programs in the sandbox from the rest of the system, which means the security software will be unable to monitor the system correctly. Note that virus scanner software which does not include active ("real time") monitoring should be able to function correctly under Sandboxie. Please note: Not all Anti-virus "suites" will work. Sandboxie may not function with certain suites (Kaspersky.)
