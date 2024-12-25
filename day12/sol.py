
coord = tuple[int, int]
edge = coord
vertex = list[edge] | None



class Sol:
    def __init__(self, inputPath):
        type area = int
        type perimeter = int
        self.regions:list[(area, perimeter)] = []        
        self._parseInput(inputPath)
        
        self.matrixVisits = [[False for j in range(self.mtrxN)] for i in range(self.mtrxN)]
        self.visitCnt = 0

    def _parseInput(self, inputPath):
        file = open(inputPath, "r")
        data = file.readlines()
        self.mtrxN = len(data)
        for i in range(len(data)):
            data[i] = data[i].strip()
        
        self.matrix = []
        for i in range(self.mtrxN):
            self.matrix.append(list(data[i]))

    def safe_insert(self, lst, tup):
        if(tup not in lst): lst.insert(0,tup)

    def explore_region(self, start:coord):
        if(self.matrixVisits[start[0]][start[1]]): raise RuntimeError("already visitied this part of matrix")
        
        visitQ:list[coord] = [start]
        vis = self.matrixVisits
        plant = self.matrix[start[0]][start[1]]
        area = 0
        perimeter = 0

        while len(visitQ) > 0:
            #print(f'visited: {vis}, visitQ: {visitQ}')  
            (r,c) = visitQ.pop()
            adj = 0
            if (c > 0 and self.matrix[r][c-1] == plant):
                if(not vis[r][ c - 1]):
                    visitQ.insert(0,(r, c - 1))
                    vis[r][c-1] = True
                adj +=1
            if (c < self.mtrxN - 1 and self.matrix[r][c + 1] == plant):
                if(not vis[r][ c + 1]):
                    visitQ.insert(0,(r, c + 1))
                    vis[r][c+1] = True
                adj +=1
            if (r > 0 and self.matrix[r - 1][c] == plant):
                if(not vis[r-1][c]):
                    visitQ.insert(0,(r-1,c))
                    vis[r-1][c] = True
                adj +=1
            if (r < self.mtrxN - 1 and self.matrix[r+1][c] == plant):
                if(not vis[r+1][c]):
                    visitQ.insert(0,(r+1,c))
                    vis[r+1][c] = True
                adj +=1
            
            perimeter += (4 - adj)
            area +=1
            vis[r][c] = True            
            self.visitCnt +=1
        self.regions.append((plant, area,perimeter))

    def find_unvisited(self):
        for r in range(self.mtrxN):
            for c in range(self.mtrxN):
                if (not self.matrixVisits[r][c]): return (r,c)
        
        return (-1,-1)

    def explore_right(self, start:coord, plant: chr, visitQ:list[coord]):
        (row, col) = start
        i = col
        matrix = self.matrix
        visits = self.matrixVisits
        left = 0
        right = 0
        up = 0
        down = 0

        area = 0
        while(i < self.mtrxN and matrix[row][i] == plant):
            if (i <= 0 or matrix[row][i - 1] != plant):
                left = 1
            if (i >= self.mtrxN - 1 or matrix[row][i + 1] != plant):
                right = 1
            if (row <= 0 or matrix[row - 1][i] != plant):
                up = 1
            if (row >= self.mtrxN - 1 or matrix[row + 1][i] != plant):
                down = 1
            
            if (row < self.mtrxN - 1 and matrix[row + 1][i] == plant):
                if(not visits[row + 1][i]):
                    visitQ.insert(0,(row + 1, i))
                    visits[row + 1][i] = True

            visits[row][i] = True
            area += 1
            self.visitCnt +=1 
            i += 1
            s = 0
            if (left + right + up + down > 0): s = 1

        return (area ,s)
        
    def explore_region2(self, start:coord):
        visitQ:list[coord] = [start]
        area = 0
        sides = 0
        plant = self.matrix[start[0]][start[1]]

        while len(visitQ) > 0:
            row = visitQ.pop()
            (a, s) = self.explore_right(row, plant, visitQ)
            area += a
            sides += s
            
        self.regions.append((plant , area, sides))



    def explore_regions2(self):
        maxVisits = self.mtrxN*self.mtrxN

        while self.visitCnt < maxVisits:
            unvisited = self.find_unvisited()
            if(unvisited == (-1,-1)):break
            self.explore_region2(unvisited)


    def explore_regions(self):
        maxVisits = self.mtrxN * self.mtrxN

        while self.visitCnt < maxVisits:
            unvisited = self.find_unvisited()
            if (unvisited == (-1,-1)): break
            self.explore_region(unvisited)
            


    def calculate_cost(self):
        cost = 0
        for (_,area, perimeter) in self.regions:
            cost += area * perimeter

        return cost

    def solve1(self):
        self.explore_regions()
        return self.calculate_cost() 
    
    def solve2(self):
        self.explore_regions2()
        return self.calculate_cost()

fpath = "example.txt"
sol = Sol(fpath)
print(sol.solve1())
print(sol.regions)
sol = Sol(fpath)
print(sol.solve2())
print(sol.regions)
#print(sol.matrix)
#print(sol.matrixVisits)
#print(sol.visitCnt)
#for region in sol.regions:
 #   print(region)

