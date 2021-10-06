class Configure_widgets:

    def configure_cpu_bar(self):
        cores_usage = self.cpu.cpu_usage_return()
        for core_index in range(self.cpu.logical_cpu_count):
            self.list_label[core_index].configure(text=f'core {core_index + 1} usage: {cores_usage[core_index]}%')
            self.list_pbar[core_index].configure(value=cores_usage[core_index])

        ram_usage = self.cpu.ram_usage_return()
        self.ram_label.configure(text=f'RAM usage: {ram_usage[2]}%, used: {round(ram_usage[3] / 1048576)} Mb,'
                                      f' available: {round(ram_usage[1] / 1048576)} Mb')
        self.ram_bar.configure(value=ram_usage[2])

        self.reload_usage = self.after(1000, self.configure_cpu_bar)

    def configure_window(self):
        if self.wm_overrideredirect():
            self.overrideredirect(False)
        else:
            self.overrideredirect(True)
        self.update()

    def configure_minimal_window(self):
        self.cpu_bar_for_minimal_window.configure(value=self.cpu.cpu_summary_usage_return())
        self.ram_bar_for_minimal_window.configure(value=self.cpu.ram_usage_return()[2])
        self.reload_usage = self.after(1000, self.configure_minimal_window)
        self.update()

    def configure_disks_window(self):
        for index, disk in enumerate(self.mounted_disks):
            disk_name = disk[0]
            disk_info = self.cpu.disk_usage_return(disk_name)
            disk_total = disk_info[0] / 1073741824
            disk_free = disk_info[2] / 1073741824
            disk_used_percent = disk_info[3]
            self.list_disk_label[index].configure(text=f'Disk {disk_name}({round(disk_total, 1)}Gb),'
                                                       f' usage: {disk_used_percent}%,'
                                                       f' available: {round(disk_free,1)} Gb')
            self.list_disk_pbar_label[index].configure(value=disk_used_percent)
        self.reload_disk_usage = self.after(1000, self.configure_disks_window)

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()
