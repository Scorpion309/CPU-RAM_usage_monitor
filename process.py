import psutil

class CpuBar:

    def __init__(self):
        self.cpu_count = psutil.cpu_count(logical=False)
        self.logical_cpu_count = psutil.cpu_count()


CpuBar()