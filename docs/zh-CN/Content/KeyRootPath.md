# 注册表根路径

_KeyRootPath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定特定沙盒的注册表配置单元被挂载的注册表位置。

与所有沙盒设置一样，它也可以出现在全局节中，此时它适用于所有未在沙盒节中另行指定该设置的沙盒。

更多信息参见 [沙盒层级](SandboxHierarchy.md)。

用法：
```
   .
   .
   .
   [DefaultBox]
   KeyRootPath=\REGISTRY\USER\%BOXNAME%
```

以下替换变量在此路径中可能有用。

*   变量 %SANDBOX%，展开为沙盒名称
*   变量 %USER%，展开为用户名称
*   变量 %SID%，展开为用户安全 ID（SID）
*   变量 %SESSION%，展开为终端服务会话编号

如果未指定注册表根路径，其默认值为：

*   _\REGISTRY\USER\Sandbox_%USER%_%SANDBOX%_

该值必须以前缀 **\REGISTRY\USER\** 开头，否则 Sandboxie 将无法挂载注册表配置单元。

可能没有理由更改此设置的默认值，也不建议这样做。

如果 Sandboxie 无法成功挂载或卸载沙盒化注册表配置单元，它将分别发出消息 [SBIE1241](SBIE1241.md) 和 [SBIE2208](SBIE2208.md)。
