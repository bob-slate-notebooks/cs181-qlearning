import numpy.random as npr
import sys

from SwingyMonkey import SwingyMonkey

alpha = 0.5
gamma = 0.5

class Learner:

    def __init__(self):
        self.last_state  = None
        self.last_action = None
        self.last_reward = None
        self.Q_arr = {}

    def reset(self):
        self.last_state  = None
        self.last_action = None
        self.last_reward = None


    def get_q(self, state, action):
        if (state, action) in self.Q_arr:
            return self.Q_arr[(state, action)]
        else:
            if action == None:
                action = 0
            self.Q_arr[(state, action)]= 0
            return 0

    def set_q(self, state, action, q):
        state_tuple = self.convert_state(state)
        self.Q_arr[(state_tuple, action)] = q
        #print self.Q_arr


    def convert_state(self, state):
        if state:
            vel = state["monkey"]["vel"]
            if vel < 0:
                vel = -10
            elif vel < 50:
                vel = 30
            else:
                vel = 80

            gap = state["tree"]["top"] - state["tree"]["bot"]
            if gap < 100:
                gap = 100
            elif gap < 300:
                gap = 200
            elif gap < 500:
                gap = 400
            else:
                gap = 500


            tree_far = state["tree"]["dist"]
            if tree_far < 100:
                tree_far = 100
            elif tree_far < 300:
                tree_far = 200
            elif tree_far < 500:
                tree_far = 400
            else:
                tree_far = 500

            return (vel, gap, tree_far)

        else:
            return (0,0,0)

    def action_callback(self, state):
        old_q = self.get_q(self.convert_state(self.last_state), self.last_action)
        if self.get_q(self.convert_state(state), 1)> self.get_q(self.convert_state(state), 0):
            act = 1
        else:
            act = 0
        if self.last_reward:
            reward = self.last_reward
        else:
            reward = 0

        new_q = old_q + alpha * (reward + act * gamma - old_q)
        if self.last_action == None:
            self.last_action = 0
        self.set_q(state, self.last_action, new_q)
        print state, act

        new_action = act
        new_state  = state

        self.last_action = new_action
        self.last_state  = new_state

        return self.last_action

    def reward_callback(self, reward):
        '''This gets called so you can see what reward you get.'''

        self.last_reward = reward

iters = 100
learner = Learner()

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



    
