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

        self._gen_block_map()

    # nr inserts: N*avg(digits)
    def _gen_block_map(self):
        idcnt = 0
        spaceFlag = -1
        blockMap = []
        for i in range(len(self.digits)):
            d = self.digits[i]
            if i % 2 == 0:
                for i in range(d):
                    blockMap.insert(0,idcnt)
                idcnt += 1
            else:
                for i in range(d):
                    blockMap.insert(0,spaceFlag)
        blockMap.reverse()
        self.blockMap = blockMap

    def printBlockMap(self):
        print(self.blockMap)

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






    

sol = Sol("input.txt")
sol.fragment()
#sol.printBlockMap()
print(sol.blockCheckSum())