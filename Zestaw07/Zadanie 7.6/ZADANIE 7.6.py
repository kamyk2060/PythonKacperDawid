import random


class ZeroOneIterator:
    def __init__(self):
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        result = self.current
        self.current = 1 - self.current  # Zamienia 0 na 1 i 1 na 0
        return result



class RandomDirectionIterator:
    def __init__(self):
        self.directions = ["N", "E", "S", "W"]

    def __iter__(self):
        return self

    def __next__(self):
        return random.choice(self.directions)


class WeekdayIterator:
    def __init__(self):
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        result = self.current
        self.current = (self.current + 1) % 7  # Cykl 0-6
        return result


# Test iteratorów
print("(a) Zero-One Iterator:")
zero_one = ZeroOneIterator()
for _ in range(10):
    print(next(zero_one), end=" ")
print()

print("\n(b) Random Direction Iterator:")
directions = RandomDirectionIterator()
for _ in range(10):
    print(next(directions), end=" ")
print()

print("\n(c) Weekday Iterator:")
weekdays = WeekdayIterator()
for _ in range(15):
    print(next(weekdays), end=" ")
print()