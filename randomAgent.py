from game import GameState
import random

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

    def run(self, DEBUG=False):

        self.state=GameState()
        self.rounds=0
        lastReward = -50
        lastRating = 0

        if DEBUG:
            print("Begin Game")

        while not self.state.gameOver:


            actions = self.state.getLegalActions()
            ratings=[]

            if len(actions)==0:
                self.state.gameOver=True
            else:
                action = random.choice(actions)
                self.state = self.state.generateSuccessor(action)

                if DEBUG:
                    print("****  Resultant GRID ***")
                    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
      for row in self.state.grid]))
                    print("******")
            self.rounds+=1

        if DEBUG:
            print("End game on round", self.rounds)
        return self.rounds


def train_agent():
    iterations=10
    epochs=100

    g=Game()
    for iteration in range(0,iterations):
        results=[]
        for game in range(0,epochs):
            results.append(g.run())

        f = open("randomResults.csv", "a")
        f.write(str(iteration) + "," + str(sum(results)/len(results)) + "\n")
        f.close()
        print("Saved agent")


train_agent()
