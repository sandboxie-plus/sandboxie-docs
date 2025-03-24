# Programs View

[Sandboxie Control](SandboxieControl.md) > [View Menu](ViewMenu.md) > [Programs](ViewMenu.md#programs)

![](../Media/MainWindow.png)

The _Programs View_ is the default view mode in [Sandboxie Control](SandboxieControl.md). The programs running in each sandbox are displayed here, grouped by sandbox name. The list shows three columns:

*   The _Program Name_ column displays the name of the executable file of the program. For example, the picture shows _iexplore.exe_, which is the executable name for Internet Explorer.
    *   For a row describing a sandbox, this column displays the name of the sandbox.

*   The _PID_ column displays the process ID of the program. This is the same number that appears in the Processes tab of the Windows Task Manager. (The Windows Task Manager appears when you press the Ctrl+Shift+Esc keyboard shortcut or Ctrl+Alt+Del, which leads to the Windows logon screen.)
    *   For a row describing a sandbox, this column displays _Active_ if any programs are running in the sandbox.

*   The _Window Title_ column displays the title associated with the main window of the program.

Use the small _+_ or _-_ icon, located at the start of each _Active_ sandbox row, to expand or collapse the display of programs in the sandbox.

**Context Menus**

The _Programs View_ provides context menus for sandboxes and programs. To display a context menu for the item (sandbox or program) in some row, do one of the following:

*   Click the right mouse button anywhere on the row.

*   Select (highlight) the row using the mouse or keyboard, then press Shift+F10.

*   Select (highlight) the row using the mouse or keyboard, then use the [View Menu -> Context Menu](ViewMenu.md#context-menu) command.

For a sandbox row, the context menu displayed is the same as [Sandbox Menu -> Sandbox Sub-Menu](SandboxMenu.md#sandbox-sub-menu). See there for a full description.

For a program row, the context menu offers the following commands:

*   The _Terminate Program_ command terminates the program.

*   The _Program Settings_ command displays the [Program Settings](ProgramSettings.md) window for the program.

*   The _Resource Access_ command displays the [Sandbox Settings > Resource Access](ResourceAccessSettings.md) group of settings pages, where the program name is preselected in the program name filter (_The list above applies to_ filter).

* * *

Go to [Sandboxie Control](SandboxieControl.md), [Files And Folders View](FilesAndFoldersView.md), [Help Topics](HelpTopics.md).
