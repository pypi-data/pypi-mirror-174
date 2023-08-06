# tkwinico
为Windows系统提供开发系统托盘的功能。

---

## 示例
```python
from tkwinico import *
import tkinter as tk


Window = tk.Tk()


def CallBack(Message, X, Y):
    if Message == WM_RBUTTONDOWN:
        Menu = tk.Menu(tearoff=False)
        Menu.add_command(label="Quit", command=Window.quit)
        Menu.tk_popup(X, Y)


taskbar(ADD, load(APPLICATION), (Window.register(CallBack), MESSAGE, X, Y))

Window.mainloop()
```