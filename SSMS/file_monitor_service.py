import os
import sys
import win32serviceutil
import win32service
import win32event
import servicemanager
import file_monitor  # Make sure this matches the filename of your script

class FileMonitorService(win32serviceutil.ServiceFramework):
    _svc_name_ = "FileMonitorService"
    _svc_display_name_ = "File Monitor Service"
    _svc_description_ = "Monitors a folder and logs actions for non-CSV and non-Excel files"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.is_running = False
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        file_monitor.monitor_folder()

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(FileMonitorService)
