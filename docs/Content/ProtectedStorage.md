# Protected Storage

Protected Storage (hereafter PStore) was a small memory space available until Windows 7, managed by the system security component, and usable by applications. Applications that needed to store sensitive information, such as passwords, could use PStore rather than implement means to encrypt and protect that information.

Note that PStore memory of one user account is not accessible by another user account; but all programs running in the same user account can see and change information entered into the memory store by any other application.

The best application example is Internet Explorer version 6, which uses PStore to store AutoComplete history (such as the Google search box) and passwords in Web forms.

(Note that Internet Explorer version 7 still encrypts this information, but no longer uses PStore to do it. Presumably this is an effort to hide the sensitive information from other programs -- most likely spyware that may be running in the same user account.)

Sandboxie can provide its own implementation of PStore, for sandboxed applications. This is the default setting, unless altered in [Sandbox Settings > Applications > Web Browser](ApplicationsSettings.md#web-browser).

The Sandboxie PStore is stored in the file _SbiePst.dat_ in the **sandboxed** _Windows_ folder.

The Sandboxie implementation of PStore encrypts data using a _much weaker_ method than what the system security component would have done. However, information entered into the Sandboxie PStore will likely disappear quickly, as part of the process of deleting the sandbox.
