# Running Games in Sandboxie

This page collects practical guidance for running games — and several instances of the same game — in Sandboxie Plus. It complements [Application Compartment](../PlusContent/compartment-mode.md) with a game-oriented decision path; the isolation model itself is documented there.

## When a game needs a relaxed box

Most games run fine in a standard sandbox. A game typically needs a more relaxed configuration when its launcher or engine interacts badly with Sandboxie's isolation mechanisms. The usual symptoms are:

- **The launcher starts but the game never gets past loading.** The launcher may hit an internal watchdog timeout (for example, the game has a "launcher did not respond" dialog) while the engine is still initializing.
- **Startup is dramatically slower inside the sandbox than outside it**, sometimes to the point of the watchdog giving up.
- **The game runs, but only after a very long first launch** and is fine on subsequent starts (copy-on-write migration already done).

These symptoms point to the game's own protection or anti-cheat layer reacting to Sandboxie's API hooks: it can slow initialization down to the point where the launcher's own timeout fires. On some systems this appears only after a Windows upgrade, because newer Windows builds change the interception paths the hooks rely on.

!!! tip

    Before changing sandbox settings, make sure Sandboxie Plus itself is reasonably current: newer versions carry the kernel data (DynData) needed on recent Windows builds, and an outdated driver on a new Windows build can itself break or slow sandboxed applications. Check the [CHANGELOG](https://github.com/sandboxie-plus/Sandboxie/blob/master/CHANGELOG.md) for "updated DynData" entries.

## Trying the standard sandbox first

A standard sandbox gives you the strongest isolation and is the right default. It is worth diagnosing a slow game once in a standard box before relaxing anything, because it can reveal a genuinely missing access rule rather than a hook conflict. When the program starts successfully in a standard box, a trace of its accesses (see [Trace Log](../PlusContent/TraceLog.md)) can be compared against a relaxed box to see exactly what would have to be opened.

If a standard box is not an option for the game, an [Application Compartment](../PlusContent/compartment-mode.md) box bypasses the bulk of the isolation hooks while keeping file and registry virtualization — enough to keep multiple instances separated, but not a security boundary:

```ini
[MyGameBox]
Enabled=y
NoSecurityIsolation=y
```

!!! note

    This feature requires a [supporter certificate](supporter-certificate.md). Without a valid certificate, Sandboxie refuses to start processes in a box configured this way and shows an error.

## One box per game instance

Give each instance its own box. File and registry virtualization then keep the instances separate without any extra configuration — each box gets its own copy-on-write folders, its own saved games, settings and caches:

```ini
[Game1]
NoSecurityIsolation=y
BoxDataFolder=%UserProfile%\Documents\GameInstance1

[Game2]
NoSecurityIsolation=y
BoxDataFolder=%UserProfile%\Documents\GameInstance2
```

`BoxDataFolder` is optional; without it the default sandbox folder is used. Pointing each box at its own data folder makes backups, profile resets ("delete sandbox contents") and per-instance modding straightforward, because everything for one instance lives in one place.

Start each instance from its own box, for example:

```plaintext
"C:\Program Files\Sandboxie-Plus\Start.exe" /box:Game1 "C:\Games\MyGame\launcher.exe"
"C:\Program Files\Sandboxie-Plus\Start.exe" /box:Game2 "C:\Games\MyGame\launcher.exe"
```

## Planning resources for multiple instances

Every instance runs a full game client — the sandbox itself is not the bottleneck, the game is. For reference, three instances of a typical online game are comfortable on a machine with 32 GB of RAM, assigning at least two CPU cores per instance so the host stays responsive. Graphics-heavy games are usually limited by the GPU rather than by Sandboxie; virtualized graphics settings inside the box can reduce CPU cost but may cost image quality.

Disk usage is dominated by the per-box copy-on-write folders. The first launch of each instance copies (and migrates) the game files into the box; subsequent starts reuse that copy. Plan for the game size multiplied by the number of instances, and remember that delete-sandbox-contents is the supported way to reclaim the space when an instance is retired.

## When a game still will not start

- **It hangs in an Application Compartment box too.** At this point Sandboxie's isolation is unlikely to be the blocker. Check the game's own requirements (GPU driver, redistributable runtimes, anti-cheat client), and try launching the game outside any sandbox as a control.
- **It worked before a Windows update.** Update Sandboxie Plus first (the driver may lack kernel data for the new build); if it is current, a fresh look at the box type is warranted.
- **Changing system virtualization settings did not help.** Community reports (and local testing on Windows 11) indicate that turning off memory integrity (HVCI) or VBS generally does **not** fix launcher watchdogs; the interaction is with the game's protection layer, not with kernel virtualization checks. Treat these settings as a security decision, not as a game-compatibility lever.

## Limitations to keep in mind

- An Application Compartment box materially reduces isolation — see its [security and compatibility model](../PlusContent/compartment-mode.md#security-and-compatibility-model). Use it for the game, not as a general-purpose configuration.
- If the supporter certificate expires, boxes using `NoSecurityIsolation=y` will refuse to start processes until a new certificate is applied. Keep track of the expiry date when relying on this mode for day-to-day use.
- Template rules remain in effect in an Application Compartment box. When a game needs a specific path or object, add the rule to its box rather than weakening the box further.

## Related pages

- [Application Compartment](../PlusContent/compartment-mode.md)
- [No Security Isolation](../Content/NoSecurityIsolation.md)
- [Start.exe Command Line](../Content/StartCommandLine.md)
- [Trace Log](../PlusContent/TraceLog.md)
