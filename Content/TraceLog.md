# Sandboxie Plus Trace logging UI

The Trace Log tool displays the names of any system resources that are accessed by programs running under the supervision of Sandboxie Plus. Designed to make it easy to identify those system resources which should be excluded from sandboxing, this tool can be used with the [Sandboxie Trace](SandboxieTrace.md) options.

**Important:** Please use the Trace Log tool only if you are asked to do so.

![](../Media/SBPlusTraceLog.png)

**Using the Trace Log**

1\. Enable **Trace Log** tab by opening **Options** menu -> **Trace Logging**.

2\. When the Trace Log tab is activated, it immediately starts to collect and display resource access information from all sandboxed programs that are running.

3\. At this point, perform any specific tasks that fail when done under the supervision of Sandboxie Plus.

4\. Finally, right click on the collected data and select the entry named **Copy Panel**. This copies the collected data into the clipboard.

5\. You can now paste (Ctrl+V) the collected data somewhere and make it available for analysis.

**Performance Impact**

When inactive, the Trace Log does not use any system resources and does not have any performance impact on any running programs. When active, the Trace Log, with most of the settings, has a small performance penalty on sandboxed programs.
