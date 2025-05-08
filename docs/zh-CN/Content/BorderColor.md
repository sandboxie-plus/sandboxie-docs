# 边框颜色

_BorderColor_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它控制 Sandboxie 是否在属于沙盒化应用程序的活动前台窗口周围显示彩色边框。

用法：

```
   .
   .
   .
   [DefaultBox]
   BorderColor=#00FFFF,ttl,6
   BorderColor=#00FFFF,off,6
   BorderColor=#00FFFF,on,6
```

其默认值为 _"#00FFFF,ttl,6"_。数字表示绘制的边框的默认像素宽度，可以省略。

如果 _BorderColor_ 以 _",off,6"_ 结尾，Sandboxie 将不会绘制边框，而在之前的版本中它是 _",n"_。

颜色使用类似 HTML 的 RGB 颜色表示法指定：

*   井号（#）前缀是一个恰好 6 位长的十六进制（基数为 16）数字。
*   前两个十六进制数字表示颜色的红色分量。
*   接下来的两个十六进制数字表示颜色的绿色分量。
*   最后两个十六进制数字表示颜色的蓝色分量。

当 [Sandboxie 控制器](SandboxieControl.md) 未运行时，将不会绘制边框。

相关 [Sandboxie 控制器](SandboxieControl.md) 设置：[沙盒设置 > 外观](AppearanceSettings.md) 