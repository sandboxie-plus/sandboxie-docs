# 沙箱别名

**BoxAlias** 是 [Sandboxie Ini](SandboxieIni.md) 自 **v1.14.6** 版本以来可用的沙箱设置。它允许为沙箱设置额外的显示名称。

## 语法

```ini
BoxAlias=显示名称
```

## 用法

特殊字符在沙箱名称中是无效的，而 BoxAlias 提供了一种为包含特殊字符的沙箱设置自定义显示名称的方法。当设置 BoxAlias 时，它会覆盖默认的显示行为：

```ini
[MyTestBox]
BoxAlias=Development & Testing

[WebBox]  
BoxAlias=Secure Web Browser v2.0

[WorkSandbox]
BoxAlias=Email Client*
```

## 重要说明

- BoxAlias 仅影响显示名称 - INI 文件中的实际沙箱名称保持不变
- 如果未设置 BoxAlias，沙箱名称显示时将用下划线替代空格

## 用户界面

BoxAlias 可以通过 **Sandboxie Plus** 中的 **重命名** 功能进行配置。当将沙箱重命名为包含特殊字符的名称时，Sandboxie Plus 会自动提示将其设置为别名，而不是重命名沙箱。