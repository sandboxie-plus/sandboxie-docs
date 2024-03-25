# Getting Started Part Six

### Part Six: Conclusion

This tutorial has walked you through the basic principles of using and understanding Sandboxie:
```
  * How to use Sandboxie to run your applications
  * How the changes are trapped in the sandbox
  * How to recover important files and documents out of the sandbox
  * How to delete the sandbox
```

You can read more tips about using Sandboxie in the [Usage Tips](UsageTips.md) page, and in pages about specific web browsers: [Internet Explorer Tips](InternetExplorerTips.md) and [Firefox Tips](FirefoxTips.md).

An important point to keep in mind when using Sandboxie is that it is designed to isolate programs from each other. Therefore you should expect to lose _a small_ measure of interoperability between programs. For example:

*   Email: Clicking email (_mailto_) links typically causes your web browser to start your email software. This will not work correctly unless Sandboxie is configured to run your email software in that sandbox. See [FAQ Email](FAQEmail.md).



*   You can avoid this problem by right-clicking the email link instead of left (normal) clicking it. The right-click menu will let you **copy** the email address. Then switch to your email software and **paste** the email address. If the pasted email address begins with a **mailto:** prefix, then make sure to **delete** that prefix, including the colon (:).



*   Download manager: Clicking download links is intercepted and handled by software which is operating outside your web browser. When the web browser is running in a sandbox, this might cause it to start the download manager in the sandbox as well, which would probably not be the desired result.



*   You can avoid this problem by right-clicking the download link instead of left (normal) clicking it. The right-click menu will let you **copy** the link. Then switch to your download manager program, and **paste** the link to start the download process.



On the other hand, you should not expect to lose _every_ measure of interoperability between programs. For example, you may use a dictionary software which should react to keystrokes or mouse-clicks to display information in a pop-up window. Sandboxie may or may not interfere with this, depending on how the dictionary software is designed. When things do not work as expected, please report it on the Sandboxie support and ask for a solution.

* * *

Please also take some time now to review the many settings in the [Sandbox Settings](SandboxSettings.md) window. The settings are explained clearly, and you will find many settings that allow you to find the best balance between security and convenience.

For example, one person may prefer greater security and control over web bookmarks and favorites, by letting them first save into the sandbox, and then recovering selected items through [Quick Recovery](QuickRecovery.md) or [Immediate Recovery](ImmediateRecovery.md). (This is the default configuration in Sandboxie.)

But another person may prefer to configure Sandboxie such that a sandboxed web browser can directly access the bookmarks or favorites, without an intermediate recovery step, thus sacrificing some security for greater convenience.

Sandboxie allows you to find your personal balance of security and convenience.

Enjoy!

* * *

This is the end of the tutorial. Go back to [Help Topics](HelpTopics.md), where you can read more [Usage Tips](UsageTips.md).
