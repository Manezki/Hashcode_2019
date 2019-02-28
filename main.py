from hash_io import read_file
from os import path as op

print(read_file(op.join(op.dirname(__file__), "data", "a_example.txt")))