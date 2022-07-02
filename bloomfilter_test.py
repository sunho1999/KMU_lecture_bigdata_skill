import math
import mmh3
import random

class BloomFilter:
    def __init__(self,capacity, fp_prob):
        self.capacity = capacity
        self.fp_prob = fp_prob
        self.bitarray = 0
        self.n_bits = math.ceil(-math.log(fp_prob, math.e) * capacity / (math.log(2, math.e) ** 2))
        self.n_hashs = int(self.n_bits / capacity * math.log(2, math.e))
        self.seeds = [random.randint(0,9999999) for i in range(self.n_hashs)]


    def put(self, item):
        for i in range(self.n_hashs):
            pos = mmh3.hash(item, self.seeds[i]) % self.n_bits
            self.bitarray |= (1 << pos)


    def test(self, item):
        for i in range(self.n_hashs):
            pos = mmh3.hash(item, self.seeds[i]) % self.n_bits

            if self.bitarray & (1 << pos) == 0:
                return False
        return True


bit_present = ['a','b','c','d','e','f','g','h','j','k','l','m','n','o','p',
               'aa','bb','cc','dd','ff','gg','hh','ii','jj','kk','ll','mm','nn','oo','pp','qq','ss']
bit_absent = ['q','r','s','t','u','v','w','x','y','z']  # 없는 bit (q ~ z)

bloom = BloomFilter(100, 0.1)
for i in range(len(bit_present)):
    bloom.put(bit_present[i])

bit_present = random.sample(bit_present,len(bit_present))

bit_absent = random.sample(bit_absent,len(bit_absent))

test_bit = bit_present[:10] + bit_absent
test_bit = random.sample(test_bit,len(test_bit))

for i in range(len(test_bit)):
    print(test_bit[i],bloom.test(test_bit[i]))