import time
import turtle


# To get the colors for Turtle's Function as I have just saved characters in the 2-D array
def getcolor(str):
    if str == 'R' or str == 'r':
        return 'red'
    elif str == 'W' or str == 'w':
        return 'white'
    elif str == 'B' or str == 'b':
        return 'blue'
    elif str == 'G' or str == 'g':
        return 'green'
    elif str == 'O' or str == 'o':
        return 'orange'
    elif str == 'Y' or str == 'y':
        return 'yellow'


# Class to Maintain the State of a Cube and the Different Successor Functions that can be called on it
class RubikCube:
    def __init__(self, cube=None): # It acts as Both the Deafault and copyConstructor
        if cube is None:
            self.side_f = [['G', 'G', 'G'], ['G', 'G', 'G'], ['G', 'G', 'G']]
            self.side_b = [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']]
            self.side_l = [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']]
            self.side_r = [['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R']]
            self.side_u = [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']]
            self.side_d = [['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']]
        else:
            self.side_f = [[], [], []]
            self.side_b = [[], [], []]
            self.side_l = [[], [], []]
            self.side_r = [[], [], []]
            self.side_u = [[], [], []]
            self.side_d = [[], [], []]
            for i in range(0, 3):
                for j in range(0, 3):
                    self.side_f[i].append(cube.side_f[i][j])
                    self.side_b[i].append(cube.side_b[i][j])
                    self.side_l[i].append(cube.side_l[i][j])
                    self.side_r[i].append(cube.side_r[i][j])
                    self.side_u[i].append(cube.side_u[i][j])
                    self.side_d[i].append(cube.side_d[i][j])

    # All the 6 Successor Functions are below
    def facec(self):
        c = RubikCube(self)
        for i in range(0, 3):
            for j, k in zip(range(0, 3), range(2, -1, -1)):
                c.side_f[i][j] = self.side_f[k][i]

        for i in range(0, 3):
            c.side_r[2][i] = self.side_u[2][i]
        for i in range(0, 3):
            c.side_d[2][i] = self.side_r[2][i]
        for i in range(0, 3):
            c.side_l[2][i] = self.side_d[2][i]
        for i in range(0, 3):
            c.side_u[2][i] = self.side_l[2][i]

        return c

    def backc(self):
        c = RubikCube(self)
        for i in range(0, 3):
            for j, k in zip(range(0, 3), range(2, -1, -1)):
                c.side_b[i][j] = self.side_b[k][i]

        for i in range(0, 3):
            c.side_l[0][i] = self.side_u[0][i]
        for i in range(0, 3):
            c.side_d[0][i] = self.side_l[0][i]
        for i in range(0, 3):
            c.side_r[0][i] = self.side_d[0][i]
        for i in range(0, 3):
            c.side_u[0][i] = self.side_r[0][i]

        return c

    def rightc(self):
        c = RubikCube(self)
        for i in range(0, 3):
            for j, k in zip(range(0, 3), range(2, -1, -1)):
                c.side_r[i][j] = self.side_r[k][i]

        for i in range(0, 3):
            c.side_u[i][2] = self.side_f[i][2]
        for i, j in zip(range(0, 3), range(2, -1, -1)):
            c.side_b[i][0] = self.side_u[j][2]
        for i in range(0, 3):
            c.side_d[i][0] = self.side_b[i][0]
        for i, j in zip(range(0, 3), range(2, -1, -1)):
            c.side_f[i][2] = self.side_d[j][0]

        return c

    def leftc(self):
        c = RubikCube(self)
        for i in range(0, 3):
            for j, k in zip(range(0, 3), range(2, -1, -1)):
                c.side_l[i][j] = self.side_l[k][i]

        for i, j in zip(range(0, 3), range(2, -1, -1)):
            c.side_u[i][0] = self.side_b[j][2]
        for i in range(0, 3):
            c.side_b[i][2] = self.side_d[i][2]
        for i, j in zip(range(0, 3), range(2, -1, -1)):
            c.side_d[j][2] = self.side_f[i][0]
        for i in range(0, 3):
            c.side_f[i][0] = self.side_u[i][0]

        return c

    def upc(self):
        c = RubikCube(self)
        for i in range(0, 3):
            for j, k in zip(range(0, 3), range(2, -1, -1)):
                c.side_u[i][j] = self.side_u[k][i]

        for i in range(0, 3):
            c.side_l[i][2] = self.side_f[0][i]
        for i in range(0, 3):
            c.side_b[0][i] = self.side_l[i][2]
        for i, j in zip(range(0, 3), range(2, -1, -1)):
            c.side_r[j][0] = self.side_b[0][i]
        for i, j in zip(range(0, 3), range(2, -1, -1)):
            c.side_f[0][i] = self.side_r[j][0]
        return c

    def downc(self):
        c = RubikCube(self)
        for i in range(0, 3):
            for j, k in zip(range(0, 3), range(2, -1, -1)):
                c.side_d[i][j] = self.side_d[k][i]

        for i in range(0, 3):
            c.side_l[i][0] = self.side_b[2][i]
        for i in range(0, 3):
            c.side_f[2][i] = self.side_l[i][0]
        for i, j in zip(range(0, 3), range(2, -1, -1)):
            c.side_b[2][i] = self.side_r[j][2]
        for i, j in zip(range(0, 3), range(2, -1, -1)):
            c.side_r[j][2] = self.side_f[2][i]
        return c


# Node's class for the BFS we will Implement in the main
class Node:
    def __init__(self, cube=None, move=None, Parent=None):
        self.cube = cube
        self.move = move
        self.Parent = Parent


# A function to Draw the Cube on the Turtle Screen
def DrawCube(tur, cube):
    tur.clear()
    side_f = cube.side_f
    side_b = cube.side_b
    side_l = cube.side_l
    side_r = cube.side_r
    side_u = cube.side_u
    side_d = cube.side_d
    # FaceSide
    # First Row
    for p in range(0, 3):
        tur.begin_fill()
        tur.goto(-200 + p * 50, 100)
        tur.pendown()
        tur.width(5)
        for i in range(0, 4):
            tur.fillcolor(getcolor(side_f[0][p]))
            tur.forward(50)
            tur.right(90)

        tur.end_fill()
        tur.penup()

    # Second Row
    for p in range(0, 3):
        tur.begin_fill()
        tur.goto(-200 + p * 50, 50)
        tur.pendown()
        tur.width(5)

        for i in range(0, 4):
            tur.fillcolor(getcolor(side_f[1][p]))
            tur.forward(50)
            tur.right(90)

        tur.end_fill()
        tur.penup()

        tur.end_fill()
        tur.penup()

    # 3rd Row
    for p in range(0, 3):
        tur.begin_fill()
        tur.goto(-200 + p * 50, 0)
        tur.pendown()
        tur.width(5)

        for i in range(0, 4):
            tur.fillcolor(getcolor(side_f[2][p]))
            tur.forward(50)
            tur.right(90)
        tur.end_fill()
        tur.penup()

    # LeftSide
    # First Row
    for p in range(0, 3):
        tur.begin_fill()
        tur.goto(-350 + (p * 50), 100)
        tur.pendown()
        tur.width(5)
        for i in range(0, 4):
            tur.fillcolor(getcolor(side_l[p][2]))
            tur.forward(50)
            tur.right(90)
        tur.end_fill()
        tur.penup()

    # Second Row
    for p in range(0, 3):
        tur.begin_fill()
        tur.goto(-350 + (p * 50), 50)
        tur.pendown()
        tur.width(5)

        for i in range(0, 4):
            tur.fillcolor(getcolor(side_l[p][1]))
            tur.forward(50)
            tur.right(90)

        tur.end_fill()
        tur.penup()

    # 3rd Row
    for p in range(0, 3):
        tur.begin_fill()
        tur.goto(-350 + (p * 50), 0)
        tur.pendown()
        tur.width(5)

        for i in range(0, 4):
            tur.fillcolor(getcolor(side_l[p][0]))
            tur.forward(50)
            tur.right(90)

        tur.end_fill()
        tur.penup()

    # Right Side
    # First Row
    for p in range(0, 3):
        tur.begin_fill()
        tur.goto(-50 + (p * 50), 100)
        tur.pendown()
        tur.width(5)

        for i in range(0, 4):
            tur.fillcolor(getcolor(side_r[2 - p][0]))
            tur.forward(50)
            tur.right(90)
        tur.end_fill()
        tur.penup()

    # Second Row
    for p in range(0, 3):
        tur.begin_fill()
        tur.goto(-50 + (p * 50), 50)
        tur.pendown()
        tur.width(5)

        for i in range(0, 4):
            tur.fillcolor(getcolor(side_r[2 - p][1]))
            tur.forward(50)
            tur.right(90)
        tur.end_fill()
        tur.penup()

    # 3rd Row
    for p in range(0, 3):
        tur.begin_fill()
        tur.goto(-50 + (p * 50), 0)
        tur.pendown()
        tur.width(5)

        for i in range(0, 4):
            tur.fillcolor(getcolor(side_r[2 - p][2]))
            tur.forward(50)
            tur.right(90)
        tur.end_fill()
        tur.penup()

    # Upside
    # First Row
    for p in range(0, 3):
        tur.begin_fill()
        tur.goto(-200 + (p * 50), 250)
        tur.pendown()
        tur.width(5)
        for i in range(0, 4):
            tur.fillcolor(getcolor(side_u[0][p]))
            tur.forward(50)
            tur.right(90)

        tur.end_fill()
        tur.penup()

    # Second Row
    for p in range(0, 3):
        tur.begin_fill()
        tur.goto(-200 + (p * 50), 200)
        tur.pendown()
        tur.width(5)

        for i in range(0, 4):
            tur.fillcolor(getcolor(side_u[1][p]))
            tur.forward(50)
            tur.right(90)

        tur.end_fill()
        tur.penup()

        tur.end_fill()
        tur.penup()

    # 3rd Row
    for p in range(0, 3):
        tur.begin_fill()
        tur.goto(-200 + (p * 50), 150)
        tur.pendown()
        tur.width(5)

        for i in range(0, 4):
            tur.fillcolor(getcolor(side_u[2][p]))
            tur.forward(50)
            tur.right(90)
        tur.end_fill()
        tur.penup()

    # Downside
    # First Row
    for p in range(0, 3):
        tur.begin_fill()
        tur.goto(-200 + (p * 50), -150)
        tur.pendown()
        tur.width(5)
        for i in range(0, 4):
            tur.fillcolor(getcolor(side_d[0][2 - p]))
            tur.forward(50)
            tur.right(90)

        tur.end_fill()
        tur.penup()

    # Second Row
    for p in range(0, 3):
        tur.begin_fill()
        tur.goto(-200 + (p * 50), -100)
        tur.pendown()
        tur.width(5)

        for i in range(0, 4):
            tur.fillcolor(getcolor(side_d[1][2 - p]))
            tur.forward(50)
            tur.right(90)

        tur.end_fill()
        tur.penup()

        tur.end_fill()
        tur.penup()

    # 3rd Row
    for p in range(0, 3):
        tur.begin_fill()
        tur.goto(-200 + (p * 50), -50)
        tur.pendown()
        tur.width(5)

        for i in range(0, 4):
            tur.fillcolor(getcolor(side_d[2][2 - p]))
            tur.forward(50)
            tur.right(90)
        tur.end_fill()
        tur.penup()

    # Backside
    # First Row
    for p in range(0, 3):
        tur.begin_fill()
        tur.goto(100 + (p * 50), 100)
        tur.pendown()
        tur.width(5)

        for i in range(0, 4):
            tur.fillcolor(getcolor(side_b[0][p]))
            tur.forward(50)
            tur.right(90)
        tur.end_fill()
        tur.penup()

    # Second Row
    for p in range(0, 3):
        tur.begin_fill()
        tur.goto(100 + (p * 50), 50)
        tur.pendown()
        tur.width(5)

        for i in range(0, 4):
            tur.fillcolor(getcolor(side_b[1][p]))
            tur.forward(50)
            tur.right(90)
        tur.end_fill()
        tur.penup()

    # 3rd Row
    for p in range(0, 3):
        tur.begin_fill()
        tur.goto(100 + (p * 50), 0)
        tur.pendown()
        tur.width(5)

        for i in range(0, 4):
            tur.fillcolor(getcolor(side_b[2][p]))
            tur.forward(50)
            tur.right(90)
        tur.end_fill()
        tur.penup()


# A function to check if we have reached the Goal State while applying BFS
def CheckGoalState(cube):
    for i in range(0, 3):
        for j in range(0, 3):
            if cube.side_f[0][0] != cube.side_f[i][j]:
                return False
            if cube.side_b[0][0] != cube.side_b[i][j]:
                return False
            if cube.side_u[0][0] != cube.side_u[i][j]:
                return False
            if cube.side_d[0][0] != cube.side_d[i][j]:
                return False
            if cube.side_l[0][0] != cube.side_l[i][j]:
                return False
            if cube.side_r[0][0] != cube.side_r[i][j]:
                return False
    return True

# The main itself
if __name__ == '__main__':
    #Initialising Turtles Variables for the Graphical Representation of the Cube
    a = turtle.Screen()
    turtle.delay(0)
    tur = turtle.Turtle()
    tur.hideturtle()
    tur.penup()
    tur.speed(0)

    cube = RubikCube()
    DrawCube(tur, cube)
    print('First Scramble The Cube (Every Move here is Inverse Move here) ,Press S to stop Scrambling :')
    #The Code to Scramble the Cube for an Initial State for out Blind Search
    while True:
        c = RubikCube()
        x = input("Enter the Move' :")
        if x == 'U' or x == 'u':
            for i in range(0, 3):
                c = cube.upc()
                del cube
                cube = c
            print("After U' :")
        elif x == 'L' or x == 'l':
            for i in range(0, 3):
                c = cube.leftc()
                del cube
                cube = c
            print("After L' :")
        elif x == "r" or x == "R":
            for i in range(0, 3):
                c = cube.rightc()
                del cube
                cube = c
            print("After R' :")
        elif x == "D" or x == "d":
            for i in range(0, 3):
                c = cube.downc()
                del cube
                cube = c
            print("After D' :")
        elif x == "F" or x == "f":
            for i in range(0, 3):
                c = cube.facec()
                del cube
                cube = c
            print("After F' :")
        elif x == "B" or x == "b":
            for i in range(0, 3):
                c = cube.backc()
                del cube
                cube = c
            print("After B' :")
        elif x == "s" or x == "S":
            break
        DrawCube(tur, cube)

    node = Node(cube, '-', None) # Forming the Root Node for the BFS
    print('Scrambling is Done , Now Solving the Cube')
    visited = []  # List for visited nodes.
    queue = []  # Initialize a queue
    queue.append(node)
    Goalnode = None # Helps for BackTracking
    while queue:
        currnode = queue.pop(0)
        currcube = currnode.cube
        if CheckGoalState(currcube):
            Goalnode = currnode
            break
        else:
            queue.append(Node(currcube.facec(), 'F', currnode))
            queue.append(Node(currcube.backc(), 'B', currnode))
            queue.append(Node(currcube.leftc(), 'L', currnode))
            queue.append(Node(currcube.rightc(), 'R', currnode))
            queue.append(Node(currcube.upc(), 'U', currnode))
            queue.append(Node(currcube.downc(), 'D', currnode))
            visited.append(currnode)

    print('We have found the Solution, Here are the Moves from Initial to Goal State')
    #Backtracking from the Goal to the Initial State
    stack = []
    while Goalnode is not None:
        stack.append(Goalnode)
        Goalnode = Goalnode.Parent

    #Printing How we go from the Inital State to the Goal State
    while stack:
        c = stack.pop()
        if c.move == '-':
            print('Initial State : ')
            DrawCube(tur, c.cube)
            time.sleep(2)
        else:
            print('After Move ', c.move, ' :')
            DrawCube(tur, c.cube)
            time.sleep(1)

    print('We have Reached the Goal State After the Above Moves')

    for i in visited:
        del i.cube
        del i
    for i in queue:
        del i.cube
        del i

    print('Click on the Turtle Window to close it')
    turtle.exitonclick()
