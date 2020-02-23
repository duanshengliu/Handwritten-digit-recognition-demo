# -*- coding:utf-8 -*-
from tkinter import Tk
from Window import Window

if __name__ == '__main__':
    win=Tk()
    ww = 530#窗口宽设定530
    wh = 430#窗口高设定430
    Window(win,ww,wh)
    win.protocol("WM_DELETE_WINDOW",Window.closeEvent)
    win.mainloop()