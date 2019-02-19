import csv
import os
import time

from gl import *


class Controller():

    def __init__(self, count):
        self.counter = count
        self.cpu_value = ""
        self.all_data = [('timestamp', 'cpustatus')]

    def testprocess(self):
        result = os.popen("adb shell dumpsys cpuinfo | grep %s" % GL_PACKAGE_NAME)
        for line in result.readlines():
            self.cpu_value = line.split('%')[0]
        current_time = self.getCurrentTime()
        self.all_data.append((current_time, self.cpu_value))

    def run(self):
        while self.counter > 0:
            self.testprocess()
            self.counter = self.counter - 1
            time.sleep(1)

    def getCurrentTime(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    def saveToCSV(self):
        csv_file = open('cpuinfo.csv', mode='w')
        writer = csv.writer(csv_file)
        writer.writerows(self.all_data)
        csv_file.close()


if "__main__" == __name__:
    con = Controller(20)
    con.run()
    con.saveToCSV()
