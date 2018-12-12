def firstFit(weight,num,count):
    global need
    bin_rem=[0]*num
    res=0

    for i in weight:
        need = 0
        for j in range(res):
            if bin_rem[j] >= i:
                bin_rem[j] -= i
                break
            else:
                need+=1
        if need==res:
            bin_rem[res]=c-i
            res+=1
    return res

import sys
weight = [2, 5, 4, 7, 1, 3, 8]
c = 10
n = int(len(weight))
print("Number of bins required in First Fit : {}".format(firstFit(weight, n, c)))

