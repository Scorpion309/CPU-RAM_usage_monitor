import sys
import tkinter
from tkinter import ttk

from process import CpuBar
from widget_update import Configure_widgets


class Application(tkinter.Tk, Configure_widgets):

    def __init__(self):
        tkinter.Tk.__init__(self)
        self.attributes('-alpha', 1)
        self.attributes('-topmost', True)
        self.overrideredirect(True)
        self.resizable(False, False)
        self.title('CPU-RAM usage monitor bar')
        self.cpu = CpuBar()
        self.run_with_full_window()
        self.get_installed_disks()
        self.showing_disks = False

    def run_with_full_window(self):
        self.set_ui()
        self.make_bar_cpu_ussage()
        self.configure_cpu_bar()

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

        move_button = ttk.Button(self.bar2, text='move', command=self.configure_window)
        move_button.pack(side=tkinter.LEFT)

        open_button = ttk.Button(self.bar2, text='disks', command=self.show_disk_usage)
        open_button.pack(side=tkinter.LEFT)

        self.bar = ttk.LabelFrame(self, text='Power')
        self.bar.pack(fill=tkinter.BOTH)

        self.bind_class('Tk', '<Enter>', self.enter_mouse)
        self.bind_class('Tk', '<Leave>', self.leave_mouse)

        self.combo_win.bind('<<ComboboxSelected>>', self.choise_combo)

    def make_bar_cpu_ussage(self):
        cpu_frequency = self.cpu.cpu_frequency_return()[0]
        ttk.Label(self.bar,
                  text=f'Physical cores: {self.cpu.cpu_count}, logical cores: {self.cpu.logical_cpu_count}, frequency:  {cpu_frequency} Mhz',
                  anchor=tkinter.CENTER).pack(fill=tkinter.X)

        self.list_label = []
        self.list_pbar = []

        for i in range(self.cpu.logical_cpu_count):
            self.list_label.append(ttk.Label(self.bar, anchor=tkinter.CENTER))
            self.list_pbar.append(ttk.Progressbar(self.bar, length=100))
        for i in range(self.cpu.logical_cpu_count):
            self.list_label[i].pack(fill=tkinter.X)
            self.list_pbar[i].pack(fill=tkinter.X)

        self.ram_label = ttk.Label(self.bar, text='', anchor=tkinter.CENTER)
        self.ram_label.pack(fill=tkinter.X)
        self.ram_bar = ttk.Progressbar(self.bar, length=100)
        self.ram_bar.pack(fill=tkinter.X)

    def get_installed_disks(self):
        self.mounted_disks = self.cpu.mounted_disks_return()

    def show_disk_usage(self):
        if not self.showing_disks:
            self.list_disk_label = []
            self.list_disk_pbar_label = []
            self.disks_bar = ttk.LabelFrame(self, text='Disks')
            self.disks_bar.pack(fill=tkinter.X)
            self.disks_label = ttk.Label(self.disks_bar, text='Installed disks:', anchor=tkinter.CENTER)
            self.disks_label.pack(fill=tkinter.X)

            for _ in self.mounted_disks:
                self.list_disk_label.append(ttk.Label(self.disks_bar, anchor=tkinter.CENTER))
                self.list_disk_pbar_label.append(ttk.Progressbar(self.disks_bar, length=100))

            for index, value in enumerate(self.list_disk_label):
                self.list_disk_label[index].pack(fill=tkinter.X)
                self.list_disk_pbar_label[index].pack(fill=tkinter.X)

            self.configure_disks_window()
            self.showing_disks = True
            self.update()
        else:
            self.after_cancel(self.reload_disk_usage)
            self.disks_bar.destroy()
            self.showing_disks = False

    def create_minimal_window(self):
        self.cpu_bar_for_minimal_window = ttk.Progressbar(self, length=100)
        self.cpu_bar_for_minimal_window.pack(side=tkinter.LEFT)

        self.ram_bar_for_minimal_window = ttk.Progressbar(self, length=100)
        self.ram_bar_for_minimal_window.pack(side=tkinter.LEFT)

        to_full_view_button = ttk.Button(self, text='full', command=self.create_full_window, width=5)
        to_full_view_button.pack(side=tkinter.RIGHT)

        to_move_button = ttk.Button(self, text='move', command=self.configure_window, width=5)
        to_move_button.pack(side=tkinter.RIGHT)

        self.update()
        self.configure_minimal_window()

    def create_full_window(self):
        self.after_cancel(self.reload_usage)
        self.clear_window()
        self.update()
        self.run_with_full_window()
        self.enter_mouse('')
        self.combo_win.current(1)

    def enter_mouse(self, event):
        if self.combo_win.current() == 0 or 1:
            self.geometry('')

    def leave_mouse(self, event):
        if self.combo_win.current() == 0:
            self.geometry(f'{self.winfo_width()}x1')

    def choise_combo(self, event):
        if self.combo_win.current() == 2:
            self.enter_mouse('')
            self.unbind_class('Tk', '<Enter>')
            self.unbind_class('Tk', '<Leave>')
            self.combo_win.unbind('<<ComboboxSelected>>')
            self.after_cancel(self.reload_usage)
            self.clear_window()
            self.update()
            self.create_minimal_window()

    def app_exit(self):
        self.destroy()
        sys.exit()


if __name__ == '__main__':
    root = Application()
    root.mainloop()
