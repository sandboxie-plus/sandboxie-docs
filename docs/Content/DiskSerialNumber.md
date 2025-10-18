# Disk Serial Number

_DiskSerialNumber_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v1.15.2 / 5.70.2. This setting allows assigning custom serial numbers to specific disk devices within sandboxes, working in conjunction with [Hide Disk Serial Number](HideDiskSerialNumber.md).

## Syntax

```ini
DiskSerialNumber=<DeviceName>,<SerialNumber>
```

* **DeviceName**: Windows device name (e.g., HarddiskVolume1, HarddiskVolume2)
* **SerialNumber**: Custom serial number in hexadecimal format (with or without hyphens)

## Example Usage

```ini
[DefaultBox]

HideDiskSerialNumber=y
DiskSerialNumber=HarddiskVolume1,1234-ABCD
DiskSerialNumber=HarddiskVolume2,5678-EFGH
DiskSerialNumber=HarddiskVolume3,9ABC-DEF0
```

## Prerequisites

- Requires `HideDiskSerialNumber=y` to be enabled in the same sandbox[^1].
- Without this prerequisite, the DiskSerialNumber settings are ignored.

## Serial Number Formats

### Supported Formats

- **Hyphenated**: `1234-ABCD`, `AA-BB-CC-DD`.
- **Plain**: `1234ABCD`, `AABBCCDD`.
- **Mixed**: Any combination of hex digits with optional hyphens.

### Valid Examples

```ini
DiskSerialNumber=HarddiskVolume1,1234ABCD
DiskSerialNumber=HarddiskVolume2,12-34-AB-CD
DiskSerialNumber=HarddiskVolume3,12345678
DiskSerialNumber=HarddiskVolume4,DEADBEEF
```

### Invalid Formats

- Non-hexadecimal characters (G-Z).
- Odd number of hex digits.
- Empty strings.
- Special characters other than hyphens.

## Device Name Discovery

### Method 1: Using WMIC Command

Run in Command Prompt to list available disk volumes:

```cmd
wmic logicaldisk get caption,volumeserialnumber,deviceid
```

### Method 2: Using Disk Management

1. Open **Disk Management** (`diskmgmt.msc`).
2. Right-click on volumes to see properties.
3. Note the volume labels and drive letters.

### Method 3: Registry Inspection

Check registry key: `HKEY_LOCAL_MACHINE\SYSTEM\MountedDevices`

### Method 4: Testing with Random Values

1. Set test configurations:

```ini
DiskSerialNumber=HarddiskVolume1,11111111
DiskSerialNumber=HarddiskVolume2,22222222
DiskSerialNumber=HarddiskVolume3,33333333
```

2. Run `vol C:`, `vol D:`, etc., in the sandbox to identify which device corresponds to which drive.

## Technical Implementation

### Device Path Resolution

- Sandboxie extracts device names from Windows NT paths with `\Device\` prefix[^2].
- Device name parsing stops at the next backslash or string terminator[^3].
- Failed device extraction results in random serial number generation[^4].

### Hexadecimal Processing

- Custom parser handles both hyphenated and plain hex formats[^5].
- Invalid hex strings trigger fallback to random generation[^6].
- Byte order is automatically swapped to match Windows DWORD format[^7].

### Caching Mechanism

- Serial numbers are cached per session for performance[^8]
- Thread-safe implementation using critical sections[^9]
- Cache keys are based on original hardware serial numbers[^10]

## Use Cases

### Application Testing

- Test software behavior with specific disk serial number patterns.
- Simulate different hardware configurations.
- Debug serial number-dependent functionality.

### Privacy Enhancement

- Replace real hardware identifiers with known values.
- Create consistent sandbox fingerprints.
- Prevent hardware-based tracking.

## Troubleshooting

### Common Issues

**Setting Not Applied**

- Ensure `HideDiskSerialNumber=y` is enabled.
- Verify correct device name format.
- Check hexadecimal string validity.

**Wrong Device Targeted**

- Use device discovery methods to identify correct names.
- Test with unique serial numbers to verify mapping.

**Random Values Still Returned**

- Invalid hex format triggers random fallback.
- Device name mismatch results in random generation.
- Missing `HideDiskSerialNumber` prerequisite.

## Related Settings

- [Hide Disk Serial Number](HideDiskSerialNumber.md) - Required prerequisite setting.
- [Hide Firmware Info](HideFirmwareInfo.md) - Hides additional hardware identifiers.
- [Hide Network Adapter MAC](HideNetworkAdapterMAC.md) - Customizes network adapter identifiers.
- [Random Registry UID](RandomRegUID.md) - Randomizes registry-based unique identifiers.

## Configuration Availability

- **INI Configuration**: Available
- **Plus UI**: Not available (INI-only setting)
- **Classic UI**: Not available


[^1]: **Prerequisite Check**: The `HideDiskSerialNumber` setting must be enabled for device-specific serial number mapping to function (kernel.c).

[^2]: **Device Path Parsing**: Sandboxie searches for `\Device\` prefix in NT path strings to extract device names (kernel.c).

[^3]: **Name Extraction Logic**: Device name parsing terminates at the first backslash or null character after the `\Device\` prefix (kernel.c).

[^4]: **Fallback Behavior**: Empty device names trigger `Dll_rand()` for random serial number generation (kernel.c).

[^5]: **Hex Parser Implementation**: `hex_string_to_uint8_array()` function processes hex strings while skipping hyphen characters (custom.c).

[^6]: **Error Handling**: Invalid hex characters, odd digit counts, or parsing failures return FALSE, triggering random generation (custom.c).

[^7]: **Endianness Conversion**: Byte swapping is performed when `swap_bytes=TRUE` to match Windows little-endian DWORD format (custom.c).

[^8]: **Session Persistence**: `map_insert()` stores computed serial numbers using original hardware values as keys (kernel.c).

[^9]: **Thread Safety**: Critical section `Kernel_DiskSN_CritSec` protects concurrent access to the serial number cache (kernel.c5).

[^10]: **Cache Key Strategy**: Original disk serial numbers serve as map keys for consistent per-session value retrieval (kernel.c).