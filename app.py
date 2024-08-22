import psutil
import subprocess
import logging


class SystemMonitor:
    def __init__(self, cpu_treshold=90, ram_treshold=90, log_file='/var/log/system_monitor.log'):
        self.cpu_treshold = cpu_treshold
        self.ram_treshold = ram_treshold
        self.log_file = log_file

        # Configure logging
        logging.basicConfig(
            filename=self.log_file,
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        )

    def log(self, message):
        logging.debug(message)
        print(message)

    def check_cpu_load(self):
        cpu_load = psutil.cpu_percent(interval=1, percpu=True)
        self.log(f'Current CPU Load is {cpu_load}%')
        for current_core in cpu_load:
            if current_core > 50:
                self.log(f'Warning: CPU core {current_core} exceeds 50%')
        return cpu_load

    def check_ram_load(self):
        ram_load = psutil.virtual_memory().percent
        self.log(f'Current RAM Load is {ram_load}%')
        return ram_load

    def restart_services(self, php_version="7.3"):
        try:
            subprocess.run(["systemctl", "restart", f"php{php_version}-fpm.service"], check=True)
            self.log(f' Restarted php{php_version}-fpm.service')
        except subprocess.CalledProcessError as e:
            self.log(f' Failed to restart php{php_version}-fpm.service. {e}')

        try:
            subprocess.run(["systemctl", "restart", "apache2.service"], check=True)
            self.log(f' Restarted apache2.service')
        except subprocess.CalledProcessError as e:
            self.log(f' Failed to restart apache2.service. {e}')

    def monitor_system(self, php_version="7.3"):
        cpu_load = self.check_cpu_load()
        ram_load = self.check_ram_load()

        if cpu_load > self.cpu_treshold and ram_load > self.ram_treshold:
            self.restart_services(php_version)
        else:
            self.log("System load is normal, no actions are needed!")


if __name__ == '__main__':
    monitor = SystemMonitor(cpu_treshold=90, ram_treshold=90)
    monitor.monitor_system(php_version="7.3")
