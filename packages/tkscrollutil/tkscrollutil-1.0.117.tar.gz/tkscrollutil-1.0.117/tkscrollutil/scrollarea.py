from tkinter import Widget
from tkscrollutil.load import load


class ScrollArea(Widget):
    def __init__(self, master=None, cnf={}, **kw):
        """The command creates a new window named and of the class , and makes it into a scrollarea widget.
        Additional options, described below, may be specified on the command line or in the option database to configure aspects of the scrollarea such as its borderwidth, relief, and display mode to be used for the scrollbars.
        The command returns its argument.
        At the time this command is invoked, there must not exist a window named , but 's parent must exist.scrollutil::scrollareapathNameScrollareascrollutil::scrollareapathNamepathNamepathName

        STANDARD OPTIONS

            activebackground, activeforeground, anchor,
            background, bitmap, borderwidth, cursor,
            disabledforeground, font, foreground
            highlightbackground, highlightcolor,
            highlightthickness, image, justify,
            padx, pady, relief, repeatdelay,
            repeatinterval, takefocus, text,
            textvariable, underline, wraplength

        WIDGET-SPECIFIC OPTIONS

            autohidescrollbars, lockinterval,
            respectheader, respecttitlecolumns, setfocus, xscrollbarmode, yscrollbarmode

        """
        try:
            load(master)
        except:
            from tkinter import _default_root
            load(_default_root)
        Widget.__init__(self, master, "scrollutil::scrollarea", cnf, kw, )

    def attrib(self, name=None, value=None):
        return self.tk.call(self._w, "attrib", name, value)

    def hasattrib(self, name=None):
        has = self.tk.call(self._w, "hasattrib", name)
        if has == 1:
            return True
        else:
            return False

    def unsetattrib(self, name=None):
        return self.tk.call(self._w, "unsetattrib", name)

    def setwidget(self, widget: Widget = ""):
        return self.tk.call(self._w, "setwidget", widget)


if __name__ == '__main__':
    from tkinter import Tk, Listbox
    root = Tk()

    area = ScrollArea(root, lockinterval=30000)
    list = Listbox(area)
    for item in range(30):
        list.insert(item+1, item+1)
    area.setwidget(list)
    area.pack(fill="both", expand="yes")

    root.mainloop()