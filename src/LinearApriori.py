
import numpy as np
import csv
import itertools
import time

def LinearAprioriRunner(filename, min_support):
    start = time.time()
    #read data from txt file
    with open(filename) as f:
        content = f.readlines()

    content = [x.strip() for x in content]
    min_support = min_support*len(content)
    print(min_support)

    Transaction = []                  #to store transaction
    Frequent_items_value = {}         #to store all frequent item sets

    #to fill values in transaction from txt file
    for i in range(0,len(content)):
        Transaction.append(content[i].split())

    #function to get frequent one itemset
    def frequent_one_item(Transaction,min_support):
        candidate1 = {}

        for i in range(0,len(Transaction)):
            for j in range(0,len(Transaction[i])):
                if Transaction[i][j] not in candidate1:
                    candidate1[Transaction[i][j]] = 1
                else:
                    candidate1[Transaction[i][j]] += 1

        frequentitem1 = []                      #to get frequent 1 itemsets with minimum support count
        for value in candidate1:
            if candidate1[value] >= min_support:
                frequentitem1 = frequentitem1 + [[value]]
                Frequent_items_value[tuple(value)] = candidate1[value]

        return frequentitem1

    values = frequent_one_item(Transaction,min_support)
    print(values)
    print(Frequent_items_value)


    # to remove infrequent 1 itemsets from transaction
    Transaction1 = []
    for i in range(0,len(Transaction)):
        list_val = []
        for j in range(0,len(Transaction[i])):
            if [Transaction[i][j]] in values:
                list_val.append(Transaction[i][j])
        Transaction1.append(list_val)

    #to generate subsets of itemsets of size k
    def generate_k_subsets(dataset, length):
        subsets = []
        for itemset in dataset:
            subsets.extend(map(list, itertools.combinations(itemset, length)))
        return subsets

    def subset_generation(ck_data,l):
        return map(list,set(itertools.combinations(ck_data,l)))

    #apriori generate function to generate ck
    def apriori_generate(dataset,k):
        ck = []
        #join step
        lenlk = len(dataset)
        for i in range(lenlk):
            for j in range(i+1,lenlk):
                L1 = list(dataset[i])[:k - 2]
                L2 = list(dataset[j])[:k - 2]
                if L1 == L2:
                    ck.append(sorted(list(set(dataset[i]) | set(dataset[j]))))

        #prune step
        final_ck = []
        for candidate in ck:
            all_subsets = list(subset_generation(set(candidate), k - 1))
            found = True
            for i in range(len(all_subsets)):
                value = list(sorted(all_subsets[i]))
                if value not in dataset:
                    found = False
            if found == True:
                final_ck.append(candidate)

        return ck,final_ck

    def generateL(ck,min_support):
        support_ck = {}
        for val in Transaction1:
            for val1 in ck:
                value = set(val)
                value1 = set(val1)

                if value1.issubset(value):
                    if tuple(val1) not in support_ck:
                        support_ck[tuple(val1)] = 1
                    else:
                        support_ck[tuple(val1)] += 1
        frequent_item = []
        for item_set in support_ck:
            if support_ck[item_set] >= min_support:
                frequent_item.append(sorted(list(item_set)))
                Frequent_items_value[item_set] = support_ck[item_set]

        return frequent_item

    # main apriori algorithm function
    def apriori(L1,min_support):
        k = 2;
        start=time.time()
        L = []
        L.append(0)
        L.append(L1)
        time_list=[]
        while(len(L[k-1])>0):
            first_time = time.time()
            ck,final_ck = apriori_generate(L[k-1],k)         
            print("C%d" %(k))
            print(final_ck)
            if (k > 0):
                while(len(L[k-1])>0):
                    l = generateL(final_ck, min_support)
                    L.append(l)
                    print("Frequent %d item" % (k))
                    print(l)
                    k = k + 1
                    ck, final_ck = apriori_generate(L[k - 1], k)
                    time_list.append(time.time()-first_time)
                    print("C%d" % (k))
                    print(final_ck)
                break
        end = time.time()
        return L,time_list,end-start


    L_value,time_list,total_time = apriori(values,min_support)
    print("All frequent itemsets with their support count:")
    print(Frequent_items_value)
    return time_list,total_time
