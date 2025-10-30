
x = [[],[4],(1,2),[3,4],(5,6,7)]
y = [0 for i in range (len(x))]
k = 0

for i in x:
    sum = 0
    for j in i:
        sum += j
    y[k] = sum
    k += 1

print(y)
