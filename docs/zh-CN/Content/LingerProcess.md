# 驻留进程

_LingerProcess_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它指定当这些程序是特定沙盒中仍在运行的最后一个程序时，将被自动终止的程序名称。这在某些程序偶尔启动_辅助程序_来执行特定任务，并且辅助程序在原始程序结束后仍然继续运行的情况下很有用。例如：

```
   .
   .
   .
   [DefaultBox]
   LingerProcess=jusched.exe
```

_jusched.exe_ 是 Sun Java 框架的一部分。它偶尔会在 Internet Explorer 启动 Java 框架时被启动。这个 _LingerProcess_ 示例设置指定，如果 _jusched.exe_ 是 DefaultBox 沙盒中最后一个运行的程序，那么它应该被终止。

如果某个进程是在沙盒中首先启动的进程，LingerProcess 将不会终止该进程。

例如，默认配置包含 Adobe Acrobat Reader 作为 LingerProcess，因为它通常在通过 Web 浏览器查看 PDF 文件时启动，并且在浏览器关闭后仍然继续运行。
```
   LingerProcess=acrord32.exe
```

但是，如果您手动以沙盒化方式启动 Adobe Acrobat Reader，例如从 Sandboxie 开始菜单运行它，那么 LingerProcess 设置将不会应用于该进程。

相关的 [Sandboxie 控制](SandboxieControl.md) 设置：[沙盒设置 -> 程序停止 -> 驻留程序](ProgramStopSettings.md#lingering-programs)

另见：[程序设置](ProgramSettings.md#linger)。 