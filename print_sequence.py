def print_sequence(n):
    sequence, i = '', 1
    while len(sequence) < n:
        sequence += f'{i}' * i
        i += 1
    print(sequence[:n])


n = int(input('Введите количество элементов последовательности: '))
print_sequence(n)