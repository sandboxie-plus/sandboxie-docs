# 阻止网络文件

BlockNetworkFiles 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它指定 Sandboxie 是否阻止沙盒化程序访问未特别打开的网络文件和文件夹。

```
   .
   .
   .
   [DefaultBox]
   BlockNetworkFiles=n
```

指定 _n_ 表示允许沙盒化程序访问未特别打开的网络文件，在这种情况下，沙盒状态中将显示"网络共享"。

相关 Sandboxie Plus 设置：沙盒选项 > 网络选项 > 其他选项 > 阻止网络文件和文件夹，除非特别打开

创建新沙盒时选择"配置高级选项"时的相关 Sandboxie Plus 设置：沙盒隔离选项 > 网络访问 > 允许访问网络文件和文件夹 