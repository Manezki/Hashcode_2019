from hash_io import read_file, print_to_file
from os import path as op
from tqdm import tqdm
from bitsets import bitset
import random

def metric(left, right):
    inter = left & right
    l_out = left - right
    r_out = right - left
    return min(len(inter), len(l_out), len(r_out))


def jaccard(left, right):
    inter = left & right
    total = left | right
    return len(inter)/len(total)

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


def pair_verticals(verticals):
    pass


if __name__ == "__main__":
    #data = read_file(op.join(op.dirname(__file__), "data", "a_example.txt"))
    #data = read_file(op.join(op.dirname(__file__), "data", "c_memorable_moments.txt"))
    #data = read_file(op.join(op.dirname(__file__), "data", "d_pet_pictures.txt"))
    data = read_file(op.join(op.dirname(__file__), "data", "b_lovely_landscapes.txt"))
    

    reverse_lookup = {}
    universe = set()
    #print(data)

    for k, v in data.items():
        for tag in v[1]:
            photos = reverse_lookup.get(tag, set())
            photos.add(k)
            reverse_lookup[tag] = photos
        universe |= v[1]
    
    print("Reverse lookup done")
    #universe = bitset("universe", tuple(universe))

    horizontals = [k for k, v in data.items() if v[0] == "H"]
    verticals = [k for k, v in data.items() if v[0] == "V"]

    # VxV table lower-triangle, [row][col]
    #vertical_pairs = combine_verticals([(k, v[1]) for k, v in data.items() if v[0] == "V"])
    #print(vertical_pairs)
    
    reserve = set(horizontals)
    used = set()

    slideshow = [random.choice(horizontals)]
    reserve -= set([slideshow[-1]])
    used |= set([slideshow[-1]])
    used |= set(verticals)

    # TODO Stop if current value better than achievable
    for _ in tqdm(range(len(reserve))):
        current = slideshow[-1]
        argmax = (None, 5)

        cur_tags = data[current][1]
        candidates = set()

        for t in cur_tags:
            candidates |= reverse_lookup[t]

        candidates -= used
    
        if len(candidates) == 0:
            argmax = (random.choice(list(reserve)), -1)
            
            slideshow.append(argmax[0])
            reserve -= set([argmax[0]])
            used |= set([slideshow[-1]])
            continue

        for photo in candidates:
            value = (0.33 - jaccard(data[current][1], data[photo][1]))**2
            if value < argmax[1]:
                argmax = (photo, value)
        
        slideshow.append(argmax[0])
        reserve -= set([argmax[0]])
        used |= set([slideshow[-1]])
    
    print(slideshow)
    print_to_file( [[item] for item in slideshow], "a" )
