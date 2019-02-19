import csv
import os
import string
import time

from gl import GL_PACKAGE_NAME


class Controller():
    def __init__(self, count):
        self.all_data = [('timestap', 'date')]
        self.data = ""
        self.counter = count

    def testprocess(self):
        pid = os.popen('adb shell ps | grep %s' % GL_PACKAGE_NAME).readlines()[0].split(" ")[5]
        result = os.popen('adb shell cat /proc/%s/net/dev' % pid)

        for line in result:
            if "wlan0" in line:
                line = "#".join(line.split())
                receive = line.split("#")[1]
                transmit = line.split("#")[9]

        alltraffic = int(receive) + int(transmit)
        alltraffic = alltraffic / 1024

        current_time = self.getCurrentTime()
        self.all_data.append((current_time, alltraffic.__str__()))

    def getCurrentTime(self):
        return time.strftime('%Y-%m_%d %H:%m:%s', time.localtime())

    def run(self):
        while self.counter > 0:
            self.counter = self.counter - 1
            self.testprocess()
            time.sleep(3)

    def saveToCSV(self):
        csv_file = open("traffic.csv", mode='w')
        writer = csv.writer(csv_file)
        writer.writerows(self.all_data)
        csv_file.close()


if "__main__" == __name__:
    controller = Controller(10)
    controller.run()
    controller.saveToCSV()
