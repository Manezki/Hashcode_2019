from hash_io import read_file
from os import path as op
import random

def metric(left, right):
    inter = left & right
    l_out = left - right
    r_out = right - left
    return min(inter, l_out, r_out)

if __name__ == "__main__":
    example_a = read_file(op.join(op.dirname(__file__), "data", "a_example.txt"))
    
    photos = [k for k, _ in example_a.items()]

    out = [random.choice(photos)]

    


    
