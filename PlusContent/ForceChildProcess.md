# ForceProcessChild

It was introduced after 1.14.0. When you start a new program in Sandman, select “Run outside the sandbox” in the sandbox selection window, and you'll see this option later.

## How does it work?

It is based on a process tracking mechanism.

## Can I use it in Classic Build?

Yes,you can.but you need to use command line.For example,"start.exe /box:DefaultBox /fcp Program.exe" could run a unsandboxed program named "Program.exe",and its child process will be forced into DefaultBox.

## Will any process it starts be sandboxed?

Yeah,but also no.Direct child processes opened through interfaces such as CreateProcess are sandboxed, but since they are not in the sandbox, we can not control the child processes that are indirectly opened through the DCOM or IPC interfaces.

### Un-shell explorer
Explorer is a typical example.When there is no explorer as shell running in the desktop,most of its child process will be forced.But if there is already a explorer as shell,the new explorer process will call the pervous explorer through DCOM,and then the shell explorer create a window that not controled by us,and the new process terminate by itself.
