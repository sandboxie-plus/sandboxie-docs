# SbieIni 命令行

SbieIni.exe 是一个小巧的命令行工具，用于查询和更新沙盘配置文件 [沙盘配置 (Sandboxie.ini)](SandboxieIni.md)。本页记录了常见的调用形式、自动化示例以及给维护者的实现参考。

## 快速入门

```batch
SbieIni.exe queryex DefaultBox RecoverFolder
SbieIni.exe set DefaultBox RecoverFolder %Desktop%
```

## 概述

SbieIni.exe 支持两种主要的工作流程：

- 查询配置信息（只读）
- 更新配置（`set`、`append`、`insert`、`delete`）

## 调用概要

基本形式：

```batch
SbieIni.exe query    <section> [setting]
SbieIni.exe queryex  [/expand] [/boxes] <section> [setting]

SbieIni.exe set|append|insert|delete [/passwd:********] [/drv] <section> <setting> <value>
```

说明：

- `queryex` 是 `query /expand` 的简写形式
- `/boxes` 仅列出已启用的沙箱
- `/passwd:` 提供配置密码；如果留空，程序将以交互方式提示输入
- `/drv` 通过驱动/服务 API 路由更新；未使用 `/drv` 时，将走 DLL 辅助路径

## 查询配置（只读）

用途：查看各 section 和 setting

列出所有 section 的方法：

```batch
SbieIni.exe query *
```

列出某个 section 下所有 setting 的方法：

```batch
SbieIni.exe query DefaultBox *
```

获取某个 setting 的值方法：

```batch
SbieIni.exe query DefaultBox RecoverFolder
```

展开变量为路径的方法：

```batch
SbieIni.exe queryex DefaultBox RecoverFolder
```

## 更新操作（set / append / insert / delete）

用途：修改配置内容

### Set — 替换某个设置的现有行（若不指定值则移除该设置）

```batch
SbieIni.exe set <section> <setting> <value>
```

### Append — 在已有条目后添加新行

```batch
SbieIni.exe append <section> <setting> <value>
```

### Insert — 在已有条目前添加新行

注意：某些版本中 `insert` 的行为可能与 `append` 类似，如需区分顺序请做实际测试

```batch
SbieIni.exe insert <section> <setting> <value>
```

### Delete — 移除与指定值完全匹配的行

```batch
SbieIni.exe delete <section> <setting> <value>
```

## 高级与自动化说明

- 删除整个沙箱：`SbieIni.exe set BoxName * ""`（会移除该 section 的所有行）。请谨慎使用
- 批处理文件中需将百分号变量转义为 `%%VAR%%`
- 若值中包含空格，需用英文双引号括起来
- 避免在其他进程已打开/锁定 Sandboxie.ini 时进行更新操作
- 若需驱动层级的更新或自动化场景中需要立即同步驱动状态，请使用 `/drv`（此时需保证服务/驱动可用，并且调用者具备必要权限）

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

权威行为见 `apps/ini` 源码。关键实现点如下：

- `apps/ini/cmd.c` — 参数解析辅助
- `apps/ini/query.c` — 查询实现及 SBIEDLL 查询辅助
- `apps/ini/update.c` — 更新相关命令、`/passwd` 密码提示、`/drv` 与 DLL 路径的区别
- `apps/ini/main.c` — 程序入口及用法处理

## 论坛/源码说明

部分用法示例与操作说明参考了社区论坛讨论 [存档](https://sandboxie-website-archive.github.io/www.sandboxie.com/old-forums/viewtopica6bca6bc.html#p126947)