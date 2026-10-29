# 进程速度设置 {#process-speed-settings}

进程速度设置是 [Sandboxie Ini](SandboxieIni.md) 中的沙盒设置，自 Sandboxie Plus 1.14.0 起可用。它们调整沙盒化进程内选定的 Windows 计时、休眠和计时器 API。它们不会更改 Windows 系统时钟，也不会为沙盒提供完整的时间虚拟化。

## 启用进程速度更改 {#enabling-process-speed-changes}

使用以下配置为沙盒启用该功能：

```ini
[DefaultBox]
UseChangeSpeed=y
```

`UseChangeSpeed=y` 会在适用的计时钩子初始化期间启用安装，其运行时回退值为禁用（`n`）。该值可以来自沙盒节、适用的已启用模板或 `[GlobalSettings]`；未直接写在沙盒节中，并不一定意味着该功能被禁用。当没有任何生效的值启用它时，相应的钩子不会被安装。

请使用较小的正十进制整数因子。六个因子的使用方回退值（consumer fallback）均为 `1`，即正常的中性值。普通的字面量 `0` 也会回退到该值；`AddSleepSpeed=0` 并不是跳过休眠调用的指令，也不应通过设为 0 来禁用该功能。

## 受影响的 API {#affected-apis}

这些设置只作用于下列 API 组。

### 时钟滴答与时钟函数 {#tick-and-clock-functions}

`AddTickSpeed` 和 `LowTickSpeed` 控制：

- `GetTickCount`
- `GetTickCount64`
- `QueryUnbiasedInterruptTime`
- `QueryPerformanceCounter`

对于算术范围内的较小正值，列出的大多数时钟大致按 `AddTickSpeed / LowTickSpeed` 缩放，但它们的计算方式并不相同。`GetTickCount` 以安装其钩子时捕获的原生参考值为基准，对经过时间值做缩放；`GetTickCount64` 和 `QueryPerformanceCounter` 则缩放原生的绝对值。该功能不会安装对应的 `QueryPerformanceFrequency` 钩子。

