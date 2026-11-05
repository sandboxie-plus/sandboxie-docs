# BoxGrouping

`BoxGrouping` 是自 Sandboxie Plus 1.9.1 起提供的用户设置值。它保存每个用户的层级结构，供 SandMan 把沙盒组织成可视分组。

沙盒组只是用户界面元数据。它们不会改变沙盒隔离或内容，同一组内的沙盒也不共享设置。可视嵌套不会产生配置继承，也不是父子沙盒关系。

## 存储与作用范围

`BoxGrouping` 保存在 [Sandboxie Ini](SandboxieIni.md) 中，通常位于当前 Windows 用户的节里：

```ini
[UserSettings_12345678]
BoxGrouping=:Browsers,DefaultBox
BoxGrouping=Browsers:ChromeBox,Private
BoxGrouping=Private:FirefoxBox
```

它不是逐沙盒设置，不存放在 `[GlobalSettings]` 下，也不使用模板继承。每个 Windows 用户通常有各自的 `[UserSettings_xxxxxxxx]` 节，因此可能有不同的层级。便携配置则可能使用 `[UserSettings_Portable]`。

## 语法

一般形式为：

```ini
BoxGrouping=<parent>:<member1>,<member2>,...
```

例如：

```ini
BoxGrouping=:Box1,Group1
BoxGrouping=Group1:Box2,SubGroup
BoxGrouping=SubGroup:Box3
BoxGrouping=EmptyGroup:
```

- 冒号前的文本是父组。
- 空的父组表示根层级。
- 冒号后的条目是父组的直接子项。
- 若某个名称自身还有 `BoxGrouping=<name>:` 条目，则它是子组。
- 同一父组的重复行会扩展其成员列表。
- 以冒号结尾的条目定义一个空的具名组。

SandMan 支持嵌套分组。以下配置：

```ini
BoxGrouping=:Browsers,DefaultBox
BoxGrouping=Browsers:ChromeBox,Private
BoxGrouping=Private:FirefoxBox
```

表示：

```text
Browsers
├── ChromeBox
└── Private
    └── FirefoxBox

DefaultBox
```

嵌套纯粹是组织性的。`Private` 不会向 `FirefoxBox` 传递设置或限制。

## 根层级与层级规范化

空的父键表示根。例如：

```ini
BoxGrouping=:DefaultBox,Browsers
```

把 `DefaultBox` 和 `Browsers` 都放在顶层。SandMan 可能把该目标显示为 `[None]`；`[None]` 不是真正的具名组。

SandMan 会把层级规范化为树状结构，其中每个项只应有一个父级。界面会阻止把组移动到自身或其某个后代中。手工编辑产生的畸形重复或循环数据可能被自动规范化；不应依赖确切的冲突解决方式。

## 排序

`BoxGrouping` 保存 SandMan 手动排序模式所用的成员顺序。其他生效的排序模式，例如按字母或按列排序，可能以不同顺序显示同一层级。

该顺序是显示元数据，不控制沙盒或程序的执行顺序。

## 在 SandMan 中管理分组

SandMan 直接在其主沙盒树中管理分组。相关操作包括：

- **沙盒 > 新建沙盒组**；
- 从树或组的上下文菜单创建组；
- **移动沙盒** 与 **移动组**；
- **上移** 与 **下移**；
- 拖放。

移动沙盒只会改变其可视位置和存储顺序。它不会移动沙盒文件、重建沙盒、重启其进程或更改运行时策略。

### 移除、重命名与添加项

移除组不会删除其中的沙盒。**移除组** 只移除组织节点，并把它直属的沙盒与子组移到被移除组的父层级。若移除的是顶层组，其内容成为顶层项。

通过 SandMan 重命名沙盒会更新它的组引用。重命名组会保留其内容并更新其父级关系。

未被另行指派的新沙盒出现在根层。创建或导入时若选中了目标组，SandMan 可以把该沙盒放入那个组。复制沙盒目前会保留源沙盒的组成员关系。

## 树展开状态

展开与折叠的树状态不存放在 `BoxGrouping` 中。SandMan 把它作为用户界面配置单独保存。

当前启动行为可在 **全局设置 > 界面设置 > 用户界面 > 启动时的组状态** 下选择，模式包括：

- **记住上次状态**；
- **展开所有组**；
- **折叠所有组**。

简言之，`BoxGrouping` 保存成员关系、层级与手动同级顺序；树展开状态是另外的东西。

## 无运行时或隔离影响

`BoxGrouping` 不影响：

- 文件、注册表或进程隔离；
- 程序启动限制；
- 资源限制或访问规则；
- 沙盒内容；
- 配置继承；
- 执行顺序。

无论沙盒出现在哪个组中，每个沙盒仍独立配置。可视层级不意味着策略层级：沙盒组不提供组级设置、组模板、共享限制或额外隔离。

## 手动编辑与重载行为

SandMan 通常自动管理 `BoxGrouping`。可以手动编辑，但畸形的图可能被规范化。在修订后的层级出现之前，SandMan 必须观察到或重新加载该配置变更。沙盒内的应用程序不需要重启，因为分组只是界面层面的。

冒号和逗号是持久化格式中的结构分隔符。避免在手工创建的组名中使用 `:`，也不要使用逗号；SandMan 的界面会拒绝包含逗号的组名。界面还会拒绝组名中的括号和控制字符。

## Sandboxie Plus 与 Classic

SandMan 使用 `BoxGrouping`。Sandboxie Control Classic 与传统的 `Start.exe` 沙盒选择器继续使用 `BoxDisplayOrder`。

`BoxDisplayOrder` 是旧式布局格式，对当前 SandMan 布局而言已被标记为由 `BoxGrouping` 取代。在没有 `BoxGrouping` 映射可用时，SandMan 可以使用旧式层级作为回退，但 Plus 与 Classic 不会持续同步这两种格式。Classic 仍会读取 `BoxDisplayOrder`，因此不应认为它完全过时。

对应用户界面工作流参见 [沙盒菜单](SandboxMenu.md) 与 [Sandboxie Plus 迁移指南](PlusMigrationGuide.md)。

## 导出与备份行为

`BoxGrouping` 是用户界面配置，不是导出沙盒的固有元数据。只导出沙盒再导入的常规操作不会带上用户的分组层级。包含相应用户设置节的完整 `Sandboxie.ini` 备份才能保留它。

## 版本历史

当前的 `BoxGrouping` 存储格式在 Sandboxie Plus 1.9.1 引入，属于沙盒分组配置存储的一次重做。分组功能本身早于该设置。后续版本增加或修复了嵌套分组、重命名、拖放、托盘层级、排序与展开状态的持久化。
