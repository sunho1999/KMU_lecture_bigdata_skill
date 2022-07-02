import random
from tqdm import tqdm
import matplotlib.pyplot as plt

class Reservoir:
    def __init__(self,k):
        self.sampled = []
        self.k = k
        self.cnt = 0

    def put(self,item):
        if self.cnt < self.k:
            self.sampled.append(item)
        else:
            r = random.randint(0,self.cnt)
            if r < self.k:
                self.sampled[0] = item
        self.cnt += 1
class Reservoir_non:
    def __init__(self,k):
        self.sampled = []
        self.k = k
        self.cnt = 0

    def put(self,item):
        if self.cnt < self.k:
            self.sampled.append(item)
        else:
            r = random.randint(0,self.cnt)
            if r < self.k:
                self.sampled[r] = item
        self.cnt += 1

answer = [0 for i in range(1000)]
answer_non = [0 for i in range(1000)]
for i in tqdm(range(10000)): # 10000번 반복
    for j in range(100):
        reservoir = Reservoir(1)
        for k in range(1000): # 이때 stream의 수의 범위는 0~1000
            reservoir.put(k)

        answer[reservoir.sampled[0]] +=1

for i in range(10000):
    reservoir_non = Reservoir_non(100)
    for k in range(1000):  # 이때 stream의 수의 범위는 0~1000
        reservoir_non.put(k)
    for i in reservoir_non.sampled:
        answer_non[i] += 1
plt.subplot(2,1,1)
plt.bar([i for i in range(1000)], answer, color='#e35f62')
plt.title('replace')
plt.ylabel("extract count")

plt.subplot(2,1,2)
plt.bar([i for i in range(1000)], answer_non,color='forestgreen')
plt.ylabel("extract count")
plt.title('non_reaplace')
plt.show()


