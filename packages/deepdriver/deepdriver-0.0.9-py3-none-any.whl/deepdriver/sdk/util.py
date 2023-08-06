import multiprocessing
import os
import platform
import psutil
import pynvml

try:
    pynvml.nvmlInit()
except Exception:
    pass

def get_os() -> str:
    return platform.system()

def get_python_version() -> str:
    return platform.python_version()

def get_gpu() -> str:
    try:
        return pynvml.nvmlDeviceGetName(pynvml.nvmlDeviceGetHandleByIndex(0)).decode("utf-8")
    except Exception:
        return "no gpu"

def get_gpu_count() -> int:
    try:
        return pynvml.nvmlDeviceGetCount()
    except Exception:
        return 0

def get_cpu_count() -> int:
    return multiprocessing.cpu_count()

def get_hostname() -> str:
    return platform.node()

def get_system_cpu() -> float:
    return psutil.cpu_percent()

def get_system_disk() -> float:
    return psutil.disk_usage("/").used / (2**30)

def get_system_memory() -> float:
    return psutil.virtual_memory().used / (2**30)

def get_system_proc_cpu_threads() -> int:
    pid = os.getpid() # get pid
    proc = psutil.Process(pid)
    return proc.num_threads()

def get_system_proc_memory_rss_mb() -> float:
    pid = os.getpid() # get pid
    proc = psutil.Process(pid)
    return proc.memory_info().rss / 1048576.0

def get_system_proc_memory_percent() -> float:
    pid = os.getpid() # get pid
    proc = psutil.Process(pid)
    return proc.memory_percent()

def get_system_memory_available_mb() -> float:
    return psutil.virtual_memory().available / 1048576.0
