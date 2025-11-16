# SbieIni 命令行

SbieIni.exe 是一个用于查询和更新 Sandboxie 配置文件 Sandboxie.ini 的小型命令行实用程序， [Sandboxie.ini](SandboxieIni.md). 本页面记录了常见的调用格式、自动化示例以及供维护者参考的实现细节。

## 快速入门

```batch
SbieIni.exe queryex DefaultBox RecoverFolder
SbieIni.exe set DefaultBox RecoverFolder %Desktop%
```

## 概述

SbieIni.exe 支持两种主要的工作流程：

- 查询配置值 （只读）
- 更新配置 (`set`, `append`, `insert`, `delete`)

## 调用摘要

基本格式：

```batch
SbieIni.exe query    <section> [setting]
SbieIni.exe queryex  [/expand] [/boxes] <section> [setting]

SbieIni.exe set|append|insert|delete [/passwd:********] [/drv] <section> <setting> <value>
```

注意：

- `queryex` 是 `query /expand` 的简写。
- `/boxes` 仅列出已启用的沙盒。
- `/passwd:` 提供配置密码；如果留空，该工具将以交互方式提示输入。
- `/drv` 通过驱动/服务 API 路由更新；; 若不带 `/drv` 则使用 DLL 助手路径。

## 查询配置 (只读)

目的：检查配置节和设置项。

如何列出所有配置节：

```batch
SbieIni.exe query *
```

如何列出特定配置节中的所有设置项：

```batch
SbieIni.exe query DefaultBox *
```

如何获取某个设置的一个或多个值：

```batch
SbieIni.exe query DefaultBox RecoverFolder
```

如何将变量展开为完整路径：

```batch
SbieIni.exe queryex DefaultBox RecoverFolder
```

## 更新操作 (set / append / insert / delete)

目的：修改配置内容。

### Set — 替换某个设置的所有现有行 (如果未提供值，则删除它们)

```batch
SbieIni.exe set <section> <setting> <value>
```

### Append — 在现有条目之后添加一个新的值

```batch
SbieIni.exe append <section> <setting> <value>
```

### Insert —  在现有条目之前添加一个新的值

注意： 在某些构建版本中 `insert` 的行为可能与 `append`相同； 如果顺序很重要，请进行测试。

```batch
SbieIni.exe insert <section> <setting> <value>
```

### Delete — 删除与提供的值完全匹配的行

```batch
SbieIni.exe delete <section> <setting> <value>
```

## 高级用法和自动化说明

- 要删除整个沙盒： `SbieIni.exe set BoxName * ""` （此命令会移除该配置节下的所有行），请务必谨慎操作
- 批处理文件： 请使用 `%%VAR%%` 的形式转义百分号变量。
- 如果值包含空格，请用双引号将其括起来。
- 避免在 `Sandboxie.ini` 文件被其他进程打开或锁定时运行更新操作。
- 对于需要立即更新驱动程序状态的驱动级更新或自动化场景，请使用 `/drv` (服务/驱动程序必须可用，且调用者需要有必要的权限)。

## 示例

```batch
SbieIni.exe query * | sort > Sections.txt
SbieIni.exe query DefaultBox RecoverFolder
SbieIni.exe queryex DefaultBox RecoverFolder
SbieIni.exe append DefaultBox Template RoboForm
SbieIni.exe set DefaultBox AutoRecover n
SbieIni.exe delete DefaultBox RecoverFolder "C:\Old\Path"
```

## 实现与参考

该工具的**权威性行为**定义在 `apps/ini` 的源代码中。关键的实现点如下：

- `apps/ini/cmd.c` — 参数解析助手。
- `apps/ini/query.c` — 查询功能的实现和 SBIEDLL 查询助手。
- `apps/ini/update.c` — 更新命令， `/passwd` 提示以及 `/drv` 与 DLL 路径的选择。
- `apps/ini/main.c` — 程序入口和用法处理。

## 论坛/来源说明

一些用法示例和操作说明参考了社区论坛的讨论 [存档](https://sandboxie-website-archive.github.io/www.sandboxie.com/old-forums/viewtopica6bca6bc.html#p126947).