在当前实现中，`QueryUnbiasedInterruptTime` 会先对整数因子做除法，再缩放结果。因此，与其他列出的时钟不同，小于 1 的分数比值可能得到 0，而不是按比例变慢；诸如 `3/2` 的比值会被截断为 `1`。这是当前实现的一项限制，而不是一致的分数缩放约定。参见 [当前的时钟包装函数](https://github.com/sandboxie-plus/Sandboxie/blob/31ba1e5c1aaaf3c98248a8994aecc9d016b7a310/Sandboxie/core/dll/kernel.c#L326-L401)。

这些函数表示经过时间或性能计数器时间，而不是系统日期和时间。受影响的计时源是各自独立调整的，不应被视为单一而精确的虚拟时钟。比较不同 Windows 计时源的应用程序可能会观察到差异。

### 休眠函数 {#sleep-functions}

`AddSleepSpeed` 和 `LowSleepSpeed` 控制通过 Sandboxie 的 `SleepEx` 钩子传递的请求时长。Sandboxie 不会安装单独的 `Sleep` 钩子：只有当普通 `Sleep` 调用在 Windows 中的实际执行路径到达被拦截的 `SleepEx` 实现时，它们才会受到影响。

对于算术范围内的普通正值，转发后的时长约为 `requested duration * LowSleepSpeed / AddSleepSpeed`。请求的延迟越短，执行就越可能推进得更快。在另一个因子保持为 `1` 时：

- `AddSleepSpeed=2` 会把请求的 1000 ms 休眠转发为 500 ms。
- `LowSleepSpeed=2` 会把请求的 1000 ms 休眠转发为 2000 ms。

这些是请求的间隔，并不保证实际的经过时间。转换在除法之前以 32 位无符号算术相乘：较大的值可能溢出，很小的结果可能被截断为 0，任意缩放也未必能保留 `INFINITE` 这类特殊超时值。

这不会修改 `WaitForSingleObject` 这类同步等待。实际经过时间仍受 Windows 正常调度、计时器分辨率行为和可警报休眠（alertable sleep）语义的约束。

### 计时器函数 {#timer-functions}

`AddTimerSpeed` 和 `LowTimerSpeed` 控制：

- `SetTimer`
- `timeGetTime`
- `timeSetEvent`

在当前实现中，`timeGetTime` 属于计时器因子组，而不是时钟滴答因子组。它使用自己的原生参考值（在安装其钩子时捕获）来调整返回的时钟值，这一点与 `GetTickCount` 不同；它不会更改计时器间隔。

对于算术范围内的普通正因子，`SetTimer` 和 `timeSetEvent` 大致按 `LowTimerSpeed / AddTimerSpeed` 调整请求的间隔；`timeGetTime` 时钟则遵循对应的 `AddTimerSpeed / LowTimerSpeed` 关系。在另一个因子为 `1` 时：

- `AddTimerSpeed=2` 大致将请求的计时器间隔减半，并使 `timeGetTime` 的推进速度约快一倍。
- `LowTimerSpeed=2` 大致将请求的计时器间隔加倍，并使 `timeGetTime` 的推进速度约慢一半。

间隔包装函数使用 64 位中间算术，然后再转换回原生间隔类型；较大的变换后数值可能发生窄化或回绕。Windows 的计时器最小值、支持范围、分辨率、消息处理和调度仍然生效，因此实际回调或消息送达时间可能与计算出的间隔不同。计时器钩子的安装还受额外的 GUI 条件约束，详见“运行时范围”一节。

## 因子对照 {#factor-comparison}

| 设置 | 控制对象 | 取值 `2` |
| --- | --- | --- |
| `AddTickSpeed` | 受支持的滴答（tick）/时钟源 | 约快一倍，受上文所述的时钟限制约束 |
| `LowTickSpeed` | 受支持的滴答/时钟源 | 约慢一倍，但 `QueryUnbiasedInterruptTime` 会得到 0 |
| `AddSleepSpeed` | `SleepEx` 请求时长 | 1000 ms 的请求转发为 500 ms |
| `LowSleepSpeed` | `SleepEx` 请求时长 | 1000 ms 的请求转发为 2000 ms |
| `AddTimerSpeed` | 受支持的计时器 API | 请求间隔约减半；`timeGetTime` 变快 |
| `LowTimerSpeed` | 受支持的计时器 API | 请求间隔约加倍；`timeGetTime` 变慢 |

每一对中的另一个因子均假定为 `1`。这些是请求转换或近似的时钟关系，受上文所述限制的约束。

## 示例 {#example}

```ini
[DefaultBox]
UseChangeSpeed=y
AddTickSpeed=2
AddSleepSpeed=2
AddTimerSpeed=2
```

在相应钩子已安装且取值处于算术范围内时，该配置通常会导致：

- 受影响的滴答和时钟源推进速度约快一倍，但不会使它们成为同一个一致的时钟；
- 请求的 1000 ms 休眠被转发为 500 ms；
- 请求的计时器间隔大约减少一半；
- `timeGetTime` 的推进速度约快一倍。

## 组合使用 Add 与 Low 因子 {#combining-add-and-low-factors}

同一组的 Add 与 Low 变体可以同时配置，两者互不覆盖。例如：

```ini
[DefaultBox]
UseChangeSpeed=y
AddTickSpeed=2
LowTickSpeed=3
```

在算术范围内，这会对 `GetTickCount`、`GetTickCount64` 和 `QueryPerformanceCounter` 施加约 `2/3` 的缩放，并各自使用不同的参考点。`QueryUnbiasedInterruptTime` 则先用 `2` 除以 `3`，结果为 0。因此，Add 与 Low 的取值按被拦截的 API 组合，而不是套用同一个统一公式。滴答、休眠和计时器这三个因子组相互独立，更改其中一组不会自动配置其他组。

## 运行时范围 {#runtime-scope}

相应的钩子通过 Sandboxie 注入的 DLL 在沙盒化进程内运行。是否安装取决于有效配置、初始化路径、API/模块的可用性、挂钩是否成功以及适用的钩子抑制设置；并非每个进程都会获得每一个钩子。这不是对 Windows 时钟的系统级更改。在非沙盒化运行时，SandMan 和 Sandboxie 服务通常不受影响。

计时器钩子还依赖 GUI 初始化。在应用隔间中，或在 `NoSandboxieDesktop=y` 生效时，它们的安装代码块会被跳过；滴答/时钟钩子和 `SleepEx` 钩子不共享这一 GUI 条件。

`UseChangeSpeed` 由相关的初始化器读取。重新加载配置不会重放已完成的初始化器，也不会追溯安装或移除计时钩子。要可靠地更改钩子的安装状态，请重启受影响的沙盒化应用程序。尚未运行的 GUI 初始化器可能在之后读取到新生效的取值；这属于延迟初始化，而不是由重新加载引起的重新安装。

全部六个数值因子都会在相应的钩子调用期间查询，因此成功重新加载的取值可以影响已安装的钩子。各因子对是分别读取的，跨计时源的更新并非原子操作，且初始化时保留的引用意味着更改可能导致时钟不连续。间隔更改作用于后续被拦截的调用；仅更改因子并不会重新设定已有的计时器。仅保存文件并不等于配置重新加载成功。一般的更新并不必然需要重启 Sandboxie 服务、驱动程序或 Windows。

## 预期用途 {#intended-use}

该功能适用于以下场景：在分析或测试期间缩短固定的应用程序延迟，以及为兼容的单人应用程序或游戏修改逻辑速度。兼容性取决于应用程序使用了哪些 Windows 计时机制。它不会加速 CPU 执行或提高处理器频率，也不保证应用程序执行得更快或游戏能够兼容。

## 限制 {#limitations}

- 该功能不会拦截所有 Windows 时间源或等待机制。系统实际时间（wall clock）API、`NtQuerySystemTime`、`NtDelayExecution`、同步等待、可等待计时器、计时器队列和线程池计时器均不在覆盖范围内。
- 由于只调整选定的 API，比较多个计时源的应用程序可能会观察到不一致的经过时间。
- 休眠因子通常不会缩短或延长同步等待。
- 更改计时行为可能影响应用程序逻辑、响应速度、媒体处理或超时假设。
- 请使用较小的正整数因子。整数舍入、算术限制、原生计时器约束和应用程序的计时假设都可能产生意外结果，尤其是在因子较大或间隔极短时。Add 与 Low 因子相等，并不能普遍防止中间溢出。

这些设置目前没有专门的图形界面控件。在 SandMan 中，请使用 **沙盒选项 > 配置文本 > 编辑配置**。在 Sandboxie Control（Classic）中，请使用 **配置 > 编辑配置**。在适用的情况下，Plus 与 Classic 共享相关运行时代码；手动配置不保证钩子安装成功，也不保证得到特定的计时结果。

相关：[Sandboxie Ini](SandboxieIni.md)。
