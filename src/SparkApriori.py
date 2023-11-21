from pyspark import SparkContext, SparkConf

def printList(list_a):
  for e in list_a:
    print (e)


def Dprint(info):
    print(info)


def generate_candidates(prev_itemsets, k):
    """
    Generate candidate itemsets of size k from the previous frequent itemsets.
    """
    candidates = set()  # Use a set to store unique candidates
    for itemset1 in prev_itemsets:
        for itemset2 in prev_itemsets:
            union_set = itemset1.union(itemset2)
            if len(union_set) == k:
                candidates.add(tuple(sorted(union_set)))  # Convert set to tuple before adding to set
    return [set(candidate) for candidate in candidates]  # Convert tuples back to sets while returning




def generate_f_k(sc, c_k, shared_itemset, sup):
    def get_sup(x):
        x_sup = len([1 for t in shared_itemset.value if x.issubset(t)])
        if x_sup >= sup:
            return x, x_sup
        else:
            return ()

    f_k = sc.parallelize(c_k).map(get_sup).filter(lambda x: x).collect()
    return f_k


import itertools
import time

def ParallelAprioriRunner(filename, min_sup):

    start = time.time()
    conf = SparkConf().setAppName("YetAnotherFIM4").setMaster("local")
    sc = SparkContext(conf=conf)
    input = sc.textFile(filename)
    # TransectionRDD = input.map(lambda line: line.strip().split(" "))
    n_samples = input.count()
    # min_sup to frequency
    sup = n_samples * min_sup
    print(sup)
    # split sort
    itemset = input.map(lambda line: sorted([item for item in line.strip().split(' ')]))
    # share the whole itemset with all workers
    shared_itemset = sc.broadcast(itemset.map(lambda x: set(x)).collect())
    # store for all freq_k
    frequent_itemset = []

    # prepare candidate_1
    k = 1
    c_k = itemset.flatMap(lambda x: set(x)).distinct().collect()
    c_k = [{x} for x in c_k]
    time_list=[]
    # when candidate_k is not empty
    while len(c_k) > 0:
      start_time=time.time()
        # generate freq_k
      Dprint("Combi Set{}: {}".format(k, c_k))
      f_k = generate_f_k(sc, c_k, shared_itemset, sup)
      Dprint("Freq Set{}: {}".format(k, f_k))

      frequent_itemset.append(f_k)
      k += 1
      # generate candidate_k+1
      c_k = generate_candidates([set(item) for item in map(lambda x: x[0], f_k)], k)
      time_list.append(time.time()-start_time)

    end = time.time()
    time_taken = end - start
    print("Time Taken is:")
    print(time_taken)
    print(time_list)
    sc.stop()
    return time_list,end-start