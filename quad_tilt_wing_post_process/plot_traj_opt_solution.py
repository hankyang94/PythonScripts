import numpy as np
import matplotlib
import matplotlib.pyplot as plt


filePath = "/Users/Hank/Dropbox (MIT)/Courses/6.832 Underactuated Robotics/Final Project/code/solver_output/"
fileName = "traj_opt_sol_100mps_py_speedlimit.txt"

file = open(filePath+fileName, 'r')
rawData = file.readlines()
file.close()

for i in range(0, len(rawData)):
    if rawData[i][0] == 't':
        tIndex = i
    if rawData[i][0] == 'u':
        uIndex = i
    if rawData[i][0] == 'x':
        xIndex = i

tData = rawData[(tIndex+1):uIndex]
uData = rawData[(uIndex+1):xIndex]
xData = rawData[(xIndex+1):]

for i in range(len(tData)):
    tData[i] = float(tData[i].rstrip())
for i in range(len(uData)):
    uData[i] = uData[i].rstrip().split()
    for j in range(len(uData[i])):
        uData[i][j] = float(uData[i][j])
for i in range(len(xData)):
    xData[i] = xData[i].rstrip().split()
    for j in range(len(xData[i])):
        xData[i][j] = float(xData[i][j])
tData = np.asarray(tData)
uData = np.asarray(uData)
xData = np.asarray(xData)

print tData.shape
print uData.shape
print xData.shape

# plot states of trajectory optimization
num_states = xData.shape[0]
fig1 = plt.figure(1, figsize=(5, 20))
x_states = ["x[m]", "y[m]", "z[m]", "phi", "theta", "psi",
            "x_dot[m/s]", "y_dot[m/s]", "z_dot[m/s]",
            "phi_dot[/s]", "theta_dot[/s]", "psi_dot[/s]"]
for i in range(num_states):
    fig1.add_subplot(num_states, 1, i+1)
    plt.plot(tData, xData[i, :])
    plt.xlabel(r"Time[s]")
    plt.ylabel(x_states[i])

# plot inputs of trajectory optimization
num_inputs = uData.shape[0]
fig2 = plt.figure(2, figsize=(5, 15))
u_inputs = ["omega1^2", "omega2^2", "omega3^2", "omega4^2",
            "theta_1", "theta_2", "theta_3", "theta_4"]
for i in range(num_inputs):
    fig2.add_subplot(num_inputs, 1, i+1)
    plt.plot(tData, uData[i, :])
    plt.xlabel(r"Time[s]")
    plt.ylabel(u_inputs[i])

plt.show()

