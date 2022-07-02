import random
import matplotlib.pyplot as plt
from tqdm import tqdm
class Bucket:
    def __init__(self,start,end):
        self.start = start
        self.end = end
    def __repr__(self):
        return f"({self.start},{self.end})"
class Dgim():
    def __init__(self):
        self.bucket_tower = [[]]
        self.ts = 0
    def put(self,bits):

        if bits == 1:
            self.bucket_tower[0].insert(0,Bucket(self.ts,self.ts))

            layer = 0
            if len(self.bucket_tower) < 2:
                while len(self.bucket_tower[layer]) > 2:
                    if len(self.bucket_tower) <= layer + 1:
                        self.bucket_tower.append([])

                    b1 = self.bucket_tower[layer].pop()
                    b2 = self.bucket_tower[layer].pop()
                    b1.end = b2.end

                    self.bucket_tower[layer+1].insert(0,b1)
                    layer +=1
        self.ts +=1

    def count(self,k):
        s = self.ts - k
        cnt = 0

        for layer,buckets in enumerate(self.bucket_tower):
            for bucket in buckets:
                if s <= bucket.start:
                    cnt += (1 << layer)
                elif s <= bucket.end:
                    cnt += (1 << layer) * (bucket.end-s +1) // (bucket.end - bucket.start +1)
                    return cnt
                else:
                    return cnt
        return  cnt

class Dgim1():
    def __init__(self):
        self.bucket_tower = [[]]
        self.ts = 0

    def put(self,bits):

        if bits == 1:
            self.bucket_tower[0].insert(0,Bucket(self.ts,self.ts))

            layer = 0
            if len(self.bucket_tower) < 2:
                while len(self.bucket_tower[layer]) > 2:
                    if len(self.bucket_tower) <= layer + 1:
                        self.bucket_tower.append([])

                    b1 = self.bucket_tower[layer].pop()
                    b2 = self.bucket_tower[layer].pop()
                    b1.end = b2.end

                    self.bucket_tower[layer+1].insert(0,b1)
                    layer +=1
        self.ts +=1

    def count(self,k):
        s = self.ts - k
        cnt = 0

        for layer,buckets in enumerate(self.bucket_tower):
            for bucket in buckets:
                if s <= bucket.start:
                    cnt += (1 << layer)
                elif s <= bucket.end:
                    cnt += (1 << layer) * (bucket.end-s +1) // (bucket.end - bucket.start +1)
                    return cnt
                else:
                    return cnt
        return  cnt
class Dgim2():
    def __init__(self):
        self.bucket_tower = [[]]

    def put(self,bits):
        self.bucket_tower[0].insert(0,bits)
        layer = 0
        while len(self.bucket_tower[layer]) > 2:
            if len(self.bucket_tower) < layer + 2:
                self.bucket_tower.append([])
            if type(self.bucket_tower[layer][-1]) is list: # layer[-1]이 list일 때
                if type(self.bucket_tower[layer][-2]) is  list: # layer[-2]이 list일 때
                    if sum(self.bucket_tower[layer][-1]) + sum(self.bucket_tower[layer][-2]) <= (2**(layer+1)): # 2^b보다 작을때 2개를 올림
                        a1 = self.bucket_tower[layer].pop()
                        a2 = self.bucket_tower[layer].pop()
                        self.bucket_tower[layer + 1].insert(0, a1)
                        self.bucket_tower[layer + 1].insert(0, a2)
                    else:  # 2^b 보다 클때 1개만 올림
                        a1 = self.bucket_tower[layer].pop()
                        self.bucket_tower[layer + 1].insert(0, a1)

                elif type(self.bucket_tower[layer][-2]) is int: # layer[-2]이 int일 때
                    if sum(self.bucket_tower[layer][-1]) + self.bucket_tower[layer][-2] <= (2 ** (layer + 1)):  # 2^b보다 작을때 2개를 올림
                        a1 = self.bucket_tower[layer].pop()
                        a2 = self.bucket_tower[layer].pop()
                        a1.insert(0,a2)
                        self.bucket_tower[layer + 1].insert(0, a1)
                    else:  # 2^b 보다 클때 1개만 올림
                        a1 = self.bucket_tower[layer].pop()
                        self.bucket_tower[layer + 1].insert(0, a1)

            elif type(self.bucket_tower[layer][-1]) is int: # layer[-1]이 int일 때
                if type(self.bucket_tower[layer][-2]) is list:
                    if self.bucket_tower[layer][-1] + sum(self.bucket_tower[layer][-2]) <= (2**(layer+1)): # 2^b보다 작을때 2개를 올림
                        a1 = self.bucket_tower[layer].pop()
                        a2 = self.bucket_tower[layer].pop()
                        a2.append(a1)
                        self.bucket_tower[layer + 1].insert(0, a2)
                    else:  # 2^b 보다 클때 1개만 올림
                        a1 = self.bucket_tower[layer].pop()

                        self.bucket_tower[layer + 1].insert(0, a1)

                elif type(self.bucket_tower[layer][-2]) is int:
                    if self.bucket_tower[layer][-1] + self.bucket_tower[layer][-2] <= (2**(layer+1)): # 2^b보다 작을때 2개를 올림
                        a1 = self.bucket_tower[layer].pop()
                        a2 = self.bucket_tower[layer].pop()
                        self.bucket_tower[layer + 1].insert(0, [a1, a2])
                    else:  # 2^b 보다 클때 1개만 올림
                        a1 = self.bucket_tower[layer].pop()
                        self.bucket_tower[layer + 1].insert(0, a1)
            layer +=1

