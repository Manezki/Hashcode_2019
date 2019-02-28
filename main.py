from hash_io import read_file
from os import path as op
import random

def metric(left, right):
    inter = left & right
    l_out = left - right
    r_out = right - left
    return min(inter, l_out, r_out)

if __name__ == "__main__":
    data = read_file(op.join(op.dirname(__file__), "data", "a_example.txt"))
    
    reverse_lookup = {}
    print(data)

    for k, v in data.items():
        for tag in v[1]:
            photos = reverse_lookup.get(tag, set())
            photos.add(k)
            reverse_lookup[tag] = photos
    
    print(reverse_lookup)


    
