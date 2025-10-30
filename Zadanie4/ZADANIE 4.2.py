

def make_ruler(n):
    s1 = "|"
    s2 = "0"
    przerwa = 4
    for i in range(1, n + 1):
        s1 += "....|"
        for j in range(przerwa - len(str(i)) + 1):
            s2 += " "
        s2 += str(i)

    print(s1)
    print(s2)

def make_grid(rows, cols):
    s1 = "+"
    s2 = "|"
    s3 = ""
    if (rows == 0) or (cols == 0):
        return ""

    for i in range(1,cols+1):
        s1 += "---+"
        s2 += "   |"
    for i in range(1,rows+1):
        s3 += s1
        s3 += "\n"
        s3 += s2
        s3 += "\n"
    s3 += s1
    print(s3)


make_ruler(3)
print()
make_grid(2,4)