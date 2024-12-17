from enum import Enum
import copy

class Sol:
    
    class Direction(Enum):
        UP = 0,
        DOWN = 1,
        LEFT = 2,
        RIGHT = 3,
        UNKNOWN = -1

    _X = 0
    _Y = 1

    def __init__(self, inputPath):
        self.Direction = Sol.Direction
        self.inputPath = inputPath
        file = open(inputPath, "r")
        lines = file.readlines()
        self.currPos = (0,0)
        self.direction = self.Direction.UNKNOWN

        alreadyFound = False
        for i in range(len(lines)):
            lines[i] = lines[i].strip()
            if alreadyFound: continue

            foundGuard = lines[i].find("^")
            if foundGuard != -1: 
                self.currPos = (i, foundGuard)
                self.direction = self.Direction.UP
                lines[i] = lines[i].replace("^",".")
                alreadyFound = True

        self.initPos = (self.currPos[self._X], self.currPos[self._Y])
        self.initDirection = self.direction
        self.map = lines
        self.visitMatrix = [[False for i in range(len(lines))] for j in range(len(lines[0]))]
        self.maxRow = len(lines)
        self.maxCol = len(lines[0])
        self.uniqueVisits = 1
        self.completed = False
        self.visitMatrix[self.currPos[self._X]][self.currPos[self._Y]] = True

        #print(self.map)

    def _readMapPos(self, i, j):
        if i >= self.maxRow or i < 0 or j >= self.maxCol or j < 0: return '?'
        return self.map[i][j]
    
    def _checkNextStep(self):
        (i,j) = self.currPos
        if self.direction == self.Direction.UP: return self._readMapPos(i - 1, j)
        elif self.direction == self.Direction.DOWN: return self._readMapPos(i + 1, j)
        elif self.direction == self.Direction.LEFT: return self._readMapPos(i, j - 1)
        elif self.direction == self.Direction.RIGHT: return self._readMapPos(i, j + 1)
        else: raise RuntimeError("self.direction is invalid or unknown")

    def _rotateDir(self):
        currDir = self.direction
        if currDir == self.Direction.UP: self.direction = self.Direction.RIGHT
        elif currDir == self.Direction.DOWN: self.direction = self.Direction.LEFT
        elif currDir == self.Direction.LEFT: self.direction = self.Direction.UP
        elif currDir == self.Direction.RIGHT: self.direction = self.Direction.DOWN
        else: raise RuntimeError("current direction is invalid")
        

    def _moveNext(self):
        next = self._checkNextStep()
        (i,j) = self.currPos
        if next == '.': 
            if self.direction == self.Direction.UP: self.currPos = (i - 1, j)
            elif self.direction == self.Direction.DOWN: self.currPos = (i + 1, j)
            elif self.direction == self.Direction.LEFT: self.currPos = (i, j - 1)
            elif self.direction == self.Direction.RIGHT: self.currPos = (i, j + 1)
            else: raise RuntimeError("invalid self.direction")

            if self.visitMatrix[self.currPos[self._X]][self.currPos[self._Y]] == False:
                self.visitMatrix[self.currPos[self._X]][self.currPos[self._Y]] = True
                self.uniqueVisits += 1
        elif next == '#':
            self._rotateDir()
        elif next == "?": 
            self.completed = True
        else: raise RuntimeError("invalid next char")

    def _moveNext2(self):
        next = self._checkNextStep()
        (i, j) = self.currPos
        if next == '.': 
            if self.direction == self.Direction.UP: self.currPos = (i - 1, j)
            elif self.direction == self.Direction.DOWN: self.currPos = (i + 1, j)
            elif self.direction == self.Direction.LEFT: self.currPos = (i, j - 1)
            elif self.direction == self.Direction.RIGHT: self.currPos = (i, j + 1)
            else: raise RuntimeError("invalid self.direction")

            if self.currPos in self.visitMap:
                if self.direction in self.visitMap[self.currPos]:
                    self.looped = True
                    self.completed = True
                else: 
                    self.visitMap[self.currPos].append(self.direction)
            else:
                self.visitMap[self.currPos] = [self.direction]

        elif next == '#':
            self._rotateDir()
        elif next == "?": 
            self.completed = True
        else: raise RuntimeError("invalid next char")

    def printMap(self):
        for line in self.map:
            print(line)
         
    def printVisitMatrix(self):
        for row in self.visitMatrix:
            print(row)

    def solve1(self):
       # print(f'$init: {self.currPos}')
        while self.completed == False:
            self._moveNext()
        #    print(self.currPos)
        
        return self.uniqueVisits
    
    def solve2(self):
        while self.completed == False:
            self._moveNext()
        
        self.visitedCoords=[]
        for i in range(self.maxRow):
            for j in range (self.maxCol):
                if self.visitMatrix[i][j]:
                    if self.initPos != (i,j):
                        self.visitedCoords.insert(0,(i,j))
        
        self.visitMap:dict[(int, int), list[int]] = {}
        origMap = copy.copy(self.map)
    
        self.looped = False
        self.loopPos = 0
        for (i,j) in self.visitedCoords:
            premod = self.map[i]
            modified = self.map[i][:j] + '#' + self.map[i][j + 1:]
            self.map[i] = modified
            self.currPos = self.initPos
            self.direction = self.initDirection
            self.completed = False
            self.looped = False
            
            

            #self.printMap()
            #print("\n-----------\n")

            while self.completed == False:
                self._moveNext2()
            if self.looped: self.loopPos += 1
            self.map[i] = premod
            self.visitMap = {}

        return self.loopPos
        
    

sol = Sol("input.txt")

print(sol.solve2())