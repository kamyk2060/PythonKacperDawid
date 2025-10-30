
file = open("String.txt")
line = file.read()

def fun1 ():
    count = len(line.split())
    print(count)

fun1()

