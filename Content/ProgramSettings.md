# Program Settings

### Overview

The Program Settings window is a quick way to configure some of the aspects of Sandboxie. To access the window, right-click on the name of a running sandboxed program to show the context menu, and select _Program Settings_:

![](https://xanasoft.com/wp-content/uploads/2020/10/ProgramSettingsContextMenu.png)

(You can also use Shift+F10 or the View menu to show the context menu.)

The Program Settings window displays the sandbox where the program is running, the name of the program executable file, and checkboxes for the quick configurations settings. It is composed of two pages. Switch between the pages using the _View Page 1_ and _View Page 2_ radio buttons.

* * *

### Page 1

![](https://xanasoft.com/wp-content/uploads/2020/10/ProgramSettingsPage1.png)

**Program Start**

These settings control how Sandboxie handles programs that start outside any sandbox.

<a name="alert" id="alert"></a>

*   **Issue alert message SBIE1301**
    *   Sandboxie will issue message [SBIE1301](SBIE1301) whenever this program starts outside any sandbox.
    *   See also [Configure Menu > Alert Programs](ConfigureMenu#alert).

<a name="force" id="force"></a>

*   **Force program to run in this sandbox**
    *   Sandboxie will automatically force the program to run in this sandbox.
    *   See also [Sandbox Settings > Program Start > Forced Programs](ProgramStartSettings#program).

**Program Stop**

These settings control how Sandboxie handles this program stopping in this sandbox.

<a name="linger" id="linger"></a>

*   **Stop this program if it lingers in the sandbox after other programs have ended**
    *   Sandboxie will automatically terminate this program if it remains running when all other programs stopped.
    *   See also [Sandbox Settings > Program Stop > Lingering Programs](ProgramStopSettings#linger).

<a name="leader" id="leader"></a>

*   **Stop other programs after this leader program has ended**
    *   Sandboxie will terminate every other program in the sandbox when this program stops.
    *   See also [Sandbox Settings > Program Stop > Leader Programs](ProgramStopSettings#leader).

* * *

### Page 2

![](https://xanasoft.com/wp-content/uploads/2020/10/ProgramSettingsPage2.png)

These settings control which restrictions apply to this program.

**Internet Restrictions**:

<a name="internet" id="internet"></a>

*   **Enable restrictions and allow this program to connect to the Internet**
    *   Enable Internet restrictions in the sandbox, which means no program can connect to the Internet unless explicitly allowed.
    *   Additionally, explicitly allows this program to connect to the Internet from this sandbox.
    *   See also [Sandbox Settings > Restrictions > Internet Access](RestrictionsSettings#internet).

**Start/Run Restrictions**:

<a name="startrun" id="startrun"></a>

*   **Enable restrictions and allow this program to start**
    *   Enable Start/Run restrictions in the sandbox, which means no program can start unless explicitly allowed.
    *   Additionally, explicitly allows this program to start and run in this sandbox.
    *   See also [Sandbox Settings > Restrictions > Start/Run Access](RestrictionsSettings#startrun).
