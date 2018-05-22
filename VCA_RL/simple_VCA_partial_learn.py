import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class SimpleVoiceCoilActuator():
    def __init__(self):
        self.x_coef = -176
        self.u_coef = 93

    def vca_dynamics(self, state, u):
        q = state[0]
        q_dot = state[1]
        derivs = np.zeros_like(state)
        derivs[0] = q_dot
        derivs[1] = self.x_coef * q + self.u_coef * u

        return derivs

    def simulate_states_over_time(self, state_initial, time_array, input_trajectory):
        states_over_time = np.asarray([state_initial])
        for i in range(1, len(time_array)):
            time_step = time_array[i] - time_array[i-1]
            state_next = states_over_time[-1, :] + time_step * self.vca_dynamics(states_over_time[-1, :], input_trajectory[i-1])
            states_over_time = np.vstack((states_over_time, state_next))

        return states_over_time


u_max = 10
f = 50.0
total_time = 1.0/f/2
dt = 0.001
time_array = np.arange(0, total_time+dt, dt)
state_initial = [0.0, 0.0]
gamma = 1.0
discount = np.power(gamma, time_array*1000/2)
# initial guess
input_trajectory = np.zeros_like(time_array)
# input_trajectory[time_array < total_time/2.] = u_max
# input_trajectory[time_array > total_time/2.] = -u_max
amplitude_goal = 0.005
states_goal = (- np.cos(2*np.pi*f*time_array) + 1)*amplitude_goal

simpleVCA = SimpleVoiceCoilActuator()

simulated_states = simpleVCA.simulate_states_over_time(state_initial, time_array, input_trajectory)

print len(time_array)
print len(input_trajectory)
print simulated_states.shape

fig0, axarray0 = plt.subplots(2, sharex=True)
axarray0[0].plot(time_array*1000, input_trajectory)
axarray0[0].set_ylabel("Original u[V]")
axarray0[1].plot(time_array*1000, simulated_states[:, 0], label='Original q')
axarray0[1].plot(time_array*1000, states_goal, 'r', label='q goal')
axarray0[1].set_xlabel("t[ms]")
axarray0[1].set_ylabel("q[m]")
axarray0[0].set_title('Original policy')

error = discount*(simulated_states[:, 0] - states_goal)
previous_state_cost = np.linalg.norm(error)**2
print "Cost: " + str(previous_state_cost)


mu = 0
sigma = 0.05
learning_rate = 2e0
kappa = 0.5
tao = 1
iter_max = 1000
iter = 0

fig1, axarray1 = plt.subplots(2, sharex=True)
axarray1[0].set_title('Learned policy')
axarray1[0].set_ylabel('Perturbated u[V]')
axarray1[1].set_xlabel('t[ms]')
axarray1[1].set_ylabel('q[m]')
axarray1[0].set_ylim(-u_max, u_max)
line_u, = axarray1[0].plot([], [])
line_q, = axarray1[1].plot([], [], label='Learned q')
line_g, = axarray1[1].plot(time_array*1000, states_goal, 'r', label='q goal')
axarray1[1].legend()

fig2, ax2 = plt.subplots()
line_cost, = ax2.plot([], [], lw=3)
ax2.set_yscale('log')
ax2.set_ylim(1e-8, 1e-2)
ax2.set_xlim(0, iter_max)
ax2.set_title('Cost: Sigma = ' + str(sigma) + ', eta = ' + str(learning_rate))
ax2.set_xlabel('Iteration')
ax2.set_ylabel('Error')

iter_his = []
cost_his = []

while (previous_state_cost > 1e-8) and (iter < iter_max):
    beta = np.random.normal(mu, sigma, input_trajectory.shape)
    input_trajectory_ptb = np.clip((input_trajectory + beta), -u_max, u_max)
    simulated_states = simpleVCA.simulate_states_over_time(state_initial, time_array, input_trajectory_ptb)

    line_u.set_data(time_array*1000, input_trajectory_ptb)
    line_q.set_data(time_array*1000, simulated_states[:, 0])

    error = discount*(simulated_states[:, 0] - states_goal)
    current_state_cost = np.linalg.norm(error) ** 2
    input_trajectory -= learning_rate/((tao+iter/500) ** kappa) * np.sign(current_state_cost - previous_state_cost) * beta
    # input_trajectory -= learning_rate * (current_state_cost - previous_state_cost) * beta
    input_trajectory = np.clip(input_trajectory, -u_max, u_max)
    previous_state_cost = current_state_cost
    # print str(iter) + " Cost: " + str(previous_state_cost)
    iter += 1
    iter_his.append(iter)
    cost_his.append(previous_state_cost)
    line_cost.set_data(iter_his, cost_his)
    plt.pause(0.001)


plt.show()

