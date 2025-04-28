# Portable Sandbox

The revised [layout of the sandbox](SandboxHierarchy.md) that is introduced in version 2.80 allows for greater portability of the sandbox across computers. By redirecting programs to create sandboxed objects which have a nonspecific path, it is possible to populate a sandbox on one computer, then carry this sandbox to another computer and keep using it.

For example, consider installing a game program to a portable device such as a USB memory stick which is mounted as drive P. The game may install its files to a folder on drive P, but any menu shortcuts it creates will be installed in the Windows Start menu of the local computer, outside drive P. And any registry keys it creates will also be created in the Windows registry, also outside the USB device.

By contrast, if you set the [container folder](SandboxMenu.md#set-container-folder) to drive P (for instance _P:\Sandbox_), then install the game into the (sandboxed) drive C, then _all_ objects created by the installation will be redirected to drive P.

You can then carry the USB drive to another computer where Sandboxie is installed, and set the container folder on that other computer to drive P. Through the Sandboxie Start menu, you will see the menu shortcuts installed by the game, and when you start it, the game will find its settings as they were recorded in the sandboxed registry.

Note that Sandboxie itself is not portable software, but it facilitates the portability of a large number of applications.