dgim = Dgim()
dgim1 = Dgim1()
dgim2 = Dgim2()


dgim1_layer = [[],[],[],[]]
bit_0_stream = []
bit_1_stream = []
bit_2_stream = []
bit_3_stream = []
bit = []
bitstream = []

for i in range(10000):
    prob = random.random()
    a = random.randint(0,15)
    bitstream.append(a)

    for j in range(random.randint(0,15)):
        if random.random() < prob:
            bit.append(1)
        else:
            bit.append(0)

    a = (random.randint(0,15))
    str = format(a, 'b')
    str = str.zfill(4)
    for i in range(len(str)):
        if i == 0:
            bit_3_stream.append(int(str[i]))
        elif i == 1:
            bit_2_stream.append(int(str[i]))
        elif i == 2:
            bit_1_stream.append(int(str[i]))
        elif i == 3:
            bit_0_stream.append(int(str[i]))

for b in bitstream:
    dgim.put(b)
for b in tqdm(bitstream):
    dgim2.put(b)

idx = [0]
summ = [0]
b = 0
id = 0
for k in range(len(dgim2.bucket_tower)):
    for i in range(len(dgim2.bucket_tower[k])):
        if type(dgim2.bucket_tower[k][i]) is int:
            b +=1
            idx.append(b)
            c = summ[-1]
            c = c + dgim2.bucket_tower[k][i]
            summ.append(c)
        elif type(dgim2.bucket_tower[k][i]) is list:
            if len(dgim2.bucket_tower[k]) == 1:
                idx.append(b +len(dgim2.bucket_tower[k][i]))
                b += len(dgim2.bucket_tower[k][i])
                c = summ[-1]
                c = c + sum(dgim2.bucket_tower[k][i])
                summ.append(c)
                continue
            elif len(dgim2.bucket_tower[k]) == 2:
                idx.append(b + len(dgim2.bucket_tower[k][i]))
                b += len(dgim2.bucket_tower[k][i])
                c = summ[-1]
                c = c + sum(dgim2.bucket_tower[k][i])
                summ.append(c)


dgim2_answer = [0]
id = 1
for k in range(1,2000):
    if idx[id] == k:
        dgim2_answer.append(summ[id])
        id +=1
    else:
        next = idx[id]
        before = idx[id-1]
        next_sum = summ[id]
        before_sum = summ[id-1]
        rest = next-before
        rest_sum = next_sum - before_sum
        rest_sum = (1- (idx[id]-k)/rest) * rest_sum
        dgim2_answer.append((round(summ[id-1] + rest_sum)))


for b in bit_3_stream:
    dgim.put(b)
third_cnt = 0
for k in range(1,2000):
    third_cnt = dgim.count(k)
    third_sum = sum(bit_3_stream[-k:])
    dgim1_layer[3].append(third_cnt)

for b in bit_2_stream:
    dgim.put(b)

second_cnt = 0
for k in range(1,2000):
    second_cnt = dgim.count(k)
    second_sum = sum(bit_2_stream[-k:])
    dgim1_layer[2].append(second_cnt)

for b in bit_1_stream:
    dgim.put(b)

first_cnt = 0
for k in range(1, 2000):
    first_cnt = dgim.count(k)
    first_sum = sum(bit_1_stream[-k:])
    dgim1_layer[1].append(first_cnt)

for b in bit_0_stream:
    dgim.put(b)

zero_cnt = 0
for k in range(1,2000):
    zero_cnt = dgim.count(k)
    zero_sum = sum(bit_0_stream[-k:])
    dgim1_layer[0].append(zero_cnt)

real_answer = []
dgim1_answer = []
for k in range(1,2000):
    real_answer.append(sum(bitstream[-k:]))
    total_dgim1 = dgim1_layer[0][k-1] * 1 + dgim1_layer[1][k-1] * 2 + dgim1_layer[2][k-1] * 4 + dgim1_layer[3][k-1] * 8
    dgim1_answer.append(total_dgim1)

ddd = dgim2_answer[1:]
for i in range(1,2000,20):
    print(real_answer[i], dgim1_answer[i], ddd[i])


plt.plot([i for i in range(1,2000)],real_answer,color = 'red',label = 'dgim')
plt.plot([i for i in range(1,2000)],dgim1_answer,color = 'skyblue',label = 'dgim1')
plt.plot([i for i in range(1,2000)],dgim2_answer[1:],color = 'green',label = 'dgim2')
plt.title("dgim")
plt.legend(loc = 'upper left')
plt.show()


