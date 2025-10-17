
s1 = "Python"
s2 = ""
for i in range (len(s1)):
    s2 += s1[i]
    if i != len(s1)-1:
        s2 += "_"

print(s2)

