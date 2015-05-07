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
        self.times = 0
        self.epsilon = 0.9
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
            self.Q_arr[(state, action)]= -5
            # initialize q values to negative values, this helped constant jumping
            return -5

    def set_q(self, state, action, q):
        state_tuple = self.convert_state(state)
        self.Q_arr[(state_tuple, action)] = q


    def convert_state(self, state):
        if state:
            monkey_gap = state["monkey"]["top"] - state["tree"]["bot"]
            if monkey_gap < 100:
                monkey_gap = 100
            elif monkey_gap < 300:
                monkey_gap = 200
            elif monkey_gap < 500:
                monkey_gap = 400
            else:
                monkey_gap = 500


            tree_far = state["tree"]["dist"]
            if tree_far < 100:
                tree_far = 100
            elif tree_far < 300:
                tree_far = 200
            elif tree_far < 500:
                tree_far = 400

            else:
                tree_far = 500

            return (monkey_gap, tree_far)

        else:
            return (0,0,0)

    def action_callback(self, state):

        old_q = self.get_q(self.convert_state(self.last_state), self.last_action)
        if self.get_q(self.convert_state(state), 1)> self.get_q(self.convert_state(state), 0):
            act = 1
            act_q = self.get_q(self.convert_state(state), 1)
        else:
            act = 0
            act_q = self.get_q(self.convert_state(state), 0)
        if self.last_reward:
            reward = self.last_reward
        else:
            # only run on the first ever entry when reward is None
            reward = 0

        # epsilon greedy
        if npr.random() < self.epsilon:
            act = npr.randint(0, 1)
            self.epsilon = self.epsilon * 0.5


        # actual q updating
        new_q = old_q + alpha * ((reward +  act_q* gamma )- old_q)
        if self.last_action == None:
            self.last_action = 0
        self.set_q(self.last_state, self.last_action, new_q)

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



    
