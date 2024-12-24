import re

class Sol:

    def __init__(self, inputPath):
        file = open(inputPath, "r")
        data = file.read()
        self.data = re.sub(r'\s+', "", data)
        self.digits = list(self.data)
        #convert digit chars to int
        for i in range(len(self.digits)):
            self.digits[i] = int(self.digits[i])

        self.space:list[(int, int)] = [] # [(size, index)] sorted by size
        self.files:list[(int, int)] = [] # [(index, size)] reverse sort by index

        self.gen_block_map()
        self.analyze_blocks()

    def analyze_blocks(self):
        i = 0
        length = len(self.blockMap)
        while i < length:
            
            j = i
            while(j < length and self.blockMap[j] == -1):
                j += 1
            if (j - i > 0):
                self.space.append((j - i, i))
                i = j
                continue

            jval = self.blockMap[j]
            while(j < length and self.blockMap[j] != - 1 and self.blockMap[j] == jval):
                j += 1
            if (j - i > 0):
                self.files.append((i, j - i))
                i = j
            
        def sorter(e):
            return e[0]
        
        self.space.sort(key=sorter)
        self.files.sort(key=sorter)


    def print_space(self):
        print(self.space)

    def print_files(self):
        print(self.files)

    # nr inserts: N*avg(digits)
    def gen_block_map(self):
        idcnt = 0
        spaceFlag = -1
        blockMap = []
        for i in range(len(self.digits)):
            d = self.digits[i]
            if i % 2 == 0:
                for j in range(d):
                    blockMap.insert(0,idcnt)
                if (d > 0): idcnt += 1
            else:
                for j in range(d):
                    blockMap.insert(0,spaceFlag)
        blockMap.reverse()
        self.blockMap = blockMap

   
    def printBlockMap(self):
        print(self.blockMap)

    def find_free_space(self, size:int):
        #return index of free space with size >= size
        container = []
        for i in range(len(self.space)):
            if self.space[i][0] >= size:
                container.append((self.space[i][1], i)) 
        minT = min(container, key=lambda e: e[0], default=(-1, -1))
        
        return minT[1]


    def compact(self):
        
        while self.files:
            minFreeIndex:int = min(self.space, key=lambda e: e[1])[1]
            (index, size) = self.files.pop()
            if (minFreeIndex >= index): break
            foundSpaceIndex = self.find_free_space(size)

            #print(f'file(index,size):{(index, size)} space(size,index):{self.space[foundSpaceIndex]}')

            if(foundSpaceIndex != -1):
                (fsize, findex) = self.space[foundSpaceIndex]
                if (findex > index): continue
                #print(f"Moving file {index} to {findex}")

                id = self.blockMap[index]
                FREE = -1
                for i in range(size):
                    self.blockMap[findex + i] = id
                    self.blockMap[index + i] = FREE
                if(fsize == size): self.space.pop(foundSpaceIndex)
                else: self.space[foundSpaceIndex] = (fsize - size, findex + size)
                self.space.sort(key=lambda e: e[1])
                #self.printBlockMap()


       

    def fragment(self):
        FREE_SPACE=-1
        lptr = 0
        rptr = len(self.blockMap) - 1

        bmap = self.blockMap
        while lptr <= rptr:
            if(bmap[rptr] < 0): rptr -= 1
            elif(bmap[lptr] >= 0): lptr += 1
            else:
                bmap[lptr] = bmap[rptr]
                bmap[rptr] = FREE_SPACE

    def blockCheckSum(self):
        bmap = self.blockMap
        i = 0
        sum = 0
        while(bmap[i] >= 0):
            sum += (i * bmap[i])
            i += 1
        return sum

    def blockCheckSum2(self):
        s = 0
        for i in range(len(self.blockMap)):
            if(self.blockMap[i] != -1): s += i * self.blockMap[i]
        return s



    

sol = Sol("input.txt")
#sol.printBlockMap()
#print(len(sol.blockMap))
#sol.print_space()
#sol.print_files()
sol.compact()
#sol.printBlockMap()
print(sol.blockCheckSum2())
#print(sol.digits)