L = [7, 24, 123, 5, 89, 456, 1, 67]
result = ""
for x in L:
    result += str(x).zfill(3)
print(result)