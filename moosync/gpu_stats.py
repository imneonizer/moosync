import pynvml

class GpuStats:
    def __init__(self):
        pynvml.nvmlInit()
        self.count = pynvml.nvmlDeviceGetCount()
        self.all_gpus = [i for i in range(self.count)]
    
    def human_size(self, bytes, units=[' bytes','KB','MB','GB','TB', 'PB', 'EB']):
        """ Returns a human readable string representation of bytes """
        return str(bytes) + units[0] if bytes < 1024 else self.human_size(bytes>>10, units[1:])

    def pprint(self):
        for i in range(self.count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            name = pynvml.nvmlDeviceGetName(handle).decode().replace("NVIDIA", "").strip()
            info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            
            print(f"{i}. {name} {self.human_size(info.used)}/{self.human_size(info.total)} ({(info.used/info.total)*100:.2f}%)")
    
    def list_gpus_free_more_than(self, free_percent):
        gpus = []
        for i in range(self.count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            
            gpu_memory_free_perecent = (info.free / info.total)
            if gpu_memory_free_perecent >= free_percent:
                gpus.append(i)
        
        return gpus

    def list_gpus_used_less_than(self, used_percent):
        gpus = []
        for i in range(self.count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            
            gpu_memory_used_perecent = (info.used / info.total)
            if gpu_memory_used_perecent <= used_percent:
                gpus.append(i)
        
        return gpus
    
    def verify_gpu_index(self, gpus):
        if isinstance(gpus, int):
            gpus = [gpus]
        for i in gpus:
            if i not in self.all_gpus:
                raise ValueError(f"GPU index {i} out of range, possible values: {self.all_gpus}")
    
    def are_gpus_available(self, gpus, thresh=0.5):            
        available_gpus = self.list_gpus_free_more_than(thresh)
        result = True
        for i in gpus:
            self.verify_gpu_index(i)
            if i not in available_gpus:
                result = False
        return result

gpustats = GpuStats()