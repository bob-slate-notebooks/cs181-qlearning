import numpy.random as npr
import sys

from SwingyMonkey import SwingyMonkey

class Learner:

    def __init__(self, epsilon, alpha, gamma):
        self.last_state  = None
        self.last_action = None
        self.last_reward = None

        # initializations for Q-Learning
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.actions = [0, 1]
        self.Q = {}

    def reset(self):
        self.last_state  = None
        self.last_action = None
        self.last_reward = None

    def update_Q(self, state, action, reward):
        self.last_reward = reward

    def action_callback(self, state):
        '''Implement this function to learn things and take actions.
        Return 0 if you don't want to jump and 1 if you do.'''

        # exploration vs exploitation loop
        if npr.random() < self.epsilon:
            new_action = npr.rand() < 0.1
        else:
            # for a in self.actions:
            #     if (state, a) not in self.Q:
            #         self.Q[(state, a)] = 0
            #     q_array += [self.Q[(state, a)]]
            q_array = [2, 1]
            max_q = max(q_array)
            count = q_array.count(max_q)
            if count > 1:
                best = [i for i in range(len(self.actions)) if q_array[i] == maxQ]
                i = npr.choice(best)
            else:
                i = q_array.index(max_q)
            new_action = self.actions[i]
        
        new_state = state
        self.last_action = new_action
        self.last_state  = new_state

        self.update_Q(new_state, new_action, self.reward_callback)

        return self.last_action

    def reward_callback(self, reward):
        '''This gets called so you can see what reward you get.'''

        self.last_reward = reward

iters = 100
epsilon = 0.1
alpha = 0.2
gamma = 0.9
learner = Learner(epsilon, alpha, gamma)

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



    
