import mmh3
import math
import random
import matplotlib.pyplot as plt
from tqdm import tqdm


class FM2:
    def __init__(self,domain_size,groupsize):
        self.bitarray = [0 for _ in range(groupsize)]
        self.domain_size = domain_size
        self.n_bits = math.ceil(math.log2(domain_size))
        self.mask = (1 << self.n_bits) - 1
        self.seed = [random.randint(0,9999999) for _ in range(groupsize)]
        self.groupsize = groupsize

    def put(self,item):
        for i in range(self.groupsize):
            h = mmh3.hash(item,self.seed[i]) & self.mask
            r = 0
            if h == 0:
                return
            while (h & (1 << r)) == 0:
                r += 1
            self.bitarray[i] |= (1 << r)
    def size(self):
        sum = 0
        for i in range(self.groupsize):
            R = 0
            while(self.bitarray[i] & (1 << R) != 0):
                R += 1
            sum += R
        R = sum / self.groupsize
        return 2 ** R/0.77351

class FM1:
    def __init__(self,domain_size):
        self.bitarray = 0
        self.domain_size = domain_size
        self.n_bits = math.ceil(math.log2(domain_size))
        self.mask = (1 << self.n_bits) -1
        self.seed = random.randint(0,9999999)
        self.r_list = []

    def put(self,item):
        h = mmh3.hash(item,self.seed) & self.mask
        r = 0
        if h == 0:
            return
        while (h & (1 << r)) == 0:
            r += 1
        if len(self.r_list) == 0:
            self.r_list.append(r)
        elif self.r_list[0] < r:
            del self.r_list[0]
            self.r_list.append(r)
        self.bitarray |= (1 << r)
    def size(self):
        R = self.r_list[0]
        #while(self.bitarray & (1 << R) != 0):
        #    R += 1
        return 2 ** R

x1_test = []
y1_test = []

x2_test = []
y2_test = []
tset1 = set()
tset2 = set()


fm1 = FM1(1000)
fm2 = FM2(1000,10)
for j in tqdm(range(10000)):
    item = str(random.randint(0,100000))
    fm1.put(item)
    fm2.put(item)
    tset1.add(item)
    tset2.add(item)

    x1_test.append(len(tset1))
    y1_test.append(fm1.size())
    x2_test.append(len(tset2))
    y2_test.append(fm2.size())

print(f"true: {len(tset1)}, estimate: {fm1.size()}")


plt.scatter(x1_test,y1_test,color ='r',s = 5,label = "FM1")
plt.scatter(x2_test,y2_test,color ='green', s = 5, label = "FM2")
plt.plot(x1_test,x1_test,label = 'true')
plt.legend()
plt.xlabel("test_x")
plt.ylabel("fm_size")
plt.show()