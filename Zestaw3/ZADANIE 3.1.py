x = 2
y = 3
if x > y:
    result = x # Niepotrzebne średniki
else:
    result = y # Niepotrzebne średniki
    
# Problem: W Pythonie nie można umieścić instrukcji if z blokiem kodu w tej samej linii co for.
# for i in "axby": if ord(i) < 100: print (i)

for i in "axby":
    if ord(i) < 100:
        print(i)

# Problem: W Pythonie nie można umieścić instrukcji if z blokiem kodu w tej samej linii co for.
# for i in "axby": if ord(i) < 100: print (i)
for i in "axby":
    print(ord(i) if ord(i) < 100 else i)