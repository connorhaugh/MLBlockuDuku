from blocks import BLOCKS
import random

class Action:
    """An action is a vector of (4x4 array of piece, X,Y)
    where X and Y are the postions on the playing grid from which the top left
     corner of the pieces are drawn."""

    def refreshBag():
        chosen=random.sample(BLOCKS, len(BLOCKS))
        return chosen[:3]
    @staticmethod
    def getPossibleActions(grid,piece):
        """
        Determine the set of all possible x,y s such that you could place the top left corner at that point.
        Todo: Add width and height
        """
        actions =[]

        for r in range(0,len(grid)):
            for c in range(0,len(grid)):
                valid=True
                for pair in piece:
                    i,j= pair
                    if (r+i)>=0 and (c+j)>=0 and (r+i)<len(grid) and (c+j)<len(grid): # in bounds
                        if grid[r+i][c+j]==1: #already a piece there
                            valid=False
                    else:
                        valid=False
                if(valid):
                    actions.append((r,c,piece))

        return actions


    def clearIfFull(grid):
        """
        Clear any columns, rows, and boxes from the placement of a piece. Caluculate the points earned from that removal.
        Because a row and column can clear at the same time, preserve the grid till the end.
        """
        toclear=[]
        #Check Columns
        for c in range(0,len(grid)):
            for r in range(0,len(grid)):
                if grid[r][c]==0:
                    break
            else: # executes when loop exits normally, meaning all 1s
                toclear.append(('c',c,0))

        #check Rows
        for r in range(0,len(grid)):
            for c in range(0,len(grid)):
                if grid[r][c]==0:
                    break
            else: # executes when loop exits normally, meaning all 1s
                toclear.append(('r',r,0))

        #check squares

        box_width=len(grid)//3

        for i in range(0,len(grid)-box_width+1,box_width):#remeber range is not inclusive
            for j in range(0,len(grid)-box_width+1,box_width):
                #check in each box
                filled=True
                for a in range(0,box_width,1):
                    for b in range(0,box_width,1):
                        if grid[i+a][b+j]==0:
                            filled=False
                            break
                    else:
                        continue
                    break
                if(filled):
                    toclear.append(('b',i,j))

        #Tabulate Score and Clear
        points= len(grid) * len(toclear) * 2


        """ if points > 0:
            print("reward of:", points)
            print("*****CLEAR*****")
            print('\n'.join([''.join(['{:4}'.format(item) for item in row])
        for row in grid]))
            print("***************") """

        for clear in toclear:
            if clear[0]=='r':
                for c in range(0,len(grid)):
                    grid[clear[1]][c]=0
            elif clear[0]=='c':
                for r in range(0,len(grid)):
                    grid[r][clear[1]]=0
            elif clear[0]=='b':
                i=clear[1]
                j=clear[2]
                for a in range(0,box_width,1):
                    for b in range(0,box_width,1):
                        grid[i+a][b+j]=0
        return grid,points
