file = open("String.txt")
line = file.read().split()

alphabetic = sorted(line, key=str.lower)
print("Alfabetycznie:", alphabetic)

sorted_length = sorted(line, key=len)
print("Według długości:", sorted_length)