import sys
import serial
import numpy as np
from time import sleep
from collections import deque
from matplotlib import pyplot as plt

def MotorACalibration(bitF):
    w = 7.430636447530014e-05
    a0 = 26.369001417046512
    a1 = 42.792366553793926
    b1 = -12.324717735287519
    a2 = 26.933499765232902
    b2 = -19.530367509074463
    a3 = 11.315150651232333
    b3 = -16.631428975580668
    a4 = 2.489294162580928
    b4 = -9.153722109383629
    a5 = -0.215475782450290
    b5 = -3.180320439074931
    a6 = -0.256214035002475
    b6 = -0.536035032104161
    return a0 + a1*np.cos(bitF*w) + b1*np.sin(bitF*w) \
           + a2*np.cos(2.0*bitF*w) + b2*np.sin(2.0*bitF*w) \
           + a3*np.cos(3.0*bitF*w) + b3*np.sin(3.0*bitF*w) \
           + a4*np.cos(4.0*bitF*w) + b4*np.sin(4.0*bitF*w) \
           + a5*np.cos(5.0*bitF*w) + b5*np.sin(5.0*bitF*w) \
           + a6*np.cos(6.0*bitF*w) + b6*np.sin(6.0*bitF*w)

def MotorBCalibration(bitF):
    w = 9.745973193663611e-05
    a0 = 2.677556372177879
    a1 = 0.087802552266365
    b1 = 2.132922208355770
    a2 = -0.379712039244581
    b2 = 1.173208902204697
    a3 = -0.357648678874241
    b3 = 0.611855241307163
    a4 = -0.301231731752640
    b4 = 0.228443777988462
    a5 = -0.189415796590939
    b5 = 0.049054710883965
    a6 = -0.084774303948667
    b6 = 0.009042376872602
    return a0 + a1*np.cos(bitF*w) + b1*np.sin(bitF*w) \
           + a2*np.cos(2.0*bitF*w) + b2*np.sin(2.0*bitF*w) \
           + a3*np.cos(3.0*bitF*w) + b3*np.sin(3.0*bitF*w) \
           + a4*np.cos(4.0*bitF*w) + b4*np.sin(4.0*bitF*w) \
           + a5*np.cos(5.0*bitF*w) + b5*np.sin(5.0*bitF*w) \
           + a6*np.cos(6.0*bitF*w) + b6*np.sin(6.0*bitF*w)

# class that holds analog data for N samples
class AnalogData:
  # constr
  def __init__(self, maxLen):
    self.ax = deque([0.0]*maxLen)
    self.maxLen = maxLen

  # ring buffer
  def addToBuf(self, buf, val):
    if len(buf) < self.maxLen:
      buf.append(val)
    else:
      buf.pop()
      buf.appendleft(val)

  # add data
  def add(self, data):
    assert(len(data) == 1)
    self.addToBuf(self.ax, data[0])

    
# plot class
class AnalogPlot:
  # constr
  def __init__(self, analogData, ylimits):
    # set plot to animated
    self.num_channels_VCA = 2
    self.num_channels = len(analogData)
    self.num_VCAs = self.num_channels / self.num_channels_VCA
    print "plot init"
    plt.ion()
    self.fig, self.axarry = plt.subplots(self.num_channels_VCA, self.num_VCAs, sharex = True)
    self.line = [None] * self.num_channels
    for i in range(self.num_VCAs):
        for j in range(self.num_channels_VCA):
            self.axarry[j, i].set_ylim(ylimits[i][j][0], ylimits[i][j][1])
            self.line[2*i+j], = self.axarry[j, i].plot(analogData[i].ax)
    plt.pause(0.00000001)

  # update plot
  def update(self, analogData):
    #~ print analogData.ax
    for i in range(self.num_channels):
        self.line[i].set_ydata(analogData[i].ax)
    plt.pause(0.00000001)
    #~ plt.draw()

# main() function
def main():
  voltage_per_bit = 5.0/(2**16)
  duty_per_bit = 1.0/256
  # strPort = '/dev/ttyUSB0'  # for linux platforms
  strPort = 'COM20'       # for windows platforms

  # plot parameters
  analogData = [AnalogData(200), AnalogData(200), AnalogData(200), AnalogData(200)] # two VCAs, each has two channels
  analogPlot = AnalogPlot(analogData, [[[0, 5],[-1, 1]], [[0,5],[-1,1]]])

  print 'plotting data...'

  # open serial port
  teensy = serial.Serial(strPort, 230400)
  count = 0
  while True:
    try:
      rawRead = teensy.readline().replace('\x00', '').replace('\r', '').replace('\n', '')
      #~ print "got one line"
      if len(rawRead) != 0:
        #~ print "add data"
        #~ print rawRead
        try:
            data = int(rawRead)
            if data > 1000:   ## point data is from 10k to 50k, from motor A
                position = MotorACalibration(data)
                if position > 0 and position < 5:
                    analogData[0].add([position])
            elif data > -260 and data < 260:
                duty = data*duty_per_bit                    ## duty data in from -256 to 256
                if duty > -1 and duty < 1:
                    analogData[1].add([duty])
            elif data < -1000:  # from motor B
                position = MotorBCalibration(-data)
                if position > 0 and position < 5:
                    analogData[2].add([position])
            else:
                duty = (data-600) * duty_per_bit
                if duty > -1 and duty < 1:
                    analogData[3].add([duty])
            count += 1
            if count % 100 == 0:    ## update plot every 100 data point
                analogPlot.update(analogData)
        except:
            print 'I2C error data'
    except KeyboardInterrupt:
      print 'exiting'
      break
  # close serial
  teensy.flush()
  teensy.close()

# call main
if __name__ == '__main__':
  main()
