from hash_io import read_file
from os import path as op
import random

def metric(left, right):
    inter = left & right
    l_out = left - right
    r_out = right - left
    return min(inter, l_out, r_out)

def combine_verticals(verticals):
    """
    Returns: VxV table of sets. V[0,1] is the union of tags from photos 0,1
    """
    size = len(verticals)
    data = [[set() for i in range(size)] for _ in range(size)]

    for i in range(size):
        for j in range(i):
            data[i][j] |= verticals[i][1] | verticals[j][1]
    
    return data


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

    horizontals = [k for k, v in data.items() if v[0] == "H"]
    verticals = [k for k, v in data.items() if v[0] == "V"]

    # VxV table lower-triangle, [row][col]
    vertical_pairs = combine_verticals([(k, v[1]) for k, v in data.items() if v[0] == "V"])
    print(vertical_pairs)
    
