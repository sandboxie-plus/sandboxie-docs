# 启动命令行

根据为 Sandboxie Start 程序指定的命令行参数，它可以执行以下任何操作：

*   [启动](#启动程序)受 Sandboxie 监管的程序
*   [停止](#停止程序)沙箱内的程序
*   [列出](#列出程序)沙箱内的程序
*   [删除](#删除沙箱内容)沙箱的内容
*   [重新加载](#重新加载配置) Sandboxie 配置
*   启动[禁用强制程序](#禁用强制程序)模式
*   [相关](#相关阅读材料)阅读材料

* * *
### 启动程序

这是默认行为。通过指定程序可执行文件的完整或部分路径，Sandboxie Start 将在 Sandboxie 的监管下启动该程序：
```
  "C:\Program Files\Sandboxie\Start.exe"  c:\windows\system32\notepad.exe
  "C:\Program Files\Sandboxie\Start.exe"  notepad.exe
```

允许使用两个特殊的程序名称：
```
  "C:\Program Files\Sandboxie\Start.exe"  default_browser
  "C:\Program Files\Sandboxie\Start.exe"  mail_agent
```

根据指定的参数，Sandboxie Start 还可以显示“运行任何程序”对话框窗口或 Sandboxie 开始菜单：
```
  "C:\Program Files\Sandboxie\Start.exe"  run_dialog
  "C:\Program Files\Sandboxie\Start.exe"  start_menu
```

在所有形式中，参数 _/box:沙箱名称_ 都适用，并且可以在 Start.exe 和参数之间指定，以指示除默认的 _DefaultBox_ 之外的沙箱名称。例如：
```
  "C:\Program Files\Sandboxie\Start.exe"  /box:TestBox  run_dialog
```

/box 参数的一种特殊形式是 _/box:__ask___，它会使 Start.exe 显示沙箱选择对话框。

参数 _/silent_ 可用于消除一些弹出错误消息。例如：
```
  "C:\Program Files\Sandboxie\Start.exe"  /silent  no_such_program.exe
```

在静默和正常操作中，Start.exe 在成功时以零退出代码退出，失败时以非零退出代码退出。在批处理文件中，可以使用 _IF ERRORLEVEL_ 条件检查退出代码。

参数 _/elevate_ 可用于在启用了用户账户控制 (UAC) 的系统上以管理员权限运行程序。例如：
```
  "C:\Program Files\Sandboxie\Start.exe"  /elevate cmd.exe
```

参数 _/env_ 可用于传递环境变量：
```
  "C:\Program Files\Sandboxie\Start.exe"  /env:VariableName=VariableValueWithoutSpace
  "C:\Program Files\Sandboxie\Start.exe"  /env:VariableName="Variable Value With Spaces"
```

参数 _/hide_window_ 可用于指示启动的程序不应显示其窗口：
```
  "C:\Program Files\Sandboxie\Start.exe"  /hide_window cmd.exe /c automated_script.bat
```

参数 _/wait_ 可用于运行程序，等待其完成，并返回程序的退出状态：
```
  "C:\Program Files\Sandboxie\Start.exe"  /wait cmd.exe
```

请注意，Start.exe 是一个 Win32 应用程序，而不是控制台应用程序，因此系统的 "start" 命令在此处很有用，可以强制系统等待 Start.exe 完成：
```
  start /wait "C:\Program Files\Sandboxie\Start.exe" /wait cmd /c exit 9
  echo %ERRORLEVEL%
  9
```

系统等待 Start.exe 完成，而 Start.exe 又等待 "cmd /c exit 9" 完成，然后退出状态 9 一直返回。

参数可以按任何顺序组合。例如：
```
   "C:\Program Files\Sandboxie\Start.exe"  /box:CustomBox /silent MyProgram.exe
```

### 停止程序

终止在特定沙箱中运行的所有程序。请注意，该请求会传输到 Sandboxie 服务 SbieSvc，该服务实际执行终止操作。
```
  "C:\Program Files\Sandboxie\Start.exe"  /terminate
  "C:\Program Files\Sandboxie\Start.exe"  /box:TestBox  /terminate
  "C:\Program Files\Sandboxie\Start.exe"  /terminate_all
```

如果省略参数 _/box:沙箱名称_，则将停止在默认沙箱 _DefaultBox_ 中运行的程序。

形式 _/terminate_all_ 会终止所有沙箱中的所有程序。

* * *

### 卸载沙箱镜像

这些命令用于卸载由 Sandboxie Plus 创建的加密沙箱镜像或 RAM 磁盘。这些参数从 v1.11.0 / 5.66.0 版本开始可用。
```
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /unmount
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /box:EncryptedBox  /unmount
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /unmount_all
```

如果省略参数 _/box:沙箱名称_，则将卸载默认沙箱 _DefaultBox_ 的镜像。

形式 _/unmount_all_ 会终止所有加密沙箱中的所有程序，并卸载所有加密沙箱镜像，包括由 Sandboxie Plus 创建的 RAM 磁盘。

### 挂载沙箱镜像

这些命令用于挂载由 Sandboxie Plus 创建的加密沙箱镜像。这些参数从 v1.11.0 / 5.66.0 版本开始可用。
```
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /key:[box image password] /mount_protected
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /key:[box image password] /mount
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /box:EncryptedBox  /key:[box image password] /mount_protected
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /box:EncryptedBox  /key:[box image password] /mount
```

如果省略参数 _/box:沙箱名称_，则将挂载默认沙箱 _DefaultBox_ 的镜像。

形式 _/mount_protected_ 会以“沙箱根保护”模式挂载加密沙箱镜像。“沙箱根保护”可防止在沙箱外部运行的进程访问加密沙箱的根文件夹。

* * *

### 列出程序

列出在特定沙箱中运行的所有程序的系统进程 ID 号。
```
  "C:\Program Files\Sandboxie\Start.exe"  /listpids
  "C:\Program Files\Sandboxie\Start.exe"  /box:TestBox  /listpids
```

如果省略参数 _/box:沙箱名称_，则将列出在默认沙箱 _DefaultBox_ 中运行的程序。

输出格式为每行一个数字。第一行包含程序的数量，随后每行一个进程 ID。示例输出：
```
    "C:\Program Files\Sandboxie\Start.exe"  /listpids | more
    3
    3036
    2136
    384
```

请注意，Start.exe 不是控制台应用程序，因此除非使用 `| more` 之类的结构对输出进行管道处理，否则输出不会显示在命令提示符窗口中。

* * *

### 删除沙箱内容
```
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_silent
```

可以在 Start.exe 和删除命令之间指定 _/box:沙箱名称_ 参数。

删除命令中的 __silent_ 后缀表示 Sandboxie Start 应静默忽略任何错误，并且不显示任何错误消息。

删除操作分两个阶段进行：

*   阶段 1：扫描沙箱的内容，并处理在第二阶段可能会造成问题的文件：
    *   删除符号链接（也称为重解析点）。
    *   使只读文件和目录具有完全访问权限。
    *   将名称非常长的文件和目录重命名为较短的名称。
    *   将沙箱重命名为 `__Delete_(沙箱名称)_(某个随机数)` 格式。例如，如果沙箱是 DefaultBox，则可能会重命名为 `__Delete_DefaultBox_01C4012345678912`。

*   阶段 2：删除在阶段 1 中处理过的任何沙箱。
    *   在阶段 1 中处理过的沙箱是那些已按上述方式重命名的沙箱。
    *   在阶段 2 中可能会删除多个沙箱。
    *   默认情况下，使用标准系统命令 RMDIR 来删除重命名后的沙箱文件夹。
    *   或者，可以使用第三方删除实用程序。请参阅[安全删除沙箱](SecureDeleteSandbox.md)。

发出 _delete_sandbox_ 命令会使 Start.exe 依次调用阶段 1 和阶段 2。Start.exe 还接受以下命令来调用特定阶段：
```
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_phase1
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_phase2
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_silent_phase1
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_silent_phase2
```

* * *

### 重新加载配置

此命令将 SandboxieIni 中的 Sandboxie 配置重新加载到活动的 Sandboxie 驱动程序中。通常在手动编辑 Sandboxie.ini 文件后很有用。
```
  "C:\Program Files\Sandboxie\Start.exe"  /reload
```

请注意，重新加载配置对在发出此命令时已经在运行的沙箱程序不会生效。

* * *

### 禁用强制程序

以下命令可使程序在沙箱外部运行，即使该程序是被强制在沙箱内运行的。这类似于在“运行沙箱程序”命令的沙箱选择窗口中使用“在沙箱外部运行”选项。
```
  "C:\Program Files\Sandboxie\Start.exe"  /dfp            c:\path\to\program.exe
  "C:\Program Files\Sandboxie\Start.exe"  /disable_force  c:\path\to\program.exe
```

请注意，/dfp 和 /disable_force 是相同的。您还可以在单击“运行沙箱程序”命令时按住 Ctrl 和 Shift 键来选择此选项。

此命令的旧形式可以临时为所有程序禁用强制程序模式。其功能类似于在 Sandboxie Control 的[托盘图标菜单](TrayIconMenu.md#禁用强制程序)（而不是[文件菜单](FileMenu.md#禁用强制程序)）中使用“禁用强制程序”命令。
```
  "C:\Program Files\Sandboxie\Start.exe"  disable_force
```

请注意，此命令语法中缺少斜杠。还要注意，此命令不是一个切换开关。它总是会启用“禁用强制程序”模式，并始终重新启动倒计时计时器。目前，Start.exe 不提供取消此模式的方法。

* * *

### 相关阅读材料

另请参阅：[注入 DLL](InjectDll.md) 和 [SBIE DLL API](SBIEDLLAPI.md)

转到[帮助主题](HelpTopics.md)。