# 阻止网络文件访问

`BlockNetworkFiles` 是 [Sandboxie Ini](SandboxieIni.md) 文件中的一个沙箱设置项。它指定了 Sandboxie 是否会阻止沙箱内程序在未被明确允许的情况下访问网络文件和文件夹。

```
   .
   .
   .
   [DefaultBox]
   BlockNetworkFiles=n
```

指定为 _n_ 表示沙箱内的程序可以在未被明确允许的情况下访问网络文件，此时沙箱状态中会出现 "网络分享"。

相关 Sandboxie Plus 设置路径：沙箱选项 > 网络选项 > 其他选项 > 阻止网络文件和文件夹，除非已被明确打开

在创建新沙箱并选择 "配置高级选项" 时的相关设置：沙箱隔离选项 > 网络访问 > 允许访问网络文件和文件夹
