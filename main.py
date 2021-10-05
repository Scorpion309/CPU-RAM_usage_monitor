import tkinter
from tkinter import ttk
from process import CpuBar
import sys

class Application(tkinter.Tk):

    def __init__(self):
        tkinter.Tk.__init__(self)
        self.attributes('-alpha', 1)
        self.attributes('-topmost', True)
        self.overrideredirect(True)
        self.resizable(False, False)
        self.title('CPU-RAM usage monitor bar')
        self.cpu = CpuBar()
        self.set_ui()
        self.make_bar_cpu_ussage()

    def set_ui(self):
        exit_button = ttk.Button(self, text='Exit', command=self.app_exit)
        exit_button.pack(fill=tkinter.X)

        self.bar2 = ttk.LabelFrame(self, text='Manual')
        self.bar2.pack(fill=tkinter.X)

        self.combo_win = ttk.Combobox(self.bar2,
                                      values=['hide', "don't hide", 'min'],
                                      width=9,
                                      state='readonly')
        self.combo_win.current(1)
        self.combo_win.pack(side=tkinter.LEFT)

        move_button = ttk.Button(self.bar2, text='move')
        move_button.pack(side=tkinter.LEFT)

        open_button = ttk.Button(self.bar2, text='>>>')
        open_button.pack(side=tkinter.LEFT)

        self.bar = ttk.LabelFrame(self, text='Power')
        self.bar.pack(fill=tkinter.BOTH)

        self.bind_class('Tk', '<Enter>', self.enter_mouse)
        self.bind_class('Tk', '<Leave>', self.leave_mouse)

    def make_bar_cpu_ussage(self):
        ttk.Label(self.bar, text=f'Physical cores: {self.cpu.cpu_count}, logical cores: {self.cpu.logical_cpu_count}',
                  anchor=tkinter.CENTER).pack(fill=tkinter.X)

        self.list_label = []
        self.list_pbar = []

        for i in range(self.cpu.logical_cpu_count):
            self.list_label.append(ttk.Label(self.bar, anchor=tkinter.CENTER))
            self.list_pbar.append(ttk.Progressbar(self.bar, length=100))
        for i in range(self.cpu.logical_cpu_count):
            self.list_label[i].pack(fill=tkinter.X)
            self.list_pbar[i].pack(fill=tkinter.X)

    def enter_mouse(self, event):
        if self.combo_win.current() == 0 or 1:
            self.geometry('')

    def leave_mouse(self, event):
        if self.combo_win.current() == 0:
            self.geometry(f'{self.winfo_width()}x1')


    def app_exit(self):
        self.destroy()
        sys.exit()



if __name__ == '__main__':
    root = Application()
    root.mainloop()