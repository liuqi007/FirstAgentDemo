import platform
import psutil
import subprocess
import json

def get_host_info() -> str:
    """get host information.
    Returns:
        str: the host information in json format string.
    """
    host_info = {
        "platform": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "architecture": platform.architecture(),
        "processor": platform.processor(),
        "memory": str(round(psutil.virtual_memory().total / (1024.0 ** 3), 2)) + " GB",
    }
    cpu_count = psutil.cpu_count()
    host_info["cpu_count"] = cpu_count


    try:
        cpu_model = subprocess.check_output("wmic cpu get caption", shell=True).decode().strip().split("\n")[1]
        host_info["cpu_model"] = cpu_model
    except Exception as e:
        host_info["cpu_model"] = "unknown"

    return json.dumps(host_info, indent=4)


if __name__ == '__main__':
    print(get_host_info())