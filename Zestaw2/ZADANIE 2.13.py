file = open("String.txt")
line = file.read().split()

sum = 0
for i in range (len(line)):
    sum += len(line[i])

print(sum)