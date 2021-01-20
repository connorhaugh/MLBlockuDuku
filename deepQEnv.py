from action import Action
from deepQAgent import QAgent
from operator import itemgetter
from blocks import BLOCKS
import copy
from util import Observation
import pickle
from config import BOARD_WIDTH,BOARD_AREA
import collections

class GameState:

    def __init__(self):
        self.grid=[[0]*BOARD_WIDTH for i in range(BOARD_WIDTH)]
        self.score=0
        self.reward=0
        self.gameOver=False
        self.rounds=0
        self.bag=Action.refreshBag()

    def generateSuccessor(self,action):

        """
        Generates a new configuration of the sate reached by translating the current
        configuration by the action vector. Note this is a low-level operation which does not respect legality
        """
        current = self
        sucessor = copy.deepcopy(current)
        x,y,piece = action

        #apply action
        zeroed_tiles= piece
        for item in zeroed_tiles:
            a,b=item
            sucessor.grid[x+a][y+b]=1

        #clear points on the grid if full
        sucessor.grid,points = Action.clearIfFull(sucessor.grid)
        sucessor.reward=points # add clearnace points
        sucessor.reward+= len(zeroed_tiles) # add added points
        sucessor.score+=sucessor.reward

        #remove peice from bag, refresh bag if needed.
        for item in self.bag:
            if collections.Counter(item) == collections.Counter(piece):
                sucessor.bag.remove(item)
        if len(sucessor.bag)==0:
            sucessor.bag=Action.refreshBag()

        return sucessor

    def getLegalActions(self):
        actions=[]
        for p in self.bag:
            actions.append(Action.getPossibleActions(self.grid,p))
        return actions[0]

class Game:

    """The game. Instead of asking the Q agent to perform the task
    "What is the best action to take at this step given my current state?"
    instead ask
    "What is the rating for this new board, which comes from the old board and this legal action?"
    and then take the best-rated action, where ratings are from 0-10.
    That way, the network doesn't have to deal with the larger state space of (board,piece) pairs or provide complex actions.
    """
    def __init__(self):
        self.state=GameState()
        self.agent = QAgent(BOARD_AREA,100)
        self.rounds=0

    def test(grid, action):
        newgrid = copy.deepcopy(grid)
        x,y,piece = action

        zeroed_tiles= piece
        for item in zeroed_tiles:
            a,b=item
            newgrid[x+a][y+b]=1
        newgrid,points = Action.clearIfFull(newgrid)

        return newgrid

    def save(self):
        object = self.agent
        filehandler = open('agent.ml', 'wb')
        pickle.dump(object, filehandler)

    def run(self, DEBUG=False, training= True):

        self.state=GameState()
        self.rounds=0
        lastReward = -50
        lastRating = 0

        if DEBUG:
            print("Begin Game")


        if not training:
            self.movesList =[]

        while not self.state.gameOver:
            actions = self.state.getLegalActions()
            ratings=[]

            if len(actions)==0:
                self.state.gameOver=True
            else:
                for action in actions:
                    board = Game.test(self.state.grid,action)
                    observation = Observation(self.state.grid,board,lastRating,lastReward)
                    rate = self.agent.step(observation,training)
                    ratings.append((action,rate))

                bestaction = max(ratings,key=itemgetter(1))
                lastRating = bestaction[1]
                self.state = self.state.generateSuccessor(bestaction[0])
                lastReward = self.state.reward + self.rounds

                if DEBUG:
                    print("****  Resultant GRID ***")
                    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
      for row in self.state.grid]))
                    print("******")

                if not training:
                    self.movesList.append(self.state.grid)

            self.rounds+=1

        if DEBUG:
            print("End game on round", self.rounds)
        return self.rounds

def train_agent():
    iterations=1000
    epochs=100
    g=Game()
    for iteration in range(0,iterations):
        results=[]
        for game in range(0,epochs):
            results.append(g.run())

        f = open("deepQresults.csv", "a")
        f.write(str(iteration) + "," + str(sum(results)/len(results)) + "\n")
        f.close()
        g.save()
        print("Saved agent")

def play_agent():
    g = Game()
    pickle_off = open("agent.ml","rb")
    g.agent = pickle.load(pickle_off)
    print("Game Over. Score:", g.state.score)
    g.run(False,False)
    return g.movesList
