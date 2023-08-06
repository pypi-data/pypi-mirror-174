from tkinter.ttk import Widget, Notebook
from tkscrollutil.load import load_tile
from tkscrollutil.attrib import Attrib


class ScrolledNoteBook(Attrib, Notebook):
    def __init__(self, master=None, cnf={}, **kw):
        """
        STANDARD OPTIONS

            activebackground, activeforeground, anchor,
            background, bitmap, borderwidth, cursor,
            disabledforeground, font, foreground
            highlightbackground, highlightcolor,
            highlightthickness, image, justify,
            padx, pady, relief, repeatdelay,
            repeatinterval, takefocus, text,
            textvariable, underline, wraplength

        """
        try:
            load_tile(master)
        except:
            from tkinter import _default_root
            load_tile(_default_root)
        Widget.__init__(self, master, "scrollutil::scrollednotebook", kw)


if __name__ == '__main__':
    from tkinter import Tk, Frame
    from tkscrollutil import ttkScrolledNoteBook, addclosetab
    root = Tk()

    notebook = ttkScrolledNoteBook()

    addclosetab("TNotebook")

    notebook.add(Frame(notebook), text="Hello World")
    notebook.pack(fill="both", expand="yes")

    root.mainloop()