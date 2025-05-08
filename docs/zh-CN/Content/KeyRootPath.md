# 注册表根路径

_KeyRootPath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它指定特定沙盒的注册表配置单元挂载的注册表位置。

与所有沙盒设置一样，它也可以在全局部分中指定，在这种情况下，它将适用于所有未在沙盒部分中指定此设置的沙盒。

有关更多信息，请参见[沙盒层次结构](SandboxHierarchy.md)。

用法：
```
   .
   .
   .
   [DefaultBox]
   KeyRootPath=\REGISTRY\USER\%BOXNAME%
```

以下替换变量在此路径中可能有用：

* 变量 %SANDBOX% 展开为沙盒名称
* 变量 %USER% 展开为用户名
* 变量 %SID% 展开为用户安全标识符（SID）
* 变量 %SESSION% 展开为终端服务会话号

如果未指定 KeyRootPath，其默认值为：

* _\REGISTRY\USER\Sandbox_%USER%_%SANDBOX%_

该值必须以前缀 **\REGISTRY\USER\** 开头，否则 Sandboxie 将无法挂载注册表配置单元。

可能没有理由更改此设置的默认值，也不建议这样做。

如果 Sandboxie 无法成功挂载或卸载沙盒化的注册表配置单元，它将分别发出消息 [SBIE1241](SBIE1241.md) 和 [SBIE2208](SBIE2208.md)。 