# 启动命令行

根据为 Sandboxie Start 程序指定的命令行参数，它可以执行以下任何操作：

*   [启动](#启动程序) 受 Sandboxie 监管的程序
*   [停止](#停止程序) 沙盒内的程序
*   [卸载](#卸载沙盒镜像) 加密沙盒镜像
*   [挂载](#挂载沙盒镜像) 加密沙盒镜像
*   [列出](#列出程序) 沙盒内的程序
*   [删除](#删除沙盒内容) 沙盒的内容
*   [重新加载](#重新加载配置) Sandboxie 配置
*   启动 [禁用强制程序](#禁用强制程序) 模式
*   [相关](#相关阅读材料) 阅读材料

* * *
### 启动程序

这是默认行为。通过指定程序可执行文件的完整或部分路径，Sandboxie Start 将在 Sandboxie 的监管下启动该程序：
```pwsh
  "C:\Program Files\Sandboxie\Start.exe"  c:\windows\system32\notepad.exe
  "C:\Program Files\Sandboxie\Start.exe"  notepad.exe
```

允许使用两个特殊的程序名称：
```pwsh
  "C:\Program Files\Sandboxie\Start.exe"  default_browser
  "C:\Program Files\Sandboxie\Start.exe"  mail_agent
```

根据指定的参数，Sandboxie Start 还可以显示“运行任何程序”对话框窗口或 Sandboxie 开始菜单：
```pwsh
  "C:\Program Files\Sandboxie\Start.exe"  run_dialog
  "C:\Program Files\Sandboxie\Start.exe"  start_menu
```

在所有形式中，参数 _/box:沙盒名称_ 都适用，并且可以在 Start.exe 和参数之间指定，以指示除默认的 _DefaultBox_ 之外的沙盒名称。例如：
```pwsh
  "C:\Program Files\Sandboxie\Start.exe"  /box:TestBox  run_dialog
```

/box 参数的一种特殊形式是 _/box:\_\_ask\_\__，它会使 Start.exe 显示沙盒选择对话框。

参数 _/silent_ 可用于消除一些弹出错误消息。例如：
```pwsh
  "C:\Program Files\Sandboxie\Start.exe"  /silent  no_such_program.exe
```

在静默和正常操作中，Start.exe 在成功时以零退出代码退出，失败时以非零退出代码退出。在批处理文件中，可以使用 _IF ERRORLEVEL_ 条件检查退出代码。

参数 _/elevate_ 可用于在启用了用户账户控制 (UAC) 的系统上以管理员权限运行程序。例如：
```pwsh
  "C:\Program Files\Sandboxie\Start.exe"  /elevate cmd.exe
```

参数 _/env_ 可用于传递环境变量：
```pwsh
  "C:\Program Files\Sandboxie\Start.exe"  /env:VariableName=VariableValueWithoutSpace
  "C:\Program Files\Sandboxie\Start.exe"  /env:VariableName="Variable Value With Spaces"
```

参数 _/hide_window_ 可用于指示启动的程序不应显示其窗口：
```pwsh
  "C:\Program Files\Sandboxie\Start.exe"  /hide_window cmd.exe /c automated_script.bat
```

参数 _/wait_ 可用于运行程序，等待其完成，并返回程序的退出状态：
```pwsh
  "C:\Program Files\Sandboxie\Start.exe"  /wait cmd.exe
```

请注意，Start.exe 是一个 Win32 应用程序，而不是控制台应用程序，因此系统的 "start" 命令在此处很有用，可以强制系统等待 Start.exe 完成：
```pwsh
  start /wait "C:\Program Files\Sandboxie\Start.exe" /wait cmd /c exit 9
  echo %ERRORLEVEL%
  9
```

系统等待 Start.exe 完成，而 Start.exe 又等待 "cmd /c exit 9" 完成，然后退出状态 9 一直返回。

参数可以按任何顺序组合。例如：
```pwsh
   "C:\Program Files\Sandboxie\Start.exe"  /box:CustomBox /silent MyProgram.exe
```

### 停止程序

终止在特定沙盒中运行的所有程序。请注意，该请求会传输到 Sandboxie 服务 SbieSvc，该服务实际执行终止操作。
```pwsh
  "C:\Program Files\Sandboxie\Start.exe"  /terminate
  "C:\Program Files\Sandboxie\Start.exe"  /box:TestBox  /terminate
  "C:\Program Files\Sandboxie\Start.exe"  /terminate_all
```

如果省略参数 _/box:沙盒名称_，则将停止在默认沙盒 _DefaultBox_ 中运行的程序。

形式 _/terminate_all_ 会终止所有沙盒中的所有程序。

* * *

### 卸载沙盒镜像

这些命令用于卸载由 Sandboxie Plus 创建的加密沙盒镜像或 RAM 磁盘。这些参数从 v1.11.0 / 5.66.0 版本开始可用。
```pwsh
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /unmount
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /box:EncryptedBox  /unmount
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /unmount_all
```

如果省略参数 _/box:沙盒名称_，则将卸载默认沙盒 _DefaultBox_ 的镜像。

形式 _/unmount_all_ 会终止所有加密沙盒中的所有程序，并卸载所有加密沙盒镜像，包括由 Sandboxie Plus 创建的 RAM 磁盘。

### 挂载沙盒镜像

> [!WARNING]
> 在 `Start.exe` 上使用 `/key:password` 参数时，密码会显示在命令行历史、进程列表以及可能的事件日志中。请仅在安全环境中使用此参数，或考虑改用交互式密码提示。

这些命令用于挂载由 Sandboxie Plus 创建的加密沙盒镜像。这些参数从 v1.11.0 / 5.66.0 版本开始可用。
```pwsh
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /key:[box image password] /mount_protected
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /key:[box image password] /mount
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /box:EncryptedBox  /key:[box image password] /mount_protected
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /box:EncryptedBox  /key:[box image password] /mount
```

如果省略参数 _/box:沙盒名称_，则将挂载默认沙盒 _DefaultBox_ 的镜像。

形式 _/mount_protected_ 会以“沙盒根保护”模式挂载加密沙盒镜像。“沙盒根保护”可防止在沙盒外部运行的进程访问加密沙盒的根文件夹。

* * *

### 列出程序

列出在特定沙盒中运行的所有程序的系统进程 ID 号。
```pwsh
  "C:\Program Files\Sandboxie\Start.exe"  /listpids
  "C:\Program Files\Sandboxie\Start.exe"  /box:TestBox  /listpids
```

如果省略参数 _/box:沙盒名称_，则将列出在默认沙盒 _DefaultBox_ 中运行的程序。

输出格式为每行一个数字。第一行包含程序的数量，随后每行一个进程 ID。示例输出：
```pwsh
    "C:\Program Files\Sandboxie\Start.exe"  /listpids | more
    3
    3036
    2136
    384
```

请注意，Start.exe 不是控制台应用程序，因此除非使用 `| more` 之类的结构对输出进行管道处理，否则输出不会显示在命令提示符窗口中。

* * *

### 删除沙盒内容
```pwsh
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_silent
```

可以在 Start.exe 和删除命令之间指定 _/box:沙盒名称_ 参数。

删除命令中的 __silent_ 后缀表示 Sandboxie Start 应静默忽略任何错误，并且不显示任何错误消息。

删除操作分两个阶段进行：

*   阶段 1：扫描沙盒的内容，并处理在第二阶段可能会造成问题的文件：
    *   删除符号链接（也称为重解析点）。
    *   使只读文件和目录具有完全访问权限。
    *   将名称非常长的文件和目录重命名为较短的名称。
    *   将沙盒重命名为 `__Delete_(沙盒名称)_(某个随机数)` 格式。例如，如果沙盒是 DefaultBox，则可能会重命名为 `__Delete_DefaultBox_01C4012345678912`。

*   阶段 2：删除在阶段 1 中处理过的任何沙盒。
    *   在阶段 1 中处理过的沙盒是那些已按上述方式重命名的沙盒。
    *   在阶段 2 中可能会删除多个沙盒。
    *   默认情况下，使用标准系统命令 RMDIR 来删除重命名后的沙盒文件夹。
    *   或者，可以使用第三方删除实用程序。请参阅 [安全删除沙盒](SecureDeleteSandbox.md)。

发出 _delete_sandbox_ 命令会使 Start.exe 依次调用阶段 1 和阶段 2。Start.exe 还接受以下命令来调用特定阶段：
```pwsh
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_phase1
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_phase2
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_silent_phase1
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_silent_phase2
```

* * *

### 重新加载配置

此命令将 SandboxieIni 中的 Sandboxie 配置重新加载到活动的 Sandboxie 驱动程序中。通常在手动编辑 Sandboxie.ini 文件后很有用。
```pwsh
  "C:\Program Files\Sandboxie\Start.exe"  /reload
```

请注意，重新加载配置对在发出此命令时已经在运行的沙盒程序不会生效。

* * *

### 禁用强制程序

以下命令可使程序在沙盒外部运行，即使该程序是被强制在沙盒内运行的。这类似于在“运行沙盒程序”命令的沙盒选择窗口中使用“在沙盒外部运行”选项。
```pwsh
  "C:\Program Files\Sandboxie\Start.exe"  /dfp            c:\path\to\program.exe
  "C:\Program Files\Sandboxie\Start.exe"  /disable_force  c:\path\to\program.exe
```

请注意，/dfp 和 /disable_force 是相同的。您还可以在单击“运行沙盒程序”命令时按住 Ctrl 和 Shift 键来选择此选项。

此命令的旧形式可以临时为所有程序禁用强制程序模式。其功能类似于在沙盒管理器的 [托盘图标菜单](TrayIconMenu.md#禁用强制沙盒化程序)（而不是 [文件菜单](FileMenu.md#禁用强制程序)）中使用“禁用强制程序”命令。
```pwsh
  "C:\Program Files\Sandboxie\Start.exe"  disable_force
```

请注意，此命令语法中缺少斜杠。还要注意，此命令不是一个切换开关。它总是会启用“禁用强制程序”模式，并始终重新启动倒计时计时器。目前，Start.exe 不提供取消此模式的方法。

* * *

### 高级 / 内部开关

以下开关主要面向高级用法、自动化或内部/调试场景。它们实现在 Start.exe 的源码（`start.cpp`）中。这些选项可能随版本变化，通常终端用户不需要用到。

#### /keep_alive

让 Start.exe 保持运行并监督已启动的程序。该开关实现的是重启循环（监督器），而非简单的一次性等待。`start.cpp` 中实现的行为如下：

> [!Note]
> `/keep_alive` 仅在监督用的 Start.exe 实例运行于沙盒内（沙盒化实例）时有效。当在沙盒外运行时，它没有任何效果。

- Start.exe 捕获已启动进程的句柄（等待时使用带 `SEE_MASK_NOCLOSEPROCESS` 的 `ShellExecuteEx`/`CreateProcess`）。
- Start.exe 等待子进程退出，并通过 `GetExitCodeProcess` 读取其退出码。
- 若子进程以 `EXIT_SUCCESS`（零）退出，Start.exe 结束并返回该零退出码。
- 若子进程以非零码退出，且 `/keep_alive` 仍生效，Start.exe 将尝试重启该程序并再次监督。该循环会重试有限的次数：

    - 实现会递增一个重试计数器，当计数小于 5 时持续重试（即最多重试 5 次）。
    - 极短运行（代码将短于约 5 秒的运行视为初始化失败）会计入重试次数；较长的运行会重置失败计数器。

- 若程序完全无法启动，Start 会为该次调用禁用 keep-alive（不重试）。

简而言之：

- 当你希望 Start.exe 作为监督父进程、并在程序非正常退出时自动重启它（带小型重试/退避策略）时，请使用 `/keep_alive`。这与 `/wait` 不同：`/wait` 让 Start.exe 等待并在子进程退出后随之退出；`/keep_alive` 让 Start.exe 持续监督，并在子进程崩溃或以非零码退出时将其重启，直至达到重试上限。

最终结果：

- 成功（0）退出时，最终返回的退出码为 0。
- 若重试耗尽且程序持续以非零码退出，Start.exe 将停止重试并返回最后一次的非零退出码。

示例：
```cmd
"Start.exe" /keep_alive notepad.exe
"Start.exe" Start.exe /keep_alive notepad.exe
```
当你希望已启动的程序在沙盒内保持可用（崩溃后自动重启），并让 Start.exe 在整个会话期间保持监督父进程身份时，此功能很有用。

#### /fake_admin

将已启动的程序标记为在沙盒内拥有伪造的管理员上下文。这可以帮助某些会检测管理员状态并据此改变行为的安装程序或旧程序。这是一种沙盒侧的兼容性措施，与真正的 UAC 提升并不相同。

示例：
```cmd
"Start.exe" /fake_admin setup.exe
```

#### /force_children (or /fcp)

将已启动的进程标记为：它创建的任何子进程都会被强制进入指定的沙盒。它本身并不会将最初启动的程序（例如安装程序）放入沙盒。当存在此选项时，Start.exe 会发出 API 调用来强制子进程。

示例：
```cmd
"Start.exe" /fcp myinstaller.exe
"Start.exe" /force_children myinstaller.exe
```

#### /env:=Refresh

触发当前沙盒化进程的环境刷新。当从沙盒化实例调用时，Start.exe 会调用内部的 `Env_Refresh` 辅助函数；在沙盒外运行时没有任何效果。如需设置单个环境变量，请改用 `/env:Name=Value`。

示例：
```cmd
"Start.exe" /env:=Refresh
```

#### /uac_prompt

带参数调用 Sandboxie 的安全 UAC 提示 UI（沙盒化 UAC 对话框）。这主要是供其他 Sandboxie 组件用来显示安全 UAC 提示的内部辅助工具。该命令接受用于填充对话框的内部参数（通常由服务或代理代码生成）。

示例：
```cmd
"Start.exe" uac_prompt <internal-pkt-params>
```

#### mount_hive

请求沙盒化实例挂载一份注册表配置单元副本，供沙盒内程序访问。当在沙盒外调用时，Start.exe 会将命令转发给沙盒化实例，由其执行挂载；当在沙盒内调用时，则直接执行挂载。

示例：
```cmd
"Start.exe" mount_hive
```

#### run_sbie_ctrl and open_agent[:param]

`run_sbie_ctrl` 与 `open_agent[:param]` 是用于请求 Sandboxie 服务/代理运行 Sandboxie Agent 或执行代理任务的内部服务控制命令。`run_sbie_ctrl` 向服务发送请求以启动 Agent UI。`open_agent:` 可以向代理/服务传递参数。这些主要用于辅助工具和自动化。

示例：
```cmd
"Start.exe" run_sbie_ctrl
"Start.exe" open_agent:SandMan.exe
"Start.exe" open_agent:"SandMan.exe -autorun"
```

* * *

### 相关阅读材料

另请参阅：[注入 DLL](InjectDll.md) 和 [SBIE DLL API](SBIEDLLAPI.md)

转到 [帮助主题](HelpTopics.md)。