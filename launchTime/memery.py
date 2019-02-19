import csv
import os
import time

from gl import GL_PACKAGE_NAME


class Controller():

    def __init__(self):
        self.all_data = [("timestamp", "rm", "vm")]

    def start(self):
        cmd = "adb shell top -d 1 >> memery.txt"
        os.popen(cmd)

    def analyFile(self):
        result = os.popen("cat memery.txt | grep com.dongmibang")
        i = 0
        for line in result:
            print(line)
            line = "#".join(line.split())
            vm = line.split("#")[5].strip("M")
            rm = line.split("#")[6].strip("M")
            self.all_data.append((i, rm, vm))
            i = i + 1

    def saveDataToCSV(self):
        csv_file = open("memery.csv", mode="w")
        writer = csv.writer(csv_file)
        writer.writerows(self.all_data)
        csv_file.close()


if "__main__" == __name__:
    controller = Controller()
    controller.start()
    time.sleep(10)
    controller.analyFile()
    controller.saveDataToCSV()
