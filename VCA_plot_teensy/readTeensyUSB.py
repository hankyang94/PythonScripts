import sys, serial
import numpy as np
from time import sleep
from collections import deque
from matplotlib import pyplot as plt

# class that holds analog data for N samples
class AnalogData:
  # constr
  def __init__(self, maxLen):
    self.ax = deque([0]*maxLen)
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
  strPort = '/dev/ttyUSB0'

  # plot parameters
  analogData = [AnalogData(200), AnalogData(200)]
  analogPlot = AnalogPlot(analogData, [[10000, 50000],[-256, 256]])

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
        if int(rawRead) > 1000:   ## point data is from 10k to 50k
            analogData[0].add([int(rawRead)])
        else:                    ## duty data in from -256 to 256
            analogData[1].add([int(rawRead)])
        count += 1
        if count % 100 == 0:    ## update plot every 100 data point
            analogPlot.update(analogData)
    except KeyboardInterrupt:
      print 'exiting'
      break
  # close serial
  teensy.flush()
  teensy.close()

# call main
if __name__ == '__main__':
  main()
