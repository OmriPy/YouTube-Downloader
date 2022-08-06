import tkinter
from tkinter import ttk

class Entry(tkinter.Entry):
    def Clear(self):
        self.delete(0, tkinter.END)
    
    def Disable(self):
        self.config(state=tkinter.DISABLED)

    def Enable(self):
        self.config(state=tkinter.NORMAL)
    
    def InsertText(self, text: str):
        self.insert(0, text)

    def EnableClear(self):
        self.Enable()
        self.Clear()

    def EnableClearInsertDisable(self, text: str):
        self.EnableClear()
        self.InsertText(text)
        self.Disable()

def UnGrid(Widgets: list):
    for widg in Widgets:
        if type(widg) == tkinter.Button or type(widg) == tkinter.Entry or type(widg) == Entry\
            or type(widg) == ttk.Combobox or type(widg) == tkinter.Label:
            widg.grid_forget()
        else: raise TypeError("Unexpected argument types")