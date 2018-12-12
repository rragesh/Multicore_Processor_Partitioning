def bestFit(weight,num,count):
    bin_rem=[0]*num
    res=0
    print count
    for i in weight:
        min = count+1
        for j in range(res):
            if bin_rem[j] >= i and bin_rem[j]-i < min:
                min = bin_rem[j] - i
                bin = j
                break
        if min==count+1:
            bin_rem[res]=c-i
            res+=1
        else:
            bin_rem[bin]-=i
    return res

weight = [2, 5, 4, 7, 1, 3, 8]
c = 10
n = int(len(weight))
print("Number of bins required in best Fit : {}".format(bestFit(weight, n, c)))
