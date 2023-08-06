import pandas as pd
import io


stock_df = pd.read_csv('D:\\Personal\\Jiiva\\DataSet\\tech-stocks-04-2021.csv')

print(stock_df)


class Axis:
    def __init__(self):
        self.x = []
        self.y = []
        self.z = []

class VibrationParam:
    def __init__(self):
        self.Fft = Axis()
        self.Rms = Axis()
        self.Velocity = Axis()
        self.Displacement = Axis()
        self.Acc = Axis()

class VsensProcess:
    def __init__(self):
        self.SensorMacID = ""
        self.VibrationData = VibrationParam()
        self.FirstDataTimestamp = None
        self.FlushoutPeriod = None
        self.Processed = 0
        self.AdditionalInfo = {}
        self.AxisList = []

    def axis_selection(self):
        pass

    def accumulate_data(self):
        pass

    def process_algorithms(self):
        pass

    def dispose(self):
        del self

    def __del__(self):
        print('object destroyed')



mydata = VsensProcess()

print(mydata)
del mydata
print('hello')
#print(mydata)