# Custom Locale/LangID

CustomLCID は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。

```
   .
   .
   .
   [DefaultBox]
   CustomLCID=1033
```

目的の言語/ロケールの [LCID](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-lcid/70feba9f-294e-491e-b6eb-56532684c37f) として 1 つの 10 進数パラメーターを受け入れます。0 に設定すると、システムの既定が使用されます。

関連する Sandboxie Plus 設定: Sandbox Options > Advanced Options > Privacy > Custom Locale/LangID

注: 16 進数の値を 10 進数に変換することで目的の値を特定できます。または[こちら](https://learn.microsoft.com/en-us/openspecs/office_standards/ms-oe376/6c085406-a698-4e12-9d4d-c3b0ee3dbc4a)で見つけることができます。
