# tkscrollutil

[文档](https://www.nemethi.de/scrollutil/index.html) [主页](https://www.nemethi.de/)

![PyPI](https://img.shields.io/pypi/v/tkscrollutil?color=07c160&label=winico)
![PyPI - Downloads](https://img.shields.io/pypi/dw/tkscrollutil?color=0f5fff)
![PyPI - License](https://img.shields.io/pypi/l/tkscrollutil?color=red)

---

## ScrolllArea
可以快速地为水平滚动、垂直滚动组件设置滚动条

### 属性
`autohidescrollbars` 设置组件是否自动隐藏滚动条。布尔数值。默认`False`。也就是说，当你把鼠标指针放到滚动条上时，滚动条才会显示。 

`lockinterval` 设置组件滚动条地锁定间隔。整数数值。默认`300`.

`respectheader` 仅当将嵌入到组件内地`tablelist`版本为6.5及以上版本时才能使用，后续等开发出`tablelist`的扩展库时补充

`respecttitlecolumns` 仅当将嵌入到组件内地`tablelist`版本为6.5及以上版本时才能使用，后续等开发出`tablelist`的扩展库时补充

`xscrollbarmode` 设置水平滚动条的模式。可选值为`static` `dynamic` `none`。默认`none`。`static`为常驻滚动条；`dynamic`为自动滚动条；`none`为没有滚动条

`yscrollbarmode` 设置垂直滚动条的模式。可选值为`static` `dynamic` `none`。默认`static`。`static`为常驻滚动条；`dynamic`为自动滚动条；`none`为没有滚动条

### 方法
`setwidget` 设置具有滚动条属性的组件，使组件快速设置滚动条。

### 示例
```python
from tkinter import Tk, Listbox
from tkscrollutil import ScrollArea

Window = Tk()

Area = ScrollArea(Window)
List = Listbox(Area)
for Item in range(50):
    List.insert(Item+1, Item+1)
Area.setwidget(List)
Area.pack(fill="both", expand="yes")

Window.mainloop()
```

## ttkScrollArea
见上方。与`ScrollArea`不同的是，`ttkScrollArea`具有ttk组件的属性，并且`ScrollArea`和`ttkScrollArea`不能同时使用。

### 示例
```python
from tkinter import Tk, Listbox
from tkscrollutil import ttkScrollArea

Window = Tk()

Area = ttkScrollArea(Window)
List = Listbox(Area)
for Item in range(50):
    List.insert(Item+1, Item+1)
Area.setwidget(List)
Area.pack(fill="both", expand="yes")

Window.mainloop()
```

## ScrollSync
同步滚动条，当其中一个滚动时，另一个也会跟随着移动起来。

### 方法
`setwidgets` 设置同步滚动的组件。需输入列表，如 [widget1, widget2] 。

`widgets` 获取同步滚动的组件。

### 示例
```python
from tkinter import Tk, Listbox, Frame
from tkscrollutil import ScrollArea, ScrollSync
Window = Tk()

Frame = Frame()

Area = ScrollArea(Frame, yscrollbarmode="static")
Sync = ScrollSync(Area)
Area.setwidget(Sync)

Area.pack(fill="y", side="right")

List1 = Listbox()
List1.pack(fill="both", side="left", expand="yes")
List2 = Listbox()
List2.pack(fill="both", side="right", expand="yes")

for Item in range(300):
    List1.insert(Item, Item)
    List2.insert(Item, Item)

Sync.setwidgets([List1, List2])

Frame.pack(fill="both", expand="yes")

Window.mainloop()
```

## ttkScrollSync
见上方。与`ScrollSync`不同的是，`ttkScrollSync`具有ttk组件的属性，并且`ScrollSync`和`ttkScrollSync`不能同时使用。

### 示例
```python
from tkinter import Tk, Listbox, Frame
from tkscrollutil import ttkScrollArea, ttkScrollSync
Window = Tk()

Frame = Frame()

Area = ttkScrollArea(Frame, yscrollbarmode="static")
Sync = ttkScrollSync(Area)
Area.setwidget(Sync)

Area.pack(fill="y", side="right")

List1 = Listbox()
List1.pack(fill="both", side="left", expand="yes")
List2 = Listbox()
List2.pack(fill="both", side="right", expand="yes")

for Item in range(300):
    List1.insert(Item, Item)
    List2.insert(Item, Item)

Sync.setwidgets([List1, List2])

Frame.pack(fill="both", expand="yes")

Window.mainloop()
```

## ttkScrolledNoteBook
scrollutil本身不提供ScrolledNoteBook，只有ttk能够提供。
```python
from tkinter import Tk, Frame
from tkscrollutil import ttkScrolledNoteBook, addclosetab
Window = Tk()

NoteBook = ttkScrolledNoteBook(Window)

addclosetab("TNotebook")

NoteBook.add(Frame(NoteBook), text="Hello World")
NoteBook.pack(fill="both", expand="yes")

Window.mainloop()
```