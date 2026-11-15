# Allow Raw Disk Read

_AllowRawDiskRead_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、v0.7.0 / 5.48.0 以降で利用できます。この設定は、昇格されたサンドボックス化されたプロセスが読み取りのためにボリューム/ディスクにアクセスするのを防ぐ保護を無効にするために使用できます。

```
   .
   .
   .
   [DefaultBox]
   AllowRawDiskRead=y
```

関連する Sandboxie Plus 設定: Sandbox Options > File Options > Allow elevated sandboxed applications to read the harddrive
