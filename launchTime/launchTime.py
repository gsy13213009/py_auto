import csv
import os
import time


class App():

    def __init__(self):
        self.content = None
        self.startTime = None

    def launchApp(self):
        cmd = 'adb shell am start -W -n com.dongmibang.dongmibang/.activity.SplashActivity'
        self.content = os.popen(cmd)

    def stopColdApp(self):
        cmd = 'adb shell am force-stop com.dongmibang.dongmibang'
        os.popen(cmd)

    def stopHotApp(self):
        cmd = 'adb shell input keyevent 3'
        os.popen(cmd)

    def getLaunchTime(self):
        for line in self.content.readlines():
            if 'ThisTime' in line:
                self.startTime = line.split(":")[1]
                break
        return self.startTime


class Controller():

    def __init__(self, count):
        self.app = App()
        self.counter = count
        self.all_data = [('timestamp', "elapsedtime")]

    # 单次测试
    def testProcess(self):
        self.app.launchApp()
        elpasedtime = self.app.getLaunchTime()
        time.sleep(5)
        self.app.stopHotApp()
        current_time = self.getCurrentTime()
        time.sleep(1)
        self.all_data.append((current_time, elpasedtime))

    def run(self):
        while self.counter > 0:
            self.testProcess()
            self.counter = self.counter - 1

    def getCurrentTime(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return current_time

    def saveDataToCSV(self):
        csv_file = open('startTime_hot.csv', mode='w')
        writer = csv.writer(csv_file)
        writer.writerows(self.all_data)
        csv_file.close()


if "__main__" == __name__:
    controller = Controller(10)
    controller.run()
    controller.saveDataToCSV()
