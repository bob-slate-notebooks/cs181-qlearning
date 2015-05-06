import numpy as np
import numpy.random as npr
import sys

from SwingyMonkey import SwingyMonkey

class Learner:

    def __init__(self, nvars, nstates, alpha, gamma):
        # input
        self.nvars   = nvars
        self.nstates = nstates
        self.alpha   = alpha
        self.gamma   = gamma
        # new parameters
        self.last_state  = None
        self.last_action = None
        self.last_reward = None
        self.value       = np.zeros(tuple(nstates for i in range(nvars)))

    def reset(self):
        self.last_state  = None
        self.last_action = None
        self.last_reward = None

    def transform(self, state):
        if state is None:
            return None
        dist = state['tree']['dist']
        tree = (state['tree']['top'] + state['tree']['bot']) / 2
        monk = (state['monkey']['top'] + state['monkey']['bot']) / 2
        return (dist, tree, monk)

    def value(self, state):
        if state is None:
            return 0.0
        if state not in self.value:
            self.value[state] = 0.0
        return self.value[state]

    def delta(self, prev, reward, curr):
        return self.last_reward + (self.gamma * self.value(curr)) - self.value(prev)

    def action_callback(self, state):
        '''Implement this function to learn things and take actions.
        Return 0 if you don't want to jump and 1 if you do.'''

        prev = self.transform(self.last_state)
        curr = self.transform(state)
        self.last_state = curr

        if curr is None:
            return 0

        self.value += self.alpha * self.delta(prev, self.last_reward, curr)

    def reward_callback(self, reward):
        '''This gets called so you can see what reward you get.'''

        self.last_reward = reward

iters = 100
nvars = 3
nstates = 10
alpha = 0.2
gamma = 0.9
learner = Learner(nvars, nstates, alpha, gamma)

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



    
