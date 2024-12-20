
class Sol:
    def __init__(self, inputPath):
        file = open(inputPath, "r")
        data = file.readlines()
        for i in range(len(data)):
            data[i]= data[i].replace("\n", "")
            i += 1

        self.rows = len(data)
        self.columns = len(data[0])
        self.charMatrix:list[list[chr]] = []
    
        for i in range(self.rows):
            lst = list(data[i])
            for j in range(len(lst)):
                lst[j] = int(lst[j])

            self.charMatrix.append(lst)


        self.visitMatrix = [[0] * self.columns for i in range(self.rows)]
        self.find_trail_heads()
        self.visitedMarker = 0

    def print_char_matrix(self):
        for row in self.charMatrix:
            print(row)
    def print_visit_matrix(self):
        for row in self.visitMatrix:
            print(row)
    def print_trail_heads(self):
        print(self.trailHeads)

    def find_trail_heads(self):
        trailHeads:list[(int, int)] = []
        for i in range(self.rows):
            for j in range(self.columns):
                if (self.charMatrix[i][j] == 0): trailHeads.append((i,j))
        self.trailHeads = trailHeads 



    def trail_head_score(self,x, y):
        self.visitedMarker += 1
        visited = self.visitedMarker
        queue:list[(int,int)] = [(x,y)]
        cmatx = self.charMatrix
        visitmatx  = self.visitMatrix
        visitmatx[x][y] = visited

        score = 0
        while(len(queue) > 0):
            (x,y) = queue.pop(0)
            currV = cmatx[x][y]

            if(currV == 9):
                score += 1
                continue

            if (y > 0 and cmatx[x][ y - 1] - currV == 1 and visitmatx[x][ y - 1] != visited): 
                queue.append((x, y - 1))
                visitmatx[x][y - 1] = visited
                
            if (y < self.columns - 1 and cmatx[x][ y + 1] - currV == 1 and visitmatx[x][ y + 1] != visited):
                queue.append((x, y + 1))
                visitmatx[x][y + 1] = visited
            if (x > 0 and cmatx[x - 1][ y] - currV == 1 and visitmatx[x - 1][ y] != visited):
                queue.append((x-1,y))
                visitmatx[x - 1][y] = visited 
            if (x < self.rows - 1 and cmatx[x + 1][ y] - currV == 1 and visitmatx[x + 1][ y] != visited):
                queue.append((x+1,y))
                visitmatx[x + 1][y] = visited 

        return score
    
    def trail_head_score2(self,x, y):
        queue:list[(int,int)] = [(x,y)]
        cmatx = self.charMatrix


        score = 0
        while(len(queue) > 0):
            (x,y) = queue.pop(0)
            currV = cmatx[x][y]

            if(currV == 9):
                score += 1
                continue

            if (y > 0 and cmatx[x][ y - 1] - currV == 1): 
                queue.append((x, y - 1))
            if (y < self.columns - 1 and cmatx[x][ y + 1] - currV == 1):
                queue.append((x, y + 1))
            if (x > 0 and cmatx[x - 1][ y] - currV == 1):
                queue.append((x-1,y))
            if (x < self.rows - 1 and cmatx[x + 1][ y] - currV == 1):
                queue.append((x+1,y))

        return score
        
    def trail_head_score_sum(self):
        score = 0
        for (x,y) in self.trailHeads:
            score += self.trail_head_score(x,y)
        return score
    
    def trail_head_score_sum2(self):
        score = 0
        for (x,y) in self.trailHeads:
            score += self.trail_head_score2(x,y)
        return score




sol = Sol("input.txt")
sol.print_char_matrix()
sol.print_visit_matrix()
sol.print_trail_heads()
(x,y)=sol.trailHeads[0]
score = sol.trail_head_score_sum()
print(score)
score2 = sol.trail_head_score_sum2()
print(score2)