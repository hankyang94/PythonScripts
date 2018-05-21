import numpy as np
import matplotlib
import matplotlib.pyplot as plt

filePath = "/Users/Hank/solver_output/"
fileName_traj_opt = "transform_sol_0mps_100mps_snopt_new_py.txt"
fileName_tvlqr_time = "TVLQR_log_time_0mps_100mps.txt"
fileName_tvlqr_control = "TVLQR_log_control_0mps_100mps.txt"
fileName_tvlqr_state = "TVLQR_log_state_0mps_100mps.txt"

# fileName_traj_opt = "transform_sol_100mps_0mps_snopt_new_py.txt"
# fileName_tvlqr_time = "TVLQR_log_time_100mps_0mps.txt"
# fileName_tvlqr_control = "TVLQR_log_control_100mps_0mps.txt"
# fileName_tvlqr_state = "TVLQR_log_state_100mps_0mps.txt"

########### Read trajectory optimization results ##########
file = open(filePath+fileName_traj_opt, 'r')
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

########## read tvlqr data ############
tvlqr_t = np.loadtxt(filePath+fileName_tvlqr_time)
tvlqr_u = np.loadtxt(filePath+fileName_tvlqr_control)
tvlqr_x = np.loadtxt(filePath+fileName_tvlqr_state)

tvlqr_t = np.delete(tvlqr_t, 0)
tvlqr_u = np.delete(tvlqr_u, 0, 1)
tvlqr_x = np.delete(tvlqr_x, 0, 1)

print tvlqr_t.shape
print tvlqr_u.shape
print tvlqr_x.shape


plt.rc('text', usetex=True)
plt.rc('font', family='serif')
# plot states
num_states = xData.shape[0]
fig1, axarry1 = plt.subplots(num_states, sharex=True, figsize=(5, 12), dpi=300)
x_states = [r'X[m]', r'Y[m]', r'Z[m]', r'$\phi$', r'$\theta$', r'$\psi$',
            r'$\dot{X}$[m/s]', r'$\dot{Y}$[m/s]', r'$\dot{Z}$[m/s]',
            r'$\dot{\phi}$[/s]', r'$\dot{\theta}$[/s]', r'$\dot{\psi}$[/s]']
for i in range(num_states):
    axarry1[i].plot(tData, xData[i, :], label='Trajectory Optimization')
    axarry1[i].plot(tvlqr_t, tvlqr_x[i, :], label='TVLQR')
    axarry1[i].legend()
    axarry1[i].set_ylabel(x_states[i])
axarry1[-1].set_xlabel(r'Time[s]')
fig1.subplots_adjust(hspace=0)
plt.setp([a.get_xticklabels() for a in fig1.axes[:-1]], visible=False)

# plot control inputs
num_inputs = uData.shape[0]
fig2, axarry2 = plt.subplots(num_inputs, sharex=True, figsize=(5, 8), dpi=300)
u_inputs = [r'$F_1[N]$', r'$F_2[N]$', r'$F_3[N]$', r'$F_4[N]$',
            r'$\theta_1$', r'$\theta_2$', r'$\theta_3$', r'$\theta_4$']
for i in range(num_inputs):
    axarry2[i].plot(tData, uData[i, :], label='Trajectory Optimization')
    axarry2[i].plot(tvlqr_t, tvlqr_u[i, :], label='TVLQR')
    axarry2[i].set_ylabel(u_inputs[i])
    axarry2[i].legend()
axarry2[-1].set_xlabel(r"Time[s]")
fig1.subplots_adjust(hspace=0)
plt.setp([a.get_xticklabels() for a in fig2.axes[:-1]], visible=False)
plt.show()
fig1.savefig('tvlqr_100mps_0mps_state.pdf')
fig2.savefig('tvlqr_100mps_0mps_control.pdf')