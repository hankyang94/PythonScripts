import numpy as np
import matplotlib
import matplotlib.pyplot as plt

filePath = "/Users/Hank/solver_output/"

fileName_lqr_time = "lqr_trim_100mps_log_time.txt"
fileName_lqr_control = "lqr_trim_100mps_log_control.txt"
fileName_lqr_state = "lqr_trim_100mps_log_state.txt"

lqr_t = np.loadtxt(filePath+fileName_lqr_time)
lqr_u = np.loadtxt(filePath+fileName_lqr_control)
lqr_x = np.loadtxt(filePath+fileName_lqr_state)

lqr_t = np.delete(lqr_t, 0)
lqr_u = np.delete(lqr_u, 0, 1)
lqr_x = np.delete(lqr_x, 0, 1)

lqr_u = lqr_u[:, lqr_t < 5]
lqr_x = lqr_x[:, lqr_t < 5]
lqr_t = lqr_t[lqr_t < 5]

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# plot states
num_states = lqr_x.shape[0]
fig1, axarry1 = plt.subplots(num_states, sharex=True, figsize=(5, 12), dpi=300)
x_states = [r'X[m]', r'Y[m]', r'Z[m]', r'$\phi$', r'$\theta$', r'$\psi$',
            r'$\dot{X}$[m/s]', r'$\dot{Y}$[m/s]', r'$\dot{Z}$[m/s]',
            r'$\dot{\phi}$[/s]', r'$\dot{\theta}$[/s]', r'$\dot{\psi}$[/s]']
x_goal = [0,0,1,0,0,0,0,0,0,0,0,0]
for i in range(num_states):
    axarry1[i].plot(lqr_t, lqr_x[i, :])
    axarry1[i].set_ylabel(x_states[i])
axarry1[-1].set_xlabel(r'Time[s]')
fig1.subplots_adjust(hspace=0)
plt.setp([a.get_xticklabels() for a in fig1.axes[:-1]], visible=False)

# plot control inputs
num_inputs = lqr_u.shape[0]
fig2, axarry2 = plt.subplots(num_inputs, sharex=True, figsize=(5, 12), dpi=300)
u_inputs = [r'$F_1[N]$', r'$F_2[N]$', r'$F_3[N]$', r'$F_4[N]$',
            r'$\theta_1$', r'$\theta_2$', r'$\theta_3$', r'$\theta_4$']
for i in range(num_inputs):
    axarry2[i].plot(lqr_t, lqr_u[i, :])
    axarry2[i].set_ylabel(u_inputs[i])
axarry2[-1].set_xlabel(r"Time[s]")
fig1.subplots_adjust(hspace=0)
plt.setp([a.get_xticklabels() for a in fig2.axes[:-1]], visible=False)
plt.show()
fig1.savefig('lqr_trim_state.pdf')
fig2.savefig('lqr_trim_control.pdf')
