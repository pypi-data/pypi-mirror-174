import threading
import psutil
import logging
import requests
import rospy


# from mapping_cmd_helper import ErrCode
def get_process(name):
    for proc in psutil.process_iter():
        if name in proc.name():
            return proc
    return None


def get_memory_use(proc, unit='MB'):
    if unit == 'MB':
        return proc.memory_info()[0] / 2. ** 20
    elif unit == 'GB':
        return proc.memory_info()[0] / 2. ** 30
    else:
        logging.info("The memory unit is not supported")
        return -1


class ResourceMonitor(threading.Thread):
    def __init__(self, process_name, log_interval, bag, mission_id):
        logging.basicConfig(filename="{}.log".format(bag), filemode="w", level=logging.DEBUG)
        super(ResourceMonitor, self).__init__()
        self.bag = bag
        self.mission_id = mission_id
        self._process_name = process_name
        self._log_interval = log_interval  # the unit is in second
        self._event = threading.Event()
        self.setDaemon(True)
        self.start()

    def run(self):
        logging.info("begin monotor cpu and momory usage......")
        while not self._event.isSet() and not rospy.is_shutdown():
            process = get_process(self._process_name)
            if process is not None:
                cpu_percent = process.cpu_percent()
                memory_usage = get_memory_use(process, unit='MB')
                logging.info("{} cpu usage: %{}, memory usage: {} MB".format(self._process_name, cpu_percent, int(memory_usage)))
                try:
                    requests.post(url="http://10.12.32.66:5000/ci/monitor", json={"id": self.mission_id, "case_name": self.bag, "cpu": cpu_percent, "memory": memory_usage})
                except Exception as e:
                    logging.error(e)
                    continue

            try:
                self._event.wait(self._log_interval)
            except Exception:
                logging.info("Excetpion in Event.wait, hardware_resource_monitor will exit.")
                self._event.set()
                break
