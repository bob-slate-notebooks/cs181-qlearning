import numpy as np
import numpy.random as npr
import sys

from SwingyMonkey import SwingyMonkey

class Learner:

    def __init__(self, nvars, nstates, alpha, gamma, epsil,  nacts = 2):
        self.nacts   = nacts
        self.nvars   = nvars
        self.nstates = nstates
        self.alpha   = alpha
        self.gamma   = gamma
        self.epsil   = epsil
        self.last_state  = 0, 0, 0
        self.last_action = 0
        self.last_reward = 0.0
        self.value       = np.zeros(tuple(nstates for i in range(nvars)))
        self.policy      = np.ones(tuple(nstates for i in range(nvars)), dtype = np.int)

    def reset(self):
        self.last_state  = 0, 0, 0
        self.last_action = 0
        self.last_reward = 0.0

    def new_state(self, state):
        dist = state['tree']['dist']
        dist = int((dist - (dist % 60))/60)
        monkey = state['monkey']['top']
        monkey = int((monkey - (monkey % 40))/40)
        gap = (state['tree']['top'] + state['tree']['bot']) / 2
        gap = int((gap - (gap % 40))/40)
        return (dist, monkey, gap)

    def value_model(self, curr, prev, reward, action):
        a, b, c = prev
        d, e, f = curr
        old = self.value[a][b][c]
        self.value[a][b][c] += self.alpha * (reward + self.gamma * self.value[d][e][f] - self.value[a][b][c])
        return old, self.value[a][b][c]

    def new_action(self, curr, prev, reward, action):
        old, new = self.value_model(curr, prev, reward, action)
        a,b,c = prev
        print old, new
        if old < new:
            self.policy[a][b][c] = action
        if npr.random() < self.epsil:
            self.epsil = self.epsil * 0.5
            if action == 0:
                return 1
            if action ==1:
                return 0

    def action_callback(self, state):
        
        new_state  = self.new_state(state)
        new_action = self.new_action(new_state, self.last_state, self.last_reward, self.last_action)

        self.last_state  = new_state
        self.last_action = new_action

        return self.last_action

    def reward_callback(self, reward):
        self.last_reward = reward

iters = 100
nvars = 3
nstates = 10
alpha = 0.2
gamma = 0.9
epsil = 0.1
learner = Learner(nvars, nstates, alpha, gamma, epsil)

for ii in xrange(iters):

    # Make a new monkey object.
    swing = SwingyMonkey(sound=False,            # Don't play sounds.
                         text="Epoch %d" % (ii), # Display the epoch on screen.
                         tick_length=1,          # Make game ticks super fast.
                         action_callback=learner.action_callback,
                         reward_callback=learner.reward_callback)

    # Loop until you hit something.
    while swing.game_loop():
        print swing.get_state()
        pass

    # Reset the state of the learner.
    learner.reset()
    
