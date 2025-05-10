# 注册表根路径

_KeyRootPath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙箱设置。它用于指定某个沙箱的注册表配置单元挂载的位置。

和所有沙箱设置一样，它也可以在全局部分指定，此时对于所有未在沙箱部分单独指定该设置的沙箱均适用。

更多信息请参见 [沙箱层级结构](SandboxHierarchy.md)。

用法示例：
```
   .
   .
   .
   [DefaultBox]
   KeyRootPath=\REGISTRY\USER\%BOXNAME%
```

在此路径中，以下替换变量可能会用到：

*   变量 %SANDBOX%，其值为沙箱名称
*   变量 %USER%，其值为用户名
*   变量 %SID%，其值为用户安全标识（SID）
*   变量 %SESSION%，其值为终端服务的会话编号

如果未指定 注册表根路径，则其默认值为：

*   _\REGISTRY\USER\Sandbox_%USER%_%SANDBOX%_

该值必须以 **\REGISTRY\USER\** 为前缀，否则沙盒将无法挂载注册表配置单元。

通常没有理由修改该设置的默认值，并且不建议这样做。

如果沙盒无法成功挂载或卸载沙箱注册表配置单元，分别会发出消息 [SBIE1241](SBIE1241.md) 和 [SBIE2208](SBIE2208.md)。