# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.oldValues=util.Counter()
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        x=0
        while x < iterations:
            for state in mdp.getStates():
                if mdp.isTerminal(state):
                    self.values[state]=0
                else:
                    maxqval=-9999
                    bestaction=None
                    for action in self.mdp.getPossibleActions(state):
                        qval=self.computeQValueFromValues(state, action)
                        if qval>maxqval:
                            maxqval=qval
                            bestaction=action
                    self.values[state]=maxqval
            self.oldValues=self.values.copy()
            x += 1
                #print "state:",state, "action:",bestaction, "value:",self.values[state]
    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        if action==None:
            return 0
        qvalue=0.0
        for (TState, prob) in self.mdp.getTransitionStatesAndProbs(state, action):
            qvalue+=prob*(self.mdp.getReward(state, action, TState)+self.oldValues[TState]*self.discount)

        return qvalue
    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        actions=self.mdp.getPossibleActions(state)
        if not actions:
            return None
        bestAction=None
        maxReward=-9999
        for action in actions:
            reward=0
            transitionStatesAndProbs=self.mdp.getTransitionStatesAndProbs(state, action)
            for TState, prob in transitionStatesAndProbs:
                reward+=self.oldValues[TState]*prob
            if reward>=maxReward:
                maxReward=reward
                bestAction=action
        return bestAction

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
