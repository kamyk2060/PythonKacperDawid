
def sum_seq(sequence):
    total = 0
    for item in sequence:
        if isinstance(item, (list, tuple)):
            total += sum_seq(item)
        else:
            total += item
    return total


print(sum_seq([1, (2, 3), [4, (5, 6)], 7]))  # 28

print(sum_seq([1, [2, [3, [4, [5]]]]]))  # 15

print(sum_seq([]))  # 0