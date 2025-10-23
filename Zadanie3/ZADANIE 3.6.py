
def RysujProstokat(x, y):
    s1 = "+"
    s2 = "|"
    s3 = ""
    if (x == 0) or (y == 0):
        return ""

    for i in range(1,y+1):
        s1 += "---+"
        s2 += "   |"
    for i in range(1,x+1):
        s3 += s1
        s3 += "\n"
        s3 += s2
        s3 += "\n"
    s3 += s1
    return s3


print(RysujProstokat(2,4))