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
        return psutil.disk_usage(disk)
