from action import Action
from blocks import BLOCKS
import random
import copy
from config import BOARD_WIDTH, BOARD_AREA

def refreshBag():
    chosen=random.sample(BLOCKS, len(BLOCKS))
    return chosen[:3]


class GameStateData:
    """A gamestate contains:
    gameOver (BOOL) -- Is the game over?
    grid (2d binary array) -- stores the game map
    score (Int) -- stores the score of the game.

    Bag: the current one-three possible blocks to choose from.

    """
    def __init__(self, points=0):
        """
        Creates an initial game state.
        """
        self.grid=[[0]*9 for i in range(BOARD_WIDTH)]
        self.score=points
        self.gameOver=False
        self.bag=refreshBag()


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
        sucessor.score+=points # add clearnace points
        #sucessor.score+= len(zeroed_tiles) # add added points

        #remove peice from bag, refresh bag if needed.
        for item in self.bag:
            if piece == item:
                self.bag.remove(item)
        if len(self.bag)==0:
            self.bag=refreshBag()

        return sucessor

    def getLegalActions(self):
        actions=[]
        for p in self.bag:
            actions.append(Action.getPossibleActions(self.grid,p))

        return actions[0]
