import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


filePath = "/Users/Hank/solver_output/"
fileName = "traj_opt_sol_snopt_infinity_10mps_py.txt"

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

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# plot states of trajectory optimization
num_states = xData.shape[0]
fig1, axarry1 = plt.subplots(num_states, sharex=True, figsize=(5, 12), dpi=300)
x_states = [r'X[m]', r'Y[m]', r'Z[m]', r'$\phi$', r'$\theta$', r'$\psi$',
            r'$\dot{X}$[m/s]', r'$\dot{Y}$[m/s]', r'$\dot{Z}$[m/s]',
            r'$\dot{\phi}$[/s]', r'$\dot{\theta}$[/s]', r'$\dot{\psi}$[/s]']
for i in range(num_states):
    axarry1[i].plot(tData, xData[i, :])
    axarry1[i].set_ylabel(x_states[i])
axarry1[-1].set_xlabel(r'Time[s]')
fig1.subplots_adjust(hspace=0)
plt.setp([a.get_xticklabels() for a in fig1.axes[:-1]], visible=False)
# plot inputs of trajectory optimization
num_inputs = uData.shape[0]
fig2, axarry2 = plt.subplots(num_inputs, sharex=True, figsize=(5, 12), dpi=300)
u_inputs = [r'$F_1[N]$', r'$F_2[N]$', r'$F_3[N]$', r'$F_4[N]$',
            r'$\theta_1$', r'$\theta_2$', r'$\theta_3$', r'$\theta_4$']
for i in range(num_inputs):
    axarry2[i].plot(tData, uData[i, :])
    axarry2[i].set_ylabel(u_inputs[i])
axarry2[-1].set_xlabel(r'Time[s]')
fig2.subplots_adjust(hspace=0)
plt.setp([a.get_xticklabels() for a in fig2.axes[:-1]], visible=False)

fig3 = plt.figure(figsize=(5, 3), dpi=300)
ax = fig3.gca(projection='3d')
ax.plot(xData[0], xData[1], xData[2])
ax.set_zlim(0, 20)
ax.set_xlabel(r'X[m]')
ax.set_ylabel(r'Y[m]')
ax.set_zlabel(r'Z')

fig1.savefig('infinity_state.pdf')
fig2.savefig('infinity_control.pdf')
fig3.savefig('infinity_xyz.pdf')

plt.show()


