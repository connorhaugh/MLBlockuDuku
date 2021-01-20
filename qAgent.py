import random, time, util
from action import Action
import itertools
import copy
from util import nearestPoint
from gameStateData import GameStateData


class Agent:
    """
    An agent must define a getAction method, but may also define the
    following methods which will be called if they exist:
    def registerInitialState(self, state): # inspects the starting state
    """
    def __init__(self, index=0):
        self.index = index

    def getAction(self, gameState):
        """
        The Agent will receive a GameState and
        must return an action
        """

class RAgent(Agent):
  """
  A base class for reflex agents that chooses score-maximizing actions
  """

  def registerInitialState(self, gameState):
      return

  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    """
    actions = gameState.getLegalActions()
    if len(actions)==0:
        return None

    values = [self.evaluate(gameState, a) for a in actions]


    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]
    return random.choice(bestActions)

  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a gameState.
    """
    #print("getSuccessor")
    return  gameState.generateSuccessor(action)

  def evaluate(self, gameState, action):
    """
    Computes a linear combination of features and feature weights
    """
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    return features * weights
  def final(self,state):
     return

  def getFeatures(self, gameState, action):
    """
    Returns a counter of features for the state
    """
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = successor.score
    return features

  def getWeights(self, gameState, action):
    """
    Normally, weights do not depend on the gamestate.  They can be either
    a counter or a dictionary.
    """
    return {'successorScore': 1.0}


class QAgent(RAgent):
    """
    A reflex agent that seeks wins. The agent acts based on its extensive training (using q learning).
    """
    def registerInitialState(self, gameState):
        ## Percept Learning stuff
        ## Q learning stuff- rates taken from project 3
        self.counter=0
        self.explorationRate = 0.1#Epsilon
        self.learningRate = 0.05# Alpha
        self.discountRate =0.9
        self.weights= {'opensquares':1.0,'score':1.0,'nextblocksize':1.0, 'holes':1.0}

        # read from a file the wieghts

        try:
            with open('qlearndata.txt', "r") as file:
                self.weights =eval(file.read())
        except IOError:
            return


    def getQValue(self, gameState, action):
        """
        Returns Q(state,action)
        Should return 0.0 if we have never seen a state
        """
        #print("getQValue")
        features= self.getFeatures(gameState,action)
        return features * self.weights


    def computeValueFromQValues(self, gameState):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """

        #print("COMPUTE Value FROM Q VALUES")
        qValuesList=[]
        legalActions=gameState.getLegalActions()
        if(len(legalActions)==0):
            return 0.0
        for action in legalActions:
            qValuesList.append(self.getQValue(gameState,action))
        return max(qValuesList)


    def computeActionFromQValues(self, gameState,legalActions):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """

        #print("COMPUTE ACTION FROM Q VALUES")
        #Compute HighestAction, tiebreak randomly, remove STOP
        #print(legalActions)
        hiQ=float("-inf")
        highaction=[]
        if len(legalActions) == 0:
            return None

        for action in legalActions:
            presentq=self.getQValue(gameState,action)
            #update the wieghts at this step-- note that it updates at a lot of states it never even uses
            self.update(gameState,action)
            #print('Q is: '+ str(presentq))
            if(presentq>hiQ):
                highaction=[action]
                hiQ=presentq
            if(presentq==hiQ):
                highaction.append(action)

        return random.choice(highaction)


    def flipCoin( p ):
        r = random.random()
        return r < p

    def chooseAction(self, gameState):

        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.
          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action

        #print("CHOOSE ACTION")
        legalActions = gameState.getLegalActions()
        action = None
        "*** YOUR CODE HERE ***"
        if(len(legalActions)<1):
            return None
        #Flip a coin with probability epsilon, do some random action if it comes up true
        if(util.flipCoin(self.explorationRate)):
            #print('random')
            return random.choice(legalActions)
        #else return the action with the highest q value

        choiceaction =self.computeActionFromQValues(gameState,legalActions)
        return choiceaction

    def update(self, gameState, action):
        """
          Update the weights based on the features, using the following formula:
          #Q(s,a)= Q(s,a) + alpha(R(S) + gamma(max(Q(s',a') - Q(s,a))))
        """
        "*** YOUR CODE HERE ***"
        #Update function:
        #Q(s,a)= Q(s,a) + alpha(R(S) + gamma(max(Q(s',a') - Q(s,a))))

        # Locals: reward function, next state

        self.counter+=1

        nextState= self.getSuccessor(gameState,action)
        reward= nextState.score-gameState.score
        features = self.getFeatures(gameState,action)

        #print(action)
        #print(features)

        for feature in features:
            correction = (reward + self.discountRate*self.computeValueFromQValues(nextState)) - self.getQValue(gameState, action)
            self.weights[feature] = self.weights[feature] + self.learningRate*correction * features[feature]


    def getFeatures(self, gameState, action):
        features=util.Counter()
        #print("getFeatures")
        successor = self.getSuccessor(gameState, action)
        features["score"]=gameState.score

        blanks=0


        for row in successor.grid:
            for tile in row:
                if tile == 0:
                    blanks=blanks+1
        features["opensquares"]=blanks


        holes=0
        features["holes"]= holes
        size=0
        for  nextBlock in successor.bag:
            size=size+len(nextBlock)


        features["nextblocksize"]=size
        #print(features)
        features.divideAll(10.0)
        return features

    def getWeights(self, gameState, action):
        return self.weights

    def final(self,gameState):
        self.observationHistory = []
        finalwieghts= self.weights
        file=open('qlearndata.txt','w')
        file.write(str(self.weights))
