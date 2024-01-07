# Portable Sandbox

Version 2.80 introduces a revised layout for the sandbox, enhancing portability across computers. This is achieved by redirecting programs to create sandboxed objects with nonspecific paths, allowing users to create a sandbox on one computer and seamlessly transfer it to another.

**Example Scenario:**
Imagine installing a game program on a USB memory stick mounted as drive P. If the game installs files to a folder on drive P, but creates shortcuts in the local computer's Start menu and registry keys outside the USB device, portability becomes challenging.

**Sandboxie Solution:**
By setting the [container folder](SandboxMenu.md#set-container-folder) to drive P (e.g., _P:\Sandbox_), installing the game into the sandboxed drive C ensures that all objects created during installation are redirected to drive P.

**Portability Steps:**
1. Install the game into the (sandboxed) drive C.
2. Carry the USB drive to another computer with Sandboxie installed.
3. Set the container folder on the other computer to drive P.

**Benefits:**
- Menu shortcuts installed by the game are accessible through the Sandboxie Start menu.
- The game retrieves its settings from the sandboxed registry, maintaining consistency across different computers.

**Note:**
Sandboxie itself is not portable software, but it significantly enhances the portability of numerous applications.
