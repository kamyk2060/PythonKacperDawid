
def RysujMiarke(x):
    s1 = "|"
    s2 = "0"
    przerwa = 4
    for i in range(1,x+1):
        s1 += "....|"
        for j in range (przerwa - len(str(i)) + 1):
            s2 += " "
        s2 += str(i)

    print(s1)
    print(s2)

RysujMiarke(123)