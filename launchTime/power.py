import csv
import os
import time


class Controller():

    def __init__(self, count):
        self.all_data = [('timestamp', 'power')]
        self.counter = count

    def testprocess(self):

        result = os.popen('adb shell dumpsys battery')

        for line in result:
            if "level" in line:
                power = line.split(":")[1]
                break

        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.all_data.append((current_time, power))

    def run(self):
        # 设置为非充电状态
        os.popen("adb shell dumpsys battery set status 1")
        while self.counter > 0:
            self.counter = self.counter - 1
            self.testprocess()
            time.sleep(3)

    def saveToCSV(self):
        csv_file = open("power.csv", mode="w")
        writer = csv.writer(csv_file)
        writer.writerows(self.all_data)
        csv_file.close()


if "__main__" == __name__:
    controller = Controller(10)
    controller.run()
    controller.saveToCSV()
