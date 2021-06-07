import math


target = b"Hello, world!"


def find_factors(x):
    step = 2 if x % 2 else 1
    for i in range(1, int(x ** 0.5) + 1, step):
        if x % i == 0 and i > 1:
            return [i] + find_factors(int(x / i))
    return [x]


def compress(target):
    num = int.from_bytes(target, byteorder='big')
    print(num)

    factors = find_factors(num)
    factors = {i: factors.count(i) for i in factors}
    total_length = num.bit_length()
    index_length = total_length.bit_length()

    result = "0" * index_length + "1"

    for k, v in factors.items():
        for i in (k, v):
            length = i.bit_length()
            binary = bin(length)
            bin_len = len(binary) - 2
            buffer = "0"*(index_length-bin_len)
            result += buffer + binary[2:]

    result += "0"*index_length

    for k, v in factors.items():
        for i in (k, v):
            result += bin(i)[2:]
    return result


def extract(target):
    index_len = len(target[:target.find("1")])

    indices = []
    prev = 0
    for i in range(index_len+1, len(target), index_len*2):
        start, end = i, index_len*2 + i
        section = target[start:end]
        if int(section[:index_len], base=2) == 0:
            prev = end-index_len
            break
        indices.append([int(section[:index_len], base=2), int(section[index_len:], base=2)])

    parent = 1

    for n, q in indices:
        num_sect = target[prev:prev+n]
        number = int(num_sect, base=2)
        quant_sect = target[prev+n:prev+n+q]
        quantity = int(quant_sect, base=2)

        parent *= (number ** quantity)

        prev = prev+n+q

    print(parent)
    return bytes.fromhex(hex(parent)[2:])


out = compress(target)
print(extract(out))

