# Custom Locale/LangID

CustomLCID is a sandbox setting in [Sandboxie Ini](SandboxieIni.md).

```
   .
   .
   .
   [DefaultBox]
   CustomLCID=1033
```

It accepts one Decimal parameter as the [LCID](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-lcid/70feba9f-294e-491e-b6eb-56532684c37f) of the language/locale desired. If set to 0, system default will be used.

Related Sandboxie Plus setting: Sandbox Options > Advanced Options > Privacy > Custom Locale/LangID

Note: You may determine the desired value by converting the Hexadecimal values to Decimal, or you may find them [there](https://learn.microsoft.com/en-us/openspecs/office_standards/ms-oe376/6c085406-a698-4e12-9d4d-c3b0ee3dbc4a).
