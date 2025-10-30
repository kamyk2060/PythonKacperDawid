
file = open("String.txt")
line = file.read().split()

first_letter = ""
last_letter = ""
for i in range (len(line)):
    first_letter += line[i][0]
    last_letter += line[i][len(line[i])-1]

print(first_letter)
print(last_letter)

