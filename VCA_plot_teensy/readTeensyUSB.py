import sys, serial
import numpy as np
from time import sleep
from collections import deque
from matplotlib import pyplot as plt

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
    self.num_channels = len(analogData)
    print "plot init"
    plt.ion()
    self.fig, self.axarry = plt.subplots(self.num_channels, sharex = True)
    self.line = [None] * self.num_channels
    for i in range(self.num_channels):
        self.line[i], = self.axarry[i].plot(analogData[i].ax)
        self.axarry[i].set_ylim(ylimits[i][0], ylimits[i][1])
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
  strPort = '/dev/ttyUSB0'

  # plot parameters
  analogData = [AnalogData(200), AnalogData(200)]
  analogPlot = AnalogPlot(analogData, [[0, 5],[-1, 1]])

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
            if data > 1000:   ## point data is from 10k to 50k
                voltage = data*voltage_per_bit
                if voltage > 0 and voltage < 5:
                    analogData[0].add([voltage])
            else:
                duty = data*duty_per_bit                    ## duty data in from -256 to 256
                if duty > -1 and duty < 1:
                    analogData[1].add([duty])
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
