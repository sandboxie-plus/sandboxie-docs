# 自定义区域设置/语言 ID

CustomLCID 是 [沙盘配置文件（Sandboxie.Ini）](SandboxieIni.md) 中的一个设置。
```
   .
   .
   .
   [DefaultBox]
   CustomLCID=1033
```
它接受一个十进制参数，作为所需语言/区域设置的 [LCID](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-lcid/70feba9f-294e-491e-b6eb-56532684c37f)。如果设置为 0，则将使用系统默认值。

相关的沙盘增强版（Sandboxie Plus）设置：沙箱选项 > 高级选项 > 隐私 > 自定义区域设置/语言 ID

注意：您可以通过将十六进制值转换为十进制来确定所需的值，也可以在 [此处](https://learn.microsoft.com/en-us/openspecs/office_standards/ms-oe376/6c085406-a698-4e12-9d4d-c3b0ee3dbc4a) 找到这些值。
