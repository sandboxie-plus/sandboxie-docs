# NT 命名空间隔离

_NtNamespaceIsolation_ 控制 Sandboxie 对作为命名内核对象容器的 NT 目录对象的隔离。默认启用。

该设置关注的是命名对象所使用的目录对象命名空间。它并不是每一种进程间通信（IPC）形式的开关。

## 用法

要对某个沙盒禁用常规的命名空间隔离行为：

```ini
[DefaultBox]
NtNamespaceIsolation=n
```

## 当前行为

启用命名空间隔离时，Sandboxie 会中介涉及 NT 目录对象的操作，包括命名内核对象所使用的目录创建和打开路径。Sandboxie 通常会把这些对象重定向到沙盒命名空间中。

当某个目录的沙盒副本不可用时，SbieDll 的 `NtOpenDirectoryObject` 回退路径可以打开对应的主机目录。启用命名空间隔离时，该回退会把请求的访问权限缩减为查询、遍历和读取控制权限。这可以防止常规的用户态回退在主机目录上获得创建或其他修改权限。

这种行为有助于防止沙盒进程在主机命名空间中创建冲突的名称。Sandboxie Plus 1.8.0 / Classic 5.63.0 的发布说明称此保护提升了安全性并防止了名称抢占。

## 禁用命名空间隔离

`NtNamespaceIsolation=n` 允许对主机 NT 目录对象的访问限制更宽松。这可以改善非常规命名对象命名空间场景的兼容性，但会削弱 Sandboxie 的目录对象虚拟化和名称抢占防护。

禁用此设置不会禁用每一种 IPC 限制或每一种 IPC 隔离形式。IPC 路径规则和其他 Sandboxie 控制项仍然独立存在。

## 备用 IPC 命名

`UseAlternateIpcNaming` 是为应用程序隔离沙盒引入的一种独立的高级命名模式：

```ini
[DefaultBox]
NoSecurityIsolation=y
UseAlternateIpcNaming=y
```

与把 Sandboxie 重定向的命名内核对象放到常规的独立 NT 目录对象命名空间之下不同，Sandboxie 在这种模式下会推导出一个沙盒专用的后缀，并将其附加到重定向的对象名上。在此模式下，由于重定向后的名称使用的是现有命名空间，SbieDll 不会安装其常规的目录对象命名空间钩子。

该设置改变的是 Sandboxie 对重定向的命名内核对象的命名策略。它不会重命名每一个 IPC 协议或每一个 Sandboxie 服务端点。

`UseAlternateIpcNaming` 面向应用程序隔离沙盒。项目警告称，将其与标准隔离沙盒一同使用可能导致驱动阻断访问。它不是 `NtNamespaceIsolation=n` 的别名，尽管备用命名确实避开了常规的独立目录对象命名空间路径。

## 版本历史

| 设置或变更 | 版本 |
| --- | --- |
| NT 目录对象命名空间虚拟化与 `NtNamespaceIsolation` | Sandboxie Plus 1.8.0 / Classic 5.63.0 |
| `UseAlternateIpcNaming` | Sandboxie Plus 1.17.0 / Classic 5.72.0 |

## 相关页面

- [禁用安全隔离](NoSecurityIsolation.md)
- [App Compartment](../PlusContent/compartment-mode.md)
- [Sandboxie Ini](SandboxieIni.md)