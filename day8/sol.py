

class Sol:

    def __init__(self, inputPath):
        file = open(inputPath, "r")
        lines = file.readlines()
        self.lines = lines
        file.readline()
        
        
        self.length:int = len(lines)
        self.map:list[list[chr]] = []

        self.initialize_map_from_lines()

        self.antennaMap:dict[chr, list[(int,int)]] = {}

        for i in range(self.length):
            for j in range(self.length):
                ant = self.map[i][j]
                if(ant == '.'): continue
                elif(ant in self.antennaMap): self.antennaMap[ant].insert(0,(i,j))
                else: 
                    self.antennaMap[ant] = [(i,j)]

        self.vectorPairs:dict[chr, list[tuple[int, int], tuple[int, int]]]={}

        for antenna in self.antennaMap:
            alen = len(self.antennaMap[antenna])
            ants = self.antennaMap[antenna]
            for i in range(alen):
                for j in range(i + 1, alen):
                    if antenna in self.vectorPairs:
                        self.vectorPairs[antenna].insert(0,(ants[i],ants[j]))
                    else: self.vectorPairs[antenna] = [(ants[i], ants[j])]
        self.antiNodeCnt = 0

    def initialize_map_from_lines(self):
        self.map = []
        for i in range(self.length):
            self.map.append(list(self.lines[i].strip()))

    def printVectorPairs(self):
        for antenna in self.vectorPairs:
            print(f'{antenna}: {self.vectorPairs[antenna]}')

    def printMap(self):
        result = "\n".join("".join(row) for row in self.map)
        print(result)
            



    def printAntennaMap(self):
        for antenna in self.antennaMap:
            print(f'{antenna}: {self.antennaMap[antenna]}')

    def putAntiNode(self, x, y):
        if (x < self.length and x >= 0 and y < self.length and y >=0 and self.map[x][y] != '#') :
            self.antiNodeCnt += 1
            self.map[x][y] = '#'

    def putAntiNodesByIncrement(self,x_start,y_start ,x_incr, y_incr):
        x = x_start
        y = y_start
        while (x < self.length and x >= 0 and y < self.length and y >=0):
            if(self.map[x][y] != '#'):
                self.antiNodeCnt += 1
                self.map[x][y] = '#'
            x += x_incr
            y += y_incr
        

    def antiNodeGen2(self):
        for antenna in self.vectorPairs:
            for((a,b), (c,d)) in self.vectorPairs[antenna]:
                self.putAntiNodesByIncrement(c, d, c-a, d - b)
                self.putAntiNodesByIncrement(a, b, a -c , b - d)


    def antiNodeGen(self):
        for antenna in self.vectorPairs:
            for ((a, b), (c, d)) in self.vectorPairs[antenna]:
               # print(f'v0:{(2*c - a, 2*d - b)}, v1: {2*a - c, 2*b - d}')
                self.putAntiNode(2*c - a, 2*d - b)
                self.putAntiNode(2*a - c, 2*b - d)

    def solve(self):
        self.antiNodeGen()
        return self.antiNodeCnt
    
    def solve2(self):
        self.antiNodeCnt = 0
        self.initialize_map_from_lines()
        self.antiNodeGen2()
        return self.antiNodeCnt


sol = Sol("input.txt")

sol.printMap()
print(sol.solve())
sol.printMap()
print(sol.solve2())
