import psutil


class CpuBar:

    def __init__(self):
        self.cpu_count = psutil.cpu_count(logical=False)
        self.logical_cpu_count = psutil.cpu_count()

    def cpu_usage_return(self):
        return psutil.cpu_percent(percpu=True)

    def cpu_summary_usage_return(self):
        return psutil.cpu_percent()

    def ram_usage_return(self):
        return psutil.virtual_memory()

    def mounted_disks_return(self):
        return psutil.disk_partitions()

    def disk_usage_return(self, disk):
        self.disk_info = psutil.disk_usage(disk)
        self.disk_total = self.disk_info[0]
        self.disk_used = self.disk_info[1]
        self.disk_free = self.disk_info[2]
        self.disk_used_percent = self.disk_info[3]
        return self.disk_used_percent
