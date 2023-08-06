import subprocess
import psutil

def is_nvidia_gpu_available():
   try:
      subprocess.check_output('nvidia-smi')
      return True
   except Exception:
      return False

def get_cpu_info():
    cpu_cores= psutil.cpu_count()
    mem = psutil.virtual_memory() #(total,available,percent,used,free,...)
    
    return {"CPU_cores":cpu_cores,
            "Memory": mem[1]}

def get_gpu_info():
    gpu_name_map = {"Tesla T4":"T4"}
    gpu_info = []
    try:
        proc = subprocess.Popen(
            ["nvidia-smi",
             "--query-gpu=gpu_name,index,uuid,memory.total,memory.free,memory.used,count,utilization.gpu,utilization.memory",
              "--format=csv"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = proc.communicate()
        stdout = stdout.decode("utf-8")
        stdout = stdout.split("\n")
        stdout.pop(0)
        for l in stdout:
            tokens = l.split(", ")
            if len(tokens) > 6:
                gpu_name = tokens[0]
                if gpu_name in gpu_name_map:
                    gpu_name = gpu_name_map[tokens[0]]
                gpu_info.append({'name': gpu_name.lower(),
                                 'id': tokens[1], 
                                 'mem': tokens[3],
                                 'cores': tokens[6],
                                 'mem_free': tokens[4],
                                 'mem_used': tokens[5],
                                 'util_gpu': tokens[7],
                                 'util_mem': tokens[8]})
        return gpu_info
    except Exception:
        return None