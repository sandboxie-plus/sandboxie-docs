# RunCommand

`RunCommand` 会在 SandMan 中为沙盒的 **运行** 菜单添加自定义条目。选中某个条目会在该沙盒中启动它配置的命令。定义条目并不会在沙盒启动时或沙盒的其他事件中自动启动程序。

这是 SandMan 的菜单功能，而不是由驱动程序强制实施的执行规则。当前的 Sandboxie Control Classic 代码没有提供对应的自定义运行菜单使用方。

<div id="configuration-formats"></div>

## 配置格式

每一行 `RunCommand` 定义菜单中的一个条目。简单格式用第一个 `|` 把显示名称与命令行分隔开：

```ini
[DefaultBox]
RunCommand=Notepad|"C:\Windows\notepad.exe"
RunCommand=Config\Open win.ini|"C:\Windows\notepad.exe" "C:\Windows\win.ini"
```

命令可以包含参数。包含空格的路径请加引号，参数请按被启动程序的要求加引号。SandMan 会把命令行传给其常规的沙盒启动器；`RunCommand` 不提供独立的 shell 命令解析器。

名称中的反斜杠会创建菜单层级。例如 `Config\Open win.ini` 会出现在 **运行 > Config** 下。多级可以用 `Tools\Editors\Notepad` 这样的写法。

旧式格式还允许在名称部分的第一个逗号之后给出可选图标：`Name,icon|command`。由于第一个逗号和第一个 `|` 都是分隔符，菜单名称需要包含这些字符时请改用 JSON。

需要指定图标或工作目录时，请使用带有 `Command`、`Name`、可选 `Icon` 和可选 `WorkingDir` 字段的 JSON 值：

```ini
RunCommand={"Command":"\"C:\\Windows\\notepad.exe\" \"C:\\Windows\\win.ini\"","Name":"Config\\Open win.ini","Icon":"C:\\Windows\\System32\\notepad.exe,0","WorkingDir":"C:\\Windows"}
```

JSON 要求按示例转义反斜杠和嵌入的引号。当既未设置图标也未设置工作目录时，SandMan 的编辑器写入紧凑的旧式格式；否则写入 JSON。序列化条目时，它会移除 `WorkingDir` 中的双引号。

`Icon` 可以用 `path,index` 指定图标文件与索引，也可以只给索引以配合命令的可执行文件使用。未指定显式图标时，SandMan 会尝试使用命令可执行文件的图标。如果指定的图标无法加载，则使用回退图标。特殊索引 `-1` 会选择 SandMan 的 Internet 图标。

<div id="working-directory-and-sandbox-paths"></div>

## 工作目录与沙盒路径

`WorkingDir` 是可选的。指定后，SandMan 会把它作为 `Start.exe` 启动器的工作目录传入；为空时，SandMan 不为该次启动设置工作目录。请使用适合所启动程序的路径。

SandMan 能识别命令与工作目录字符串中的 `%BoxRoot%`，并在启动前把它替换为该沙盒的文件根路径。固定程序时可能会创建这样的路径。请不要把这种替换当作通用的环境变量展开。

<div id="global-sandbox-and-template-entries"></div>

## 全局、沙盒与模板条目

条目可以放在 `[GlobalSettings]` 中以适用于所有沙盒，也可以放在单个沙盒的节中。适用的模板也可以提供条目。SandMan 构建某个沙盒的运行菜单时，会同时请求本地值、模板值和全局值。这些条目是合并的，而不是当作一个覆盖性取值：添加某个沙盒专属的条目不会替换同名的全局条目，因此可能出现重复的菜单动作。

沙盒的 **运行菜单** 编辑器只显示它自己的条目，而不是来自全局设置与模板的完整有效列表。全局编辑器单独管理全局条目。由于有效列表可能合并来自沙盒、适用模板和全局设置的条目，请不要把不同配置来源的条目之间的相对顺序当作稳定的菜单顺序。

<div id="sandman-interface"></div>

## SandMan 界面

对单个沙盒，请打开 **沙盒选项 > 常规选项 > 运行菜单**。编辑器列出 **名称** 与 **命令行**，并提供添加程序或命令、移除条目、上移或下移的控件。**添加程序** 还提供 **浏览程序**。

对适用于所有沙盒的条目，请打开 **选项 > 全局设置 > 常规选项 > 运行菜单**。这是用于 `[GlobalSettings]` 条目的独立编辑器。

你也可以使用正在运行的沙盒化进程的 **预设 > 固定到运行菜单** 操作。SandMan 会把它的可执行文件与工作目录记录到一个沙盒本地条目中。显示在沙盒 **从开始菜单运行** 子菜单下的快捷方式同样可以被固定，并在可用时保留其命令、参数、图标和工作目录。该子菜单表示沙盒内的开始菜单项，而不是宿主 Windows 的开始菜单。

运行菜单项也可以用来创建桌面快捷方式。`RunCommand` 值本身并不是 Windows `.lnk` 文件。

<div id="execution-and-changes"></div>

## 执行与更改

选中自定义条目时，SandMan 会展开其命令与工作目录中的 `%BoxRoot%`，然后用所选沙盒和默认启动标志调用其常规的 `RunStart` 路径。该路径会为该沙盒调用 `Start.exe`。`RunCommand` 不会请求提升权限，也不会绕过该沙盒的常规限制。

SandMan 在更新所选沙盒的菜单时，会依据配置重新构建运行菜单。保存更改后，如有必要请重新打开菜单；现有的沙盒化进程无需重启。如果你在 SandMan 之外编辑了 `Sandboxie.ini`，请先重新加载配置。

`RunCommand` 与 `StartCommand`、`StartSystemBox` 这类自动启动设置不同，也与宿主侧的 [SandMan triggers](SandManTriggers.md)（如 `OnBoxDelete` 或 `OnBoxTerminate`）不同。另一个独立的 `CSbieUtils::RunCommand()` 辅助函数执行其他 SandMan 命令，并不是 `RunCommand=` 菜单条目的使用方。

<div id="version-history"></div>

## 版本历史

更新日志在 Sandboxie Plus 0.5.0 / Classic 5.45.0 这一对版本中记录了按沙盒自定义的运行菜单命令与进程固定功能。这确立的是 SandMan 界面上的里程碑，而不是 `RunCommand` 设置的原始引入日期——该设置当前的元数据中没有 `AddedVersion`。

之后的里程碑包括 1.6.1 / 5.61.1 的全局运行菜单条目、1.8.0 / 5.63.0 的菜单文件夹，以及 1.9.0 / 5.64.0 的自定义图标。后续版本修复了运行菜单条目的工作目录处理。

<div id="related-pages"></div>

## 相关页面

- [Sandboxie Ini](SandboxieIni.md)
- [启动命令行](StartCommandLine.md)
- [启动系统沙盒](StartSystemBox.md)
- [SandMan Triggers](SandManTriggers.md)
