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

        self.gen_block_map()

    # nr inserts: N*avg(digits)
    def gen_block_map(self):
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

    def gen_block_map2(self):
        idcnt = 0
        spaceFlag = -1
        blockMap = []
        for i in range(len(self.digits)):
            d = self.digits[i]
            tmp = []
            if i % 2 == 0:
                for i in range(d):
                    tmp.insert(0,idcnt)
                idcnt += 1
            else:
                for i in range(d):
                    tmp.insert(0,spaceFlag)
            if(len(tmp) > 0): blockMap.insert(0,tmp)
        blockMap.reverse()
        self.blockMap = blockMap    

    def printBlockMap(self):
        print(self.blockMap)

    def _find_leftmost_space(self,prevlm):
        i = prevlm
        if(i > 0): i += 1
        while True:
            #print("LOOP STUCK LEFTMOST")
            if (i >= len(self.blockMap)): return len(self.blockMap)
            elif (self.blockMap[i][0] == -1): return i
            else: i += 1
    
    def _next_rmost_file(self, prevrm):
        i = prevrm
        i -= 1
        while True:
            #print("LOOP STUCK NEXT RMOST")
            if(i < 0): return len(self.blockMap)
            elif(self.blockMap[i][0] != -1): return i
            else: i -= 1

    def _free_space_merge(self):
        bmap = self.blockMap
        i = 1
        while(i < len(bmap)):
            if(bmap[i][0] == -1 and bmap[i-1][0] == -1):
                bmap[i-1] = bmap[i-1] + bmap[i]
                bmap.pop(i)
            else: i += 1

    def split_list(self, lst, split_index_exclusive):
        return (lst[0:split_index_exclusive], lst[split_index_exclusive:len(lst)])
    
    def compact(self):
        lmost = self._find_leftmost_space(0)
        lptr = lmost
        rptr = self._next_rmost_file(len(self.blockMap))

        bmap:list[list[int]] = self.blockMap
        while (lmost < rptr):
            lptr = self._find_leftmost_space(0)
            #print(f'(lmost, rptr): {lmost, rptr}')     
            while(lptr < rptr):
                lptr = self._find_leftmost_space(0)
                rptr = self._next_rmost_file(0)
                spaceLen = len(bmap[lptr])
                fileLen = len(bmap[rptr])
                if (spaceLen >= fileLen):
             #       print(f'inner loop: {lptr, rptr}')
                    if(spaceLen > fileLen):
                        (tmpFileLoc, newSpaceLoc) = self.split_list(bmap[lptr], fileLen)
                        bmap[lptr] = tmpFileLoc
                        bmap.insert(lptr + 1, newSpaceLoc)  
                        rptr += 1
                        #print(f'spaceLen: {spaceLen}, fileLen: {fileLen} ,{tmpFileLoc+newSpaceLoc} --> {(tmpFileLoc, newSpaceLoc)}')
                    tmp = bmap[lptr]
                    bmap[lptr] = bmap[rptr]
                    bmap[rptr] = tmp
                    lmost = self._find_leftmost_space(lmost)
                    #self.printBlockMap()
                    break
                else: 
                    rptr = self._next_rmost_file(rptr)
            self._free_space_merge()
                           
         


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






    

sol = Sol("example.txt")
sol.printBlockMap()
sol.fragment()
sol.printBlockMap()
print(sol.blockCheckSum())
sol.gen_block_map2()
sol.printBlockMap()
sol.compact()
sol.printBlockMap()