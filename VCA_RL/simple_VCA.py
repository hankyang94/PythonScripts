import numpy as np
import matplotlib.pyplot as plt

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

u_max = 5
f = 50.0
total_time = 1.0/f
dt = 0.001
time_array = np.arange(0, total_time+dt, dt)
state_initial = [0.0, 0.0]
# initial guess
input_trajectory = np.zeros_like(time_array)
input_trajectory[time_array < total_time/2.] = u_max
input_trajectory[time_array > total_time/2.] = -u_max
amplitude_goal = 0.005
states_goal = (- np.cos(2*np.pi*f*time_array) + 1)*amplitude_goal

simpleVCA = SimpleVoiceCoilActuator()

simulated_states = simpleVCA.simulate_states_over_time(state_initial, time_array, input_trajectory)

print len(time_array)
print len(input_trajectory)
print simulated_states.shape

fig0 = plt.figure()
fig0.add_subplot(211)
plt.plot(time_array, input_trajectory)
plt.xlabel("t")
plt.ylabel("u[V]")
plt.title("Original Control Policy")
fig0.add_subplot(212)
plt.plot(time_array, simulated_states[:, 0])
plt.plot(time_array, states_goal, 'r')
plt.xlabel("t")
plt.ylabel("q[m]")
plt.title("Original position trajectory")

plt.show()

previous_state_cost = np.linalg.norm(simulated_states[:, 0] - states_goal)**2
print "Cost: " + str(previous_state_cost)

mu = 0
sigma = 1.5
learning_rate = 1e1
iter = 0
while (previous_state_cost > 1e-5) and (iter < 100000):
    beta = np.random.normal(mu, sigma, input_trajectory.shape)
    input_trajectory_ptb = np.clip((input_trajectory + beta), -u_max, u_max)
    simulated_states = simpleVCA.simulate_states_over_time(state_initial, time_array, input_trajectory_ptb)
    # fig.add_subplot(211)
    # plt.plot(time_array, input_trajectory_ptb)
    # fig.add_subplot(212)
    # plt.plot(time_array, simulated_states[:, 0])
    # plt.plot(time_array, states_goal, 'r')
    # plt.show()

    current_state_cost = np.linalg.norm(simulated_states[:, 0] - states_goal) ** 2
    input_trajectory -= learning_rate/((1+iter) ** (0.01)) * (current_state_cost - previous_state_cost) * beta
    input_trajectory = np.clip(input_trajectory, -u_max, u_max)
    previous_state_cost = current_state_cost
    print str(iter) + " Cost: " + str(previous_state_cost)
    iter += 1

fig = plt.figure()
fig.add_subplot(211)
plt.plot(time_array, input_trajectory)
plt.xlabel("t")
plt.ylabel("u[V]")
plt.title("Learned Control Policy")
fig.add_subplot(212)
plt.plot(time_array, simulated_states[:, 0])
plt.plot(time_array, states_goal, 'r')
plt.xlabel("t")
plt.ylabel("q[m]")
plt.title("Learned position trajectory")
plt.show()
