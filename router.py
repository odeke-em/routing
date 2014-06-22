#!/usr/bin/env python3
# Author: Emmanuel Odeke <odeke@ualberta.ca>

import math
import random

random.seed(100) # TODO: Find a way of sharing seed

def stepGen(base, avail):
    if not (hasattr(base, '__divmod__') and hasattr(avail, '__divmod__')):
        return None
    elif base < 0 or avail < 0:
        return None
    else:
        return 0 if not avail else math.floor(base/avail) 

def stepRange(base, n):
    if not (hasattr(base, '__divmod__') and hasattr(n, '__divmod__')):
        return None
    elif base <= n:
        return [i for i in range(base)] 

    step = stepGen(base, n) or 1
    seq = [i for i in range(step, base, step)]
  
    seqLen = len(seq) 
    while seqLen > n:
        randPick = random.randint(0, seqLen-2)
        seq.pop(randPick)
        seqLen = len(seq)

    return seq

def rangeSearch(sortedList, query):
    # Binary search algorithm however that returns (lowElem, highElem,)
    # where lowElem = l[low], highElem = l[high]. This helps give the range of an element
    # In the even that an item is present, lowElem = highElem = l[mid]
    low, high = 0, len(sortedList)-1
    lC = hC = None
    while low <= high:
        mid = (low + high)>>1
        if sortedList[mid] == query:
            lC = hC = mid
            break
        elif query < sortedList[mid]:
            hC = mid
            high = mid - 1
        else:
            lC = mid
            low = mid + 1

    return lC, hC

def acquireIndex(seq, query):
    sResult = rangeSearch(seq, query)
    # Greedy search
    tIndex, l = 0, len(sResult)
    while tIndex < l:
        if sResult[tIndex] is not None:
            return sResult[tIndex]
        tIndex += 1

def main():
    sRange = stepRange(10, 6)
    print('Srange', sRange)
    print(acquireIndex(sRange, 10))
    print(acquireIndex(sRange, 0))
    print(acquireIndex(sRange, 5))
    print(acquireIndex(sRange, -1))
    print(acquireIndex(sRange, 12))

if __name__ == '__main__':
    main()
