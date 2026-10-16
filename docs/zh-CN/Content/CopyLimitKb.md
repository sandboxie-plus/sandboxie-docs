# 复制限制 Kb

_CopyLimitKb_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，用于在需要将已有宿主机文件的内容复制到沙盒时，按文件大小判断是否迁移。限制以千字节为单位指定（1 千字节 = 1024 字节）。

更多信息参见 [SBIE2102](SBIE2102.md)。

用法：

```
   .
   .
   .
   [DefaultBox]
   CopyLimitKb=128000
```

此示例将 _DefaultBox_ 的阈值设为 128000 KiB，即 125 MiB。没有优先适用的迁移规则时，文件大小严格小于该阈值会选择完整内容迁移；文件大小恰好等于或大于阈值时，则进入大文件提示或不复制处理流程。

使用 `CopyLimitKb=-1` 可取消常规大小限制。否则，应设置合理的正整数值。

## 迁移判断

大小判断前，会按 [DontCopy](DontCopy.md)、[CopyAlways](CopyAlways.md)、[CopyEmpty](CopyEmpty.md) 的优先级依次检查匹配规则。若均未匹配，且文件达到或超过已启用的大小阈值，[PromptForFileMigration](PromptForFileMigration.md) 可让 SandMan 询问用户是否迁移。用户同意后，此次会尝试迁移完整内容，但不保证能够读取源文件或完成复制。

未获准迁移时，[CopyBlockDenyWrite](CopyBlockDenyWrite.md) 控制此次依赖初次迁移的文件打开操作：设为 `y` 时拒绝打开；否则移除写入和删除权限后重试访问宿主机文件。其余请求参数或宿主机权限仍可能导致重试失败。

此阈值不控制所有文件访问。新建文件、正常访问已有沙盒副本、通过 [OpenFilePath](OpenFilePath.md) 直接访问，以及不复制宿主机文件内容的操作，均采用其他处理路径。[CopyNewer](CopyNewer.md) 可以触发已有沙盒副本的刷新；该次迁移可能使用此大小判断。

## 生效值与界面默认值

运行时初始化采用的默认值为 `-1`：没有生效的配置值时，不启用常规大小限制。生效值可来自沙盒本身、适用且已启用的模板，或 `[GlobalSettings]` 中的默认设置。直接为某个沙盒设置值，不会改变其他沙盒的设置值。

两个界面的默认显示值不同：

- **SandMan**：从沙盒的直接设置读取，缺省显示 81920 KiB（80 MiB）。启用大小限制时，如果输入框的值为 `81920`，保存会删除沙盒中直接设置的 `CopyLimitKb` 条目，而不是写入该数值。此后，适用的继承配置或运行时默认值 `-1` 可能生效。未勾选大小限制复选框时，会写入 `-1`。
- **Sandboxie Control Classic**：49152 KiB（48 MiB），是其文件迁移界面和配置读取函数使用的默认值，并非当前运行时的默认值。

这两个界面的默认显示值都不代表 Sandboxie 有一个统一的大小限制。大小限制和警报消息可以在 [沙盒设置 > 文件迁移](FileMigrationSettings.md) 中配置。

## 使更改生效

此限制在沙盒进程初始化文件子系统时缓存。修改后，应重新启动相关沙盒进程；仅重新加载配置不会替换已初始化进程中缓存的限制值。

相关 [Sandboxie Ini](SandboxieIni.md) 设置项：[复制限制静默](CopyLimitSilent.md)
