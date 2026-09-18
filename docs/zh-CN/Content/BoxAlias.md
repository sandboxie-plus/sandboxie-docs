# 沙盒别名

**沙盒别名** 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 **v1.14.6** 起可用。它允许为沙盒设置备选显示名称。

## 语法

```ini
BoxAlias=显示名称
```

## 用法

沙盒别名提供了一种方法，为包含特殊字符的沙盒设置自定义显示名称，这些字符对沙盒名称而言本来是无效的。设置沙盒别名时，它覆盖默认的显示行为：

```ini
[MyTestBox]
BoxAlias=Development & Testing

[WebBox]  
BoxAlias=Secure Web Browser v2.0

[WorkSandbox]
BoxAlias=Email Client*
```

## 重要说明

- 沙盒别名只影响显示名称——INI 文件中的实际沙盒名称保持不变
- 如果未设置沙盒别名，沙盒名称显示时下划线会被替换为空格

## 用户界面

沙盒别名可以通过 **Sandboxie Plus** 中的**重命名**功能配置。把沙盒重命名为包含特殊字符的名称时，Sandboxie Plus 会自动提示将其设置为别名，而不是重命名沙盒。
