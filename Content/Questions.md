# Questions

* "Antivir can remove infected files out from Sandbox, why not some malware can access out of sandbox?" 

The difference here is that Antivir is not running sandboxed, so why would Sandboxie stop Antivir from doing ANYTHING?

In this case Antivir is reaching into the sandbox, which is a legitimate folder on your hard drive. You can do "Explore Contents of Sandbox" to open a shell window on that folder -- same thing.

But for programs that are running sandboxed, Sandboxie looks at every operation and decides if it allows or denies the operation, or if it redirects the operation to use an object from the sandbox.

* can't get sysinternals regmon(registry monitor) and filemon(file monitor) to work inside the sandbox. 

