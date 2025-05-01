# 边框颜色

_BorderColor_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙箱设置。它用于控制 Sandboxie 是否在活动前台窗口（如果该窗口属于沙箱化应用程序）周围显示彩色边框。

用法示例：

```
   .
   .
   .
   [DefaultBox]
   BorderColor=#00FFFF,ttl,6
   BorderColor=#00FFFF,off,6
   BorderColor=#00FFFF,on,6
```
其默认值为 _"#00FFFF,ttl,6"_。数字代表绘制边框的默认像素宽度，可省略。

如果 _BorderColor_ 以 _",off,6"_ 结尾，则 Sandboxie 不会绘制边框，而早期版本中是 _",n"_。

颜色采用类似 HTML 的 RGB 颜色表示法：

*   #号后跟一个长度为 6 的十六进制（基数为 16）数字；
*   前两位十六进制数字表示颜色的红色分量；
*   中间两位十六进制数字表示颜色的绿色分量；
*   最后两位十六进制数字表示颜色的蓝色分量。

当 [沙箱控制](SandboxieControl.md) 未运行时，边框不会被绘制。

相关的 [沙箱控制](SandboxieControl.md) 设置：[沙箱设置 > 外观](AppearanceSettings.md)
