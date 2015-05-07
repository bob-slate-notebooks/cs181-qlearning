import numpy as np
import numpy.random as npr
import sys

from SwingyMonkey import SwingyMonkey
from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection

class Learner:

    def __init__(self, network, epsilon, alpha, gamma):
        self.last_state  = None
        self.last_action = None
        self.last_reward = None

        # initializations for Q-Learning
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.actions = [0, 1]
        self.Q = {}
        self.network = network

    def reset(self):
        self.last_state  = None
        self.last_action = None
        self.last_reward = None

    def update_Q(self, network, state, action, reward):
        self.network = network

    def action_callback(self, state):
        '''Implement this function to learn things and take actions.
        Return 0 if you don't want to jump and 1 if you do.'''

        # exploration vs exploitation loop
        if npr.random() < self.epsilon:
            new_action = npr.random_integers(0, 1)
        else:
            # call q value using neural network
            q_array = self.network.activate([state['monkey']['top'], state['monkey']['bot'],
                state['monkey']['vel'], state['tree']['dist'], state['tree']['top'],
                state['tree']['bot']])
            max_q = max(q_array)
            count = (q_array == max_q).sum()
            if count > 1:
                best = [i for i in range(len(self.actions)) if q_array[i] == max_q]
                i = npr.choice(best)
            else:
                ind = np.where(q_array == max_q)
                i = int(ind[0])
            new_action = self.actions[i]
        
        new_state = state
        self.last_action = new_action
        self.last_state  = new_state

        # update neural network using q value
        self.update_Q(self.network, new_state, new_action, self.reward_callback)
        return self.last_action

    def reward_callback(self, reward):
        '''This gets called so you can see what reward you get.'''
        print reward
        self.last_reward = reward

# initalize parameters
iters = 100
epsilon = 0.1
alpha = 0.2
gamma = 0.9

# setup neural network
network = FeedForwardNetwork()

inLayer = LinearLayer(6)
hiddenLayer = SigmoidLayer(3)
outLayer = LinearLayer(2)

network.addInputModule(inLayer)
network.addModule(hiddenLayer)
network.addOutputModule(outLayer)

in_to_hidden = FullConnection(inLayer, hiddenLayer)
hidden_to_out = FullConnection(hiddenLayer, outLayer)
network.addConnection(in_to_hidden)
network.addConnection(hidden_to_out)

network.sortModules()

learner = Learner(network, epsilon, alpha, gamma)

for ii in xrange(iters):

    # Make a new monkey object.
    swing = SwingyMonkey(sound=False,            # Don't play sounds.
                         text="Epoch %d" % (ii), # Display the epoch on screen.
                         tick_length=1,          # Make game ticks super fast.
                         action_callback=learner.action_callback,
                         reward_callback=learner.reward_callback)

    # Loop until you hit something.
    while swing.game_loop():
        pass

    # Reset the state of the learner.
    learner.reset()



    
