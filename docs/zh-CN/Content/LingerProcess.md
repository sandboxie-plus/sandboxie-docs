# 驻留进程

_LingerProcess_ 是 [Sandboxie Ini](SandboxieIni.md) 文件中的一个沙箱设置。它用于指定某些程序的名称，当这些程序成为特定沙箱中最后运行的程序时，会被自动终止。此设置适用于某些程序偶尔会启动 _辅助程序_ 来执行特定任务，而即使原程序已经结束，辅助程序仍然继续运行。例如：

```
   .
   .
   .
   [DefaultBox]
   LingerProcess=jusched.exe
```

_jusched.exe_ 是 Sun Java 框架的一部分。当 Internet Explorer 启动 Java 框架时，偶尔会调用它。此 _LingerProcess_ 示例设置指定，如果 _jusched.exe_ 成为 DefaultBox 沙箱中最后一个运行的程序，则它会被终止。

如果某进程是沙箱中最先启动的进程，驻留进程不会终止该进程。

例如，默认配置中将 Adobe Acrobat Reader 作为 驻留进程，因为一般情况下在通过 Web 浏览器查看 PDF 文件时会启动该程序，而且即使浏览器关闭，该程序仍会继续运行。
```
   LingerProcess=acrord32.exe
```

然而，如果你手动在沙箱中启动 Adobe Acrobat Reader，例如通过沙盘开始菜单运行该程序，则 驻留进程 设置不会对该进程生效。

相关 [沙盘控制](SandboxieControl.md) 设置：[沙箱设置 -> 程序控制 -> 停止行为 -> 驻留进程](ProgramStopSettings.md#lingering-programs)

另见：[程序设置](ProgramSettings.md#linger)。
