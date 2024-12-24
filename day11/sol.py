import math 


#final optimized solution is explore_blinks which uses DFS and memoization to count nr of stones after blinks
#Time complexity is hard to precisely define but it must be polynomial since 75 blinks takes just milliseconds, compared to pre optimization bruteforce which would take about 4 million years, bruteforce complexy was O(2^n)
#Increasing max memo capacity --> improved time complexity
#Memory complexity: O(B*10^d) where B is nr of blinks and d is the max number of digits memoized stones can possess. 
class Sol:

    def __init__(self, inputPath):
        file = open(inputPath, "r")
        data = file.readline()

        self.init_stones = data.split()
        for i in range(len(self.init_stones)):
            self.init_stones[i] = int(self.init_stones[i])

        self.stones = self.init_stones.copy()
        self.memo:dict[tuple[int], list[int]] = {}
        
        self.explorememo:dict[(int, int), int] = {} # dict[(int: digit, int: blinks), int:count]
    
    def reset_stones(self):
        self.stones = self.init_stones.copy()
    
    def print_init_stones(self):
        print(self.init_stones)
    def print_stones(self):
        print(self.stones)
    
    def _digit_count(self, i:int):
        return int(math.floor(math.log10(i) + 1))

    def _split_integer(self, i:int, digit_cnt:int)->tuple[int, int]:
        divisor = (10**(digit_cnt/2))
        return (int((i//divisor)),int(i%divisor))

    def print_memo(self):
        print(self.memo)

    def blink(self):
        i = 0
        while i < len(self.stones):
            #print(f'i: {i}') 
            #self.print_stones()
            stone = self.stones[i]
            if (stone == 0): 
                self.stones[i] = 1
                i += 1
                continue
            dcount = self._digit_count(stone)
            #print(f'dcount: {dcount}')
            if dcount % 2 == 0:
                (lval, rval) = self._split_integer(stone, dcount)
                self.stones[i] = lval
                self.stones.insert(i + 1, rval)
                i += 2
            else:
                self.stones[i] *= 2024
                i += 1           

    def handle_stone(self, stone:int)->list[int]:
        if (stone == 0): 
            return [1]
        dcount = self._digit_count(stone)
        if dcount % 2 == 0:
            (lval, rval) = self._split_integer(stone, dcount)
            return [lval, rval]
        else:
            return [stone*2024]


    def proc_sublist(self, sublist):
        l = sublist
        N = len(l)
        #print(f'N: {N}, list: {l}')
        if (N == 1):
            return self.handle_stone(l[0])
        elif (N >= 2):
            if (tuple(l) in self.memo): return self.memo[tuple(l)]
            tv = self.proc_sublist(l[0:N//2])+self.proc_sublist(l[N//2:N])
            self.memo[tuple(l)] = tv
            return tv 
        else: return []

    def explore_stone(self, stone:int,blinks:int):
        if (blinks == 0): return 1
        if (stone == 0): 
            if((stone,blinks) in self.explorememo):
                return self.explorememo[(stone,blinks)]
            cnt = self.explore_stone(1, blinks - 1)
            self.explorememo[(stone, blinks)] = cnt
            return cnt
        else:
            MAX_DCOUNT = 7
            dcount = self._digit_count(stone)
            if (dcount < MAX_DCOUNT and (stone, blinks) in self.explorememo):
                return self.explorememo[(stone, blinks)]


            cnt = 0
            if (dcount % 2 == 0):
                (a, b)=self._split_integer(stone, dcount)
                cnt = self.explore_stone(a, blinks - 1) + self.explore_stone(b, blinks - 1)
            else:
                cnt = self.explore_stone(stone*2024, blinks - 1)

            if (dcount < MAX_DCOUNT):
                self.explorememo[(stone, blinks)] = cnt
                 
            return cnt
                

    def explore_blinks(self, blinks):
        self.reset_stones()
        stoneCnt = 0
        for stone in self.stones:
            stoneCnt += self.explore_stone(stone, blinks)
        return stoneCnt

    

    def opt_blink(self):
        self.stones = self.proc_sublist(self.stones)
    
    def opt_blinks(self, blinks:int):
        self.stones = self.init_stones
        for i in range(blinks):
            self.opt_blink()
    
    def blinks(self, blinks:int):
        self.stones = self.init_stones
        for i in range(blinks):
            self.blink()
    
    def solve1(self):
        blinkCnt = 25
        self.blinks(blinkCnt)
        return len(self.stones)


sol = Sol("input.txt")
sol.print_init_stones()
sol.print_stones()
print("blinking:")
#sol.opt_blinks(35)
stones = sol.explore_blinks(300)
print(stones)
#sol.print_stones()
print(len(sol.stones))
#print(sol.explorememo)
