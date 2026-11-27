# 崩溃与调试器诊断 {#crash-and-debugger-diagnostics}

Sandboxie 的崩溃转储与调试器等待选项独立于 [Sandboxie 跟踪](SandboxieTrace.md)。小型转储（minidump）设置在符合条件且未处理的崩溃之后创建文件，而调试器等待设置会在 Sandboxie DLL 初始化早期暂停匹配的进程，以便调试器可以附加。

<div id="minidump-crash-diagnostics"></div>

## 小型转储崩溃诊断

### EnableMiniDump

`EnableMiniDump` 是映像感知的，默认禁用：

```ini
EnableMiniDump=y
EnableMiniDump=program.exe,y
```

对于匹配的沙盒化进程，Sandboxie 会安装一个进程内未处理异常转储处理程序，它使用 Windows DbgHelp 的 `MiniDumpWriteDump` 支持。只有到达此顶层未处理异常路径的崩溃才会生成转储。该设置不保证为每种崩溃或终止方式都生成转储，也不会自动覆盖非沙盒化的 SandMan、SbieSvc、SbieDrv 或每一个 Sandboxie 组件。

转储文件会写入沙盒内，位置如下：

```text
<sandbox root>\<image-name>.<unique counter>.dmp
```

后缀是运行时生成的唯一值。发生崩溃的沙盒化进程使用其当前权限写入该文件。

更改 `EnableMiniDump` 之后请重启匹配的进程。`EnableMiniDump` 与 `MiniDumpFlags` 在 Sandboxie Plus 1.0.5 与 Sandboxie Classic 5.55.5 中引入。

### MiniDumpFlags

`MiniDumpFlags` 控制请求的转储类型：

```ini
MiniDumpFlags=Extended
MiniDumpFlags=0xAABBCCDD
```

如果该设置缺失，或包含无法识别的普通文本，Sandboxie 会使用其内置的默认标志。`Extended` 请求全面得多的转储。高级用户可以提供一个十六进制的 Windows `MINIDUMP_TYPE` 位掩码。

扩展或全内存式转储可能很大，并且可能包含敏感内存，包括应用程序数据、文档内容、凭据或进程内驻留的其他机密。分享转储之前请先检查，如果没有故障排查需求，不要将 `Extended` 用作常规默认值。

<div id="waiting-for-a-debugger"></div>

## 等待调试器

### WaitForDebugger

使用 `WaitForDebugger` 按确切的映像名称选择可执行文件：

```ini
WaitForDebugger=program.exe
```

支持多个条目。匹配不区分大小写，且不使用通配符语法。匹配的进程会在 Sandboxie DLL 初始化期间很早就暂停，直到调试器附加。

没有超时。如果没有调试器附加，该进程可能无限期保持暂停。

### WaitForDebuggerAll

```ini
WaitForDebuggerAll=y
```

这会让每个受影响的沙盒化进程都等待调试器。它默认禁用，只应在有意的开发者或故障排查工作中使用：意外启用可能使沙盒化应用程序无法正常启动。

### WaitForDebuggerCmdLine

```ini
WaitForDebuggerCmdLine=some argument
```

支持多个条目。每个条目都作为进程命令行的不区分大小写子串进行匹配。尽管历史元数据把该值描述为模式，它并不实现通配符或正则表达式语法。

`WaitForDebugger`、`WaitForDebuggerAll` 与 `WaitForDebuggerCmdLine` 是互相替代的选择器。其中任意一个匹配都可能触发等待。

### WaitForDebuggerSilent

调试器附加之后，当前行为取决于 `WaitForDebuggerSilent`：

* 启用静默模式时，进程会继续运行，Sandboxie 不会特意引发断点。
* 禁用静默模式时，Sandboxie 会引发调试断点，使已附加的调试器停在那里。

如果 `WaitForDebuggerSilent` 缺失，当前运行时会采用静默继续。要在附加后请求断点，请配置：

```ini
WaitForDebuggerSilent=n
```

SandMan 没有 **恢复** 操作。附加调试器即解除初始等待；使用断点模式时，请从调试器继续执行。

<div id="sandman-configuration"></div>

## SandMan 配置

SandMan 的 **沙盒选项 > 高级选项 > 调试 > 调试选项** 通用设置编辑器至少公开 `EnableMiniDump` 与 `WaitForDebugger`。它不为 `MiniDumpFlags`、`WaitForDebuggerAll`、`WaitForDebuggerCmdLine` 或 `WaitForDebuggerSilent` 提供专用复选框。

未发现这些选项在 Sandboxie Control Classic 中有对应的专用设置面板。兼容的手动 INI 设置由共享运行库读取。

<div id="applying-changes"></div>

## 应用更改

这些选项在进程初始化期间求值。更改之后请重启匹配的沙盒化进程；重新创建受影响的沙盒进程树是最可靠的做法。通常不需要重启 SandMan、服务或驱动程序。

<div id="related-pages"></div>

## 相关页面

* [如何使用 WinDbg](HowToUseWinDbg.md)
* [Sandboxie 跟踪](SandboxieTrace.md)
* [Sandboxie Ini](SandboxieIni.md)
