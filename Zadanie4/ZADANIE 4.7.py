
def flatten(sequence):
    result = []
    for item in sequence:
        if isinstance(item, (list, tuple)):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


# Test z przykładu
sequence = [1, (2, 3), [], [4, (5, 6, 7)], 8, [9]]
print(flatten(sequence))

