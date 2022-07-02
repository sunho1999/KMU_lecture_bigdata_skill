from ast import Pass
import itertools
from itertools import combinations


def filter(candidates,k,s):
    itemsets_cnt_k = {}
    with open ("groceries.csv","r") as f:
        for line in f:
            basket = line.strip().split(',')
            for comb in combinations(basket,k):
                comb = frozenset(comb)
                if comb in candidates:
                    if comb not in itemsets_cnt_k:
                        itemsets_cnt_k[comb] = 0
                    itemsets_cnt_k[comb] +=1
    freq_itemsets = set(itemset for itemset, cnt in itemsets_cnt_k.items() if cnt >= s)

    return freq_itemsets

def make_candidate(freq_itemsets,k):
    candidates = set()
    for itemset1 in freq_itemsets:
        for itemset2 in freq_itemsets:
            union = itemset1 | itemset2
            if len(union) == k:
                for item in union:
                    if union - {item} not in freq_itemsets:
                        break
                else:
                    candidates.add(union)
    return candidates


def association_rule(freq_itemsets_all,cnt,candidate_all):

    while(True):
        for i in freq_itemsets_all:
            a = frozenset(list(itertools.combinations(i,cnt)))
            if len(a) == 1:
                continue
            elif (len(a)) != 1:
                a = a - frozenset(i)
            for k in a: # 부분집합
                k = frozenset(k)
                support_i = 0
                support_j = 0
                for j in candidate_all:
                    if k == j.intersection(k):
                        support_i +=1
                    if i == i.intersection(j):
                        support_j +=1
                confidence = support_j/ support_i
                if confidence > 0.1:

                    print(f'{set(k)} -> {set(i)} = confidence : {confidence}, support_i = {support_i}, support_j = {support_j}')
                else:
                    pass
        else:
            cnt+=1


# item 개수 구하기
item_cnt = {}
s = 100

with open ("groceries.csv","r") as f:
    for line in f:
        basket = line.strip().split(',')
        for item in basket:
            if item not in item_cnt:
                item_cnt[item] = 0
            item_cnt[item] +=1

# L1
freq_itemsets = set(frozenset([item]) for item, cnt in item_cnt.items() if cnt >= s)

freq_itemsets_all = freq_itemsets.copy()


candidates_all = set(make_candidate(freq_itemsets,2))

k = 2
while len(freq_itemsets) > 0:
    candidates = make_candidate(freq_itemsets,k)
    candidates_all |= set(candidates)
    freq_itemsets = filter(candidates,k,s)
    freq_itemsets_all |= freq_itemsets
    print(k,len(candidates),len(freq_itemsets))
    k += 1


association_rule(list(freq_itemsets_all),1,candidates_all)

for fi in freq_itemsets_all:
    print(set(fi))


# print(candidates_all)