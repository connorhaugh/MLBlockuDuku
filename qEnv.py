from blocks import BLOCKS
from action import Action
from qAgent import QAgent
from gameStateData import GameStateData

class Game:

    """
    The Game manages the control flow, soliciting actions from agents.
    """

    def __init__( self, agent, startingIndex=0):
        # NEED TO GENERATE A STATE
        self.state= GameStateData()
        self.agent = agent

    def run(self, DEBUG=False):
        """
        Main control loop for game play.
        """
        agent=self.agent
        agent.registerInitialState(self.state)
        rounds=0

        self.state=GameStateData()
        for r in self.state.grid:
            for c in r:
                if c==1:
                    print("SOMETHING IS SUPER WRONG HERE")
                    print(self.state.grid)

        while not self.state.gameOver:
            if DEBUG:
                print("MOVE ROUND:", rounds)
            # Generate an observation of the state
            action = self.agent.chooseAction(self.state)
            if DEBUG:
                print("Chosen Action",action)
            if action == None:
                self.state.gameOver=True
            else:
                self.state = self.state.generateSuccessor(action)
                if DEBUG:
                    print("****  Resultant GRID ***")
                    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
      for row in self.state.grid]))
                    print("******")

            rounds+=1
        agent.final(self.state)
        if DEBUG:
            print(self.state.score)

        return rounds



def train_agent():
    iterations=90
    epochs=100
    agent=QAgent(1)
    for iteration in range(0,iterations):
        results=[]
        for game in range(0,epochs):
            g=Game(agent)
            results.append(g.run())

        f = open("qResults.csv", "a")
        f.write(str(iteration) + "," + str(sum(results)/len(results)) + "\n")
        f.close()
        print("Saved agent")

def play_q_agent():
    agent=QAgent(1)
    g=Game(agent)
    g.run(True)
