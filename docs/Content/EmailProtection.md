# Email Protection

For a shorter version of this discussion, see [FAQ Email](FAQEmail.md).

* * *

It is not uncommon to receive virus in an email message. Traditionally, your anti-virus and anti-spyware software works with your email software to identify malicious software as soon as it is received, or at least, as soon as it begins to execute in your computer. That works well for well-known viruses and spyware, but leaves you vulnerable to [zero-day exploits](https://en.wikipedia.org/wiki/Zero-day_(computing)), that is, vulnerable to malicious software that is not yet properly identified by the security software.

Sandboxie offers another approach. If you run your email reader program _sandboxed_ under the control of Sandboxie, this protection will also extend to any software spawned by the email reader, such as viruses and spyware, thus severely limiting the effects of the malicious software on your computer.

For example, suppose you get an email message with the a virus that presents itself as an attachment called _Click_Me_For_Best_Joke_Ever.exe_. Suppose you don't know this is a virus, and further suppose that your anti-virus has not yet been updated to identify this particular virus. You click the attachment, and it delivers the best joke ever, but it also secretly installs malicious software.

This example may not specifically name any known virus, but it is not at all farfetched. [Quoting Wikipedia on Malware](https://en.wikipedia.org/wiki/Malware#Purposes): _"Since 2003, the majority of widespread viruses and worms have been designed to take control of users' computers for illicit purposes ..."_ See also: [Construction (from Wikipedia)](https://en.wikipedia.org/wiki/Botnet#Construction).

If you run your email program sandboxed, then _Click_Me_For_Best_Joke_Ever.exe_ also runs sandboxed, and any changes it makes to the computer, or software it installs, will be confined to the sandbox. These changes will be discarded in their entirety as soon as you delete the sandbox.


#### Sandboxie is not an anti-virus, and will neither identify or warn about viruses. However, Sandboxie treats all software it runs as potentially malicious software which cannot be trusted, and will not let any program -- malicious or legitimate -- to break out of the sandbox and make permanent changes to your computer.


Note that the virus itself, in its original form as an email attachment, will remain in your mailbox even after you delete the sandbox. However, a computer virus is a piece of software, not a living creature: It cannot cause any harm your computer by merely being stored in your mailbox. It must be invoked before it can cause harm. Thus if you always run your email program sandboxed, the worst that can happen is that you will rerun the virus inside the sandbox, and then delete the sandbox again. Eventually, your anti-virus will be updated to identify this attachment as malicious software.

* * *

The following section is concerned with configuring the use of email software with Sandboxie.

You may access your email online via a Web browser running under Sandboxie, as is the case with Hotmail, Yahoo! or Gmail, to name three of the many Web mail services. In that case, no special configuration is necessary, and the following section is not relevant.

* * *

The Sandboxie protection comes at a small cost: You should always keep in mind that Sandboxie considers all content created within the sandbox as discardable content.

This means for example, that a malicious program installed by a virus is placed in the sandbox and considered discardable. But it also means that if you save an email message to a file, then that file is also put in the sandbox and will be discarded when the sandbox is deleted. **And most importantly,** this means that Sandboxie will treat incoming new mail as discardable content.

For this reason, you _must_ configure Sandboxie to treat your mailbox data files as trusted content, or you stand to lose important information. To protect against accidental loss of data, Sandboxie will issue message [SBIE2212](SBIE2212.md) if you run your email program without first properly configuring Sandboxie.

Sandboxie offers easy configuration for most popular email reader programs. See [Sandbox Settings > Applications > Email Reader](ApplicationsSettings.md#email-reader).

You may also need to tell Sandboxie where your mailbox data files reside, in the following cases:

*   If your mailbox resides in a non-default or non-standard location.
*   If you use the Eudora or The-Bat! email software.

To do that, open [Sandbox Settings > Applications > Folders](ApplicationsSettings.md#folders), select your email software from the drop-down list, and then select a folder location to be associated with it.

After completing the email configuration, you may want to test it, to make sure that even when running under Sandboxie, new emails are not lost when you delete the sandbox. To do that, follow the steps outlined in [Test Email Configuration](TestEmailConfiguration.md).
