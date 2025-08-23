# Import Box

**ImportBox** is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It allows users to load sandbox configurations from external INI files.

## Syntax

```ini
ImportBox=<Path to INI file>
```

* **Path to INI file**: The full path to an external INI file containing sandbox configuration settings.

## Purpose

ImportBox enables the creation of portable sandbox configurations by loading sandboxes from external INI files rather than storing everything in the main Sandboxie.ini file.

## Example Usage

### Basic Import

To import sandbox settings from an external file:

```ini
[GlobalSettings]
ImportBox=C:\Sandboxes\PortableSandbox.ini
```

### Multiple Imports

You can import as many sandboxes as you want:

```ini
[GlobalSettings]
ImportBox=C:\Sandboxes\SecureSandbox.ini
ImportBox=C:\Sandboxes\NoNetworkSandbox.ini
ImportBox=C:\Sandboxes\BrowserSandbox.ini
```

### Portable Configuration Example

Create a portable configuration file anywhere, for example `C:\Sandboxes\BrowserBox.ini`:

```ini
[BrowserBox]
Enabled=y
```

> **Important:**  
> When importing a sandbox from an external INI file, the file must contain exactly one section, and that section’s name must match the filename (without the `.ini` extension).  
> If there are additional sections, or if the section name does not match the filename, the import will fail.

Then import it into Sandboxie:

```ini
[GlobalSettings]
ImportBox=C:\Sandboxes\BrowserBox.ini
```

### Import Entire Sandbox Root Directory

Instead of manually importing each specific sandbox, You can import all sandbox configurations in a directory using a wildcard:

```ini
[GlobalSettings]
ImportBox=C:\Sandboxes\*
```

This imports all `.ini` files in the specified directory, making any sandboxes in that folder available for use. 

## User Interface

In **Sandboxie Plus**, you can manage ImportBox settings through:

**Global Settings** > **Advanced Config** > **Sandboxie.ini**

This interface lets you create new portable sandboxes, import existing sandbox files, or add directories as a sandbox root to automatically import sandboxes in those directories.

![ImportBox Configuration](../Media/ImportBox.png)



